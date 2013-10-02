#Copyright (C) 2013 Purushotham Kamath, Mathpak Inc
#
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


mpskip<-list();
mpmode<-list();

engineDataNamesGet <- function() {
	tree <- paste(mpapp, mpcomponent, sep='/');
	appdir <- gsub("_", "/", mpapp);
	file <- paste(stagingdir, "/", appdir, "/", mpapp, ".xml", sep ='');
	mpdata <<- engineConfigGet(file, tree);
	lskip <-list();
	lmode <-list();
	for (handle in names(data)) {
		lskip[handle] <-0;
		lmode[handle] <-"w";
	}
	mpskip <<- lskip;
	mpmode <<- lmode;
}

engineOpen <- function(handle, md){
	mpmode[handle] <<- md;
	if(mpmode[handle] == "visual") {
		outputfile <- data[handle];
		outputfile <- gsub(" ", "", outputfile);
		file <- paste(stagingdir, "/", mpapp, "/", outputfile, "/", outputfile, ".png", sep ='');
		png(file);
	}
}

engineClose <- function(handle){
	mpskip[handle]<<-0;
	mpmode[handle]<<- "w";
}


engineRead <- function(handle, records){
	if(is.null(mpdata[handle])) {
		return();
	}
	inputfile <- mpdata[handle];
	inputfile <- gsub(" ", "", inputfile);
	args <- unlist(strsplit(inputfile, "_"));

	#Fix ordering of type, user
	inputfiledir=paste(args[1],args[3], args[2], args[4], sep="/");
	inputfilename=args[4];
	appdir <- gsub("_", "/", mpapp);
	file <- paste(stagingdir, "/", appdir, "/", inputfiledir, "/", inputfilename, ".data", sep ='');
	if(records == 0) {
		samples <- read.csv(file);
	} else {
		samples <- read.csv(file, skip=as.integer(mpskip[handle]), nrows = records);
		mpskip[handle]<<-as.integer(mpskip[handle])+records;
	}
	return(samples);
}

engineWrite <- function(handle, data, mode) {
	if(is.null(mpdata[handle])) {
		return();
	}
	#TBD: Append
	outputfile <- mpdata[handle];
	outputfile <- gsub(" ", "", outputfile);
	args <- unlist(strsplit(outputfile, "_"));
	#Fix ordering of type, user
	outputfiledir=paste(args[1],args[3], args[2], args[4], sep="/");
	outputfilename=args[4];
	appdir <- gsub("_", "/", mpapp);
	file <- paste(stagingdir, "/", appdir, "/", outputfiledir, "/", outputfilename, ".data", sep ='');
	if(mpmode[handle] == "visual") {
		dev.off();
	} else if(mode == 'a') {
		write.table(data, file, col.names=FALSE, row.names=FALSE, quote=FALSE, append=TRUE, sep=',')
	} else {
		write.table(data, file, col.names=TRUE, row.names=FALSE, quote=FALSE, append=FALSE, sep=',')
	}
}

