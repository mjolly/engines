engineRead <-
function (handle, records) 
{
    if (is.null(mpdata[handle])) {
        return()
    }
    inputfile <- mpdata[handle]
    inputfile <- gsub(" ", "", inputfile)
    args <- unlist(strsplit(inputfile, "_"))
    inputfiledir = paste(args[1], args[3], args[2], args[4], 
        sep = "/")
    inputfilename = args[4]
    appdir <- gsub("_", "/", mpapp)
    file <- paste(stagingdir, "/", appdir, "/", inputfiledir, 
        "/", inputfilename, ".data", sep = "")
    if (records == 0) {
        samples <- read.csv(file)
    }
    else {
        samples <- read.csv(file, skip = as.integer(mpskip[handle]), 
            nrows = records)
        mpskip[handle] <<- as.integer(mpskip[handle]) + records
    }
    return(samples)
}
