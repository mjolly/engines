engineOpen <-
function (handle, md) 
{
    mpmode[handle] <<- md
    if (mpmode[handle] == "visual") {
        outputfile <- data[handle]
        outputfile <- gsub(" ", "", outputfile)
        file <- paste(stagingdir, "/", mpapp, "/", outputfile, 
            "/", outputfile, ".png", sep = "")
        png(file)
    }
}
