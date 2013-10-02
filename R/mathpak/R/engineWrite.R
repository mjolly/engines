engineWrite <-
function (handle, data, mode) 
{
    if (is.null(mpdata[handle])) {
        return()
    }
    outputfile <- mpdata[handle]
    outputfile <- gsub(" ", "", outputfile)
    args <- unlist(strsplit(outputfile, "_"))
    outputfiledir = paste(args[1], args[3], args[2], args[4], 
        sep = "/")
    outputfilename = args[4]
    appdir <- gsub("_", "/", mpapp)
    file <- paste(stagingdir, "/", appdir, "/", outputfiledir, 
        "/", outputfilename, ".data", sep = "")
    if (mpmode[handle] == "visual") {
        dev.off()
    }
    else if (mode == "a") {
        write.table(data, file, col.names = FALSE, row.names = FALSE, 
            quote = FALSE, append = TRUE, sep = ",")
    }
    else {
        write.table(data, file, col.names = TRUE, row.names = FALSE, 
            quote = FALSE, append = FALSE, sep = ",")
    }
}
