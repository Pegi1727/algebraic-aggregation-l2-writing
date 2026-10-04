# Analysis entry point: 04_model_metrics_vs_human; see README.md
args <- commandArgs(trailingOnly=FALSE); fileArg <- grep("^--file=",args,value=TRUE); scriptDir <- dirname(normalizePath(sub("^--file=","",fileArg[1])))
source(file.path(scriptDir,"r_helper.R")); run_analysis("04_model_metrics_vs_human")
