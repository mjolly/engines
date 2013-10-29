/*
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
*/

mpArgsGet =function() {
	var query = location.href.substring((location.href.indexOf('?')+1), location.href.length);
	if(location.href.indexOf('?') < 0) 
		query = '';

	//Use ; as a separator (gitweb uses ;, and need to maintain compatibility)
	querysplit = query.split(';');
	query = new Array();

	for(var i = 0; i < querysplit.length; i++){
		var namevalue = querysplit[i].split('=');
		namevalue[1] = namevalue[1].replace(/\+/g, ' ');
		if(namevalue[0] == "mpapp") {
			mpApp = namevalue[1];
		}
		if(namevalue[0] == "mpserver") {
			mpServer = namevalue[1];
		}
	}

}



//Check if all needed data has been downloaded. Downloading of data is async (ajax)
var mpDataLoaded = function(dh) {
	mpLoaded[dh] = true;
	var dataload = true;
	//Check if all data has been loaded
	for (var i = 0; i < mpDatahandle.length; i++) {
		var d = mpDatahandle[i];
		dataload = dataload & mpLoaded[d];
	}
	if(dataload == true) {
		//Call user callback after all data is downloaded
		mpBuild();
	}
}

var mpCSVDownload = function(dh, dn, dserver) {
	var project = dn;
	var file = dn.split("/")[3]+".data";
	var sloc = mpUrl.replace("SERVER", dserver);
	var tloc = sloc.replace("PROJECT", project);
	var loc = tloc.replace("FILE", file);
	d3.csv(loc, function(csv) {
		mpData[dh] = csv;
		//Mark data as loaded, and check if all data loaded
		mpDataLoaded(dh);
	})
}

var mpPNGDownload = function(drht, dn, dserver) {
	var project = dn;
	var file = dn.split("/")[3]+".png";
	var sloc = mpUrl.replace("SERVER", dserver);
	var tloc = sloc.replace("PROJECT", project);
	var loc = tloc.replace("FILE", file);
	mpData[dh] = loc;
	mpDataLoaded(dh);
}


/* Must be called only in mpInit() callback (after config xml file is loaded and mpData arrays are initialized)*/
var mpReadAll = function() {
	for (var i = 0; i < mpDatahandle.length; i++) {
		if(mpDataformat[i] == "csv") {
			mpCSVDownload(mpDatahandle[i], mpDataname[i], mpDataserver[i]);
		} else if(dataformat[i] == "png") {
			mpPNGDownload(mpDatahandle[i], mpDataname[i], mpDataserver[i]);
		} else {
			//Default is CSV
			mpCSVDownload(mpDatahandle[i], mpDataname[i], mpDataserver[i]);
		}
	}
}

/*Must be called only in mpInit() callback (after config xml file is loaded and mpData arrays are initialized)*/
/* TBD, add user callback argument */
var mpRead = function(dataname) {
	for (var i = 0; i < datatype.length; i++) {
		if(mpDataname[i] == dataname) {
			if(mpDataformat[i] == "csv") {
				mpCSVDownload(mpDatahandle[i], mpDataname[i], mpDataserver[i]);
			} else if(dataformat[i] == "png") {
				mpPNGDownload(mpDatahandle[i], mpDataname[i], mpDataserver[i]);
			} else {
				//Default is CSV
				mpCSVDownload(mpDatahandle[i], mpDataname[i], mpDataserver[i]);
			}
		}
	}
}


var mpData = new Array();
var mpDatahandle= new Array();
var mpDataname= new Array();
var mpDataformat= new Array();
var mpDataserver= new Array();
var mpLoaded = new Array();

var mpApp="";
var mpServer="cs.mathpak.com";  //Name of server where the app file resides, cs.mathpak.com or demo.mathpak.com for most apps
mpUrl = "http://SERVER/?p=PROJECT.git;a=blob_plain;f=FILE";

var mpInit=function(visual, local) {
	mpArgsGet();
	var regex = new RegExp('_', 'g');
	var appfile = mpApp.replace(regex, "/");

	mpVisual = visual;
	mpLocal = local;
	var ploc;
	if(mpLocal) {
		mpUrl = "/PROJECT/FILE";
		ploc = mpUrl.replace("PROJECT", appfile);
	} else {
		mpAppUrl = "http://SERVER/git?p=PROJECT.git;a=blob_plain;f=FILE";
		sloc = mpAppUrl.replace("SERVER", mpServer);
		ploc = sloc.replace("PROJECT", appfile);
	}
	var file = mpApp+".xml";
	var appfile = ploc.replace("FILE", file);
	$.ajax({
		type: "GET",
		url: appfile,
		dataType: "xml",
		success: function(xml) {
			var $tree = $(xml).find(mpVisual).children();
			var i=0;	
			$tree.each(function(){
				if ($(this).attr("handle") != null) {
					mpDatahandle[i] = $(this).attr('handle');
					var dataname = $(this).attr('data');
					
					//Fix the name/type ordering 
					var args  = dataname.split("_");
					//var regex = new RegExp('_', 'g');
					mpDataname[i] = args[0]+"/"+args[1]+"/"+args[2]+"/"+args[3];

					mpDataformat[i] = $(this).attr('format');
					mpDataserver[i] = $(this).attr('server');
					i=i+1;
				}
			});
			mpReadAll();
		}
	});
}
