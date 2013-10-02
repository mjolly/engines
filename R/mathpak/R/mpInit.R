mpInit <-
function () 
{
    stagingdir <<- Sys.getenv(c("MATHPAK_STAGING"))
    cmdargs <- commandArgs()
    mpapp <<- cmdargs[6]
    cat("Staging directory: ", stagingdir, "\n")
    cat("App:", mpapp, "\n")
    cat("Code:", mpcomponent, "\n")
    engineDataNamesGet()
    cat("Data:")
    print(mpdata)
}
