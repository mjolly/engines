engineConfigGet <-
function (file, tree) 
{
    library("XML")
    xmlText <- paste(readLines(file), "\n", collapse = "")
    doc <- xmlTreeParse(xmlText, asText = TRUE)
    nodes <- unlist(strsplit(tree, "/"))
    datanames <- list()
    apptree <- xmlChildren(doc[[1]]$children[[nodes[1]]])
    if ((length((apptree)[[nodes[2]]])) == 0) 
        return(datanames)
    algtree <- xmlChildren((apptree)[[nodes[2]]])
    for (i in algtree) {
        data <- xmlGetAttr(i, "data")
        if (!is.null(data)) {
            handle <- xmlGetAttr(i, "handle")
            datanames[handle] <- data
        }
    }
    return(datanames)
}
