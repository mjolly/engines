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

engineConfigGet <- function(file, tree) {
	library('XML');
	xmlText <- paste(readLines(file), "\n", collapse="")
	doc <- xmlTreeParse(xmlText, asText=TRUE)
	nodes <- unlist(strsplit(tree, "/"));
	datanames <-list();
	apptree <-xmlChildren(doc[[1]]$children[[nodes[1]]]);
	#print('tree');
	#print(tree);
	if((length((apptree)[[nodes[2]]])) == 0)
		return(datanames);
	#print('apptree');
	#print(apptree);
	algtree <-xmlChildren((apptree)[[nodes[2]]]);
	#print('algtree');
	#print(algtree);
	for(i in algtree) {
		data <- xmlGetAttr(i, "data");
		if(!is.null(data)) {
			handle <- xmlGetAttr(i, "handle");
			datanames[handle] <- data;
		}		
	}
	return(datanames);
}
