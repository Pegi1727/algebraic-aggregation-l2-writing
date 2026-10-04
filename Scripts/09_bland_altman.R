# Analysis entry point: 09_bland_altman; see README.md
args <- commandArgs(trailingOnly=FALSE); fileArg <- grep("^--file=",args,value=TRUE); scriptDir <- dirname(normalizePath(sub("^--file=","",fileArg[1])))
source(file.path(scriptDir,"r_helper.R")); run_analysis("09_bland_altman")
