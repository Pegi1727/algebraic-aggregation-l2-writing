"""Shared implementation for the 10 Python analysis entry points."""
import argparse, os, sys
import pandas as pd
import numpy as np

def detect(df, explicit, candidates, label, required=True):
    if explicit:
        if explicit not in df.columns: raise ValueError(f"{label} column {explicit!r} absent. Available: {list(df.columns)}")
        return explicit
    for c in candidates:
        if c in df.columns: return c
    if required: raise ValueError(f"Cannot detect {label}. Pass --{label.replace(' ','-')}; available: {list(df.columns)}")
    return None

def run(op):
    p=argparse.ArgumentParser(description='Reproducible L2 writing assessment analysis; source files are read-only.')
    p.add_argument('--input',required=True,help='Input CSV path')
    p.add_argument('--output',required=True,help='Output CSV/PNG path or output directory for multi-file results')
    p.add_argument('--human-col'); p.add_argument('--prediction-col'); p.add_argument('--id-col'); p.add_argument('--group-col')
    p.add_argument('--columns',help='Comma-separated rubric dimension columns')
    p.add_argument('--models',help='Comma-separated model/prediction columns')
    p.add_argument('--lambda',dest='lam',type=float,default=.5,help='Composite Min-Add lambda in [0,1]')
    a=p.parse_args(); df=pd.read_csv(a.input); out=a.output
    if os.path.isdir(out) or out.endswith(os.sep): os.makedirs(out,exist_ok=True); base=os.path.join(out,op+'.csv')
    else: os.makedirs(os.path.dirname(os.path.abspath(out)),exist_ok=True); base=out
    def save(x,path=base): x.to_csv(path,index=False); print(path)
    nums=df.select_dtypes(include='number')
    if op=='01_validate_files':
        report=pd.DataFrame({'column':df.columns,'dtype':[str(x) for x in df.dtypes],'missing':[int(df[c].isna().sum()) for c in df]})
        save(report); print(f'rows={len(df)} columns={len(df.columns)} duplicate_rows={int(df.duplicated().sum())}')
    elif op=='02_descriptive_summary':
        if nums.empty: raise ValueError('No numeric columns found')
        save(nums.describe().T.reset_index(names='column'))
    elif op=='03_aggregate_rubric_dimensions':
        cols=[x.strip() for x in a.columns.split(',')] if a.columns else [x for x in ['L','I','C','A','Linguistic_Accuracy_L','Intelligibility_I','Communicative_Adequacy_C','Academic_Appropriateness_A'] if x in df]
        if len(cols)<2 or any(c not in df for c in cols): raise ValueError('Pass --columns with >=2 existing rubric columns')
        if not 0<=a.lam<=1: raise ValueError('--lambda must be in [0,1]')
        x=df[cols].apply(pd.to_numeric,errors='coerce');
        if x.isna().any().any(): raise ValueError('Rubric columns contain missing/non-numeric values')
        if ((x<0)|(x>1)).any().any(): raise ValueError('Lukasiewicz t-norm requires normalized values in [0,1]')
        z=pd.DataFrame({'mean':x.mean(axis=1),'minimum':x.min(axis=1),'lukasiewicz_tnorm':np.maximum(0,x.sum(axis=1)-(len(cols)-1)),'composite_min_add':a.lam*x.min(axis=1)+(1-a.lam)*x.mean(axis=1)})
        save(z)
    elif op in ('04_model_metrics_vs_human','09_bland_altman'):
        h=detect(df,a.human_col,['Human_Global','Human_Holistic_Criterion'],'human'); models=[x.strip() for x in a.models.split(',')] if a.models else [x for x in ['Additive','Min','Luk_4D','Composite_Min_Add'] if x in df]
        if not models: models=[c for c in nums.columns if c!=h]
        if any(c not in df for c in models): raise ValueError('One or more --models columns missing')
        rows=[]
        for m in models:
            x=pd.concat([pd.to_numeric(df[h],errors='coerce'),pd.to_numeric(df[m],errors='coerce')],axis=1).dropna(); d=x.iloc[:,1]-x.iloc[:,0]
            row={'model':m,'n':len(x),'MAE':d.abs().mean(),'RMSE':np.sqrt((d*d).mean()),'bias':d.mean()}
            if op=='09_bland_altman': row.update({'mean_pair':((x.iloc[:,1]+x.iloc[:,0])/2).mean(),'loa_lower':d.mean()-1.96*d.std(ddof=1),'loa_upper':d.mean()+1.96*d.std(ddof=1)})
            rows.append(row)
        save(pd.DataFrame(rows))
    elif op=='05_subgroup_metrics':
        h=detect(df,a.human_col,['Human_Global','Human_Holistic_Criterion'],'human'); g=detect(df,a.group_col,['Profile'],'group'); models=[x.strip() for x in a.models.split(',')] if a.models else [c for c in ['Additive','Min','Luk_4D','Composite_Min_Add'] if c in df]
        rows=[]
        for group,part in df.groupby(g,dropna=False):
            for m in models:
                if m not in part: continue
                d=pd.to_numeric(part[m],errors='coerce')-pd.to_numeric(part[h],errors='coerce'); d=d.dropna(); rows.append({'group':group,'model':m,'n':len(d),'MAE':d.abs().mean(),'RMSE':np.sqrt((d*d).mean()),'bias':d.mean()})
        save(pd.DataFrame(rows))
    elif op=='06_bootstrap_mae':
        cols=[x.strip() for x in a.models.split(',')] if a.models else list(nums.columns)
        save(pd.DataFrame([{'metric':c,'n':int(nums[c].notna().sum()),'mean':nums[c].mean(),'sd':nums[c].std(),'q025':nums[c].quantile(.025),'median':nums[c].median(),'q975':nums[c].quantile(.975)} for c in cols if c in nums]))
    elif op=='07_paired_model_tests':
        from scipy.stats import wilcoxon
        cols=[x.strip() for x in a.models.split(',')] if a.models else [c for c in nums if 'MAE' in c]
        if len(cols)<2: raise ValueError('Provide at least two paired error/MAE columns via --models')
        from itertools import combinations
        pairs=[]
        for x,y in combinations(cols,2):
            z=nums[[x,y]].dropna(); stat,pv=wilcoxon(z[x],z[y]); pairs.append({'model1':x,'model2':y,'n':len(z),'statistic':stat,'p_raw':pv})
        res=pd.DataFrame(pairs); order=np.argsort(res.p_raw); adj=np.empty(len(res)); running=0
        for rank,i in enumerate(order): running=max(running,(len(res)-rank)*res.p_raw.iloc[i]); adj[i]=min(1,running)
        res['p_holm']=adj; save(res)
    elif op=='08_sensitivity_lambda':
        x=nums.copy(); lam=detect(df,None,['Weight_Comm_w'],'lambda',False)
        if not lam: raise ValueError('Need numeric weight column (e.g. Weight_Comm_w)')
        save(x.assign(lambda_value=pd.to_numeric(df[lam],errors='coerce')))
    elif op=='10_publication_figures':
        import matplotlib.pyplot as plt
        cols=[x.strip() for x in a.models.split(',')] if a.models else list(nums.columns)
        ax=nums[[c for c in cols if c in nums]].plot(kind='box',figsize=(9,5)); ax.set_ylabel('Observed value'); ax.set_title('L2 writing assessment: input distributions'); plt.tight_layout()
        target=out if out.lower().endswith('.png') else os.path.join(out,'10_publication_figures.png'); os.makedirs(os.path.dirname(os.path.abspath(target)),exist_ok=True); plt.savefig(target,dpi=300); plt.close(); print(target)
    else: raise ValueError(op)
if __name__=='__main__': run(os.path.basename(sys.argv[0])[:2]+'_'+os.path.basename(sys.argv[0]).split('_',1)[1][:-3])
