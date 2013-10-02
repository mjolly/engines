engineDataNamesGet <-
function () 
{
    tree <- paste(mpapp, mpcomponent, sep = "/")
    appdir <- gsub("_", "/", mpapp)
    file <- paste(stagingdir, "/", appdir, "/", mpapp, ".xml", 
        sep = "")
    mpdata <<- engineConfigGet(file, tree)
    lskip <- list()
    lmode <- list()
    for (handle in names(data)) {
        lskip[handle] <- 0
        lmode[handle] <- "w"
    }
    mpskip <<- lskip
    mpmode <<- lmode
}
