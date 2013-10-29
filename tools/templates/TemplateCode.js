/*
Copyright (C) 2013 Purushotham Kamath, Mathpak Inc

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
*/
//Code for component: MATHPAKCOMPONENT


'use strict';
var mpContentGen = function(){
	var inputdata = mpData["input"];
	d3.select("#mpcontent").html('');

	//Display first 14 lines of input, 3 fields only
	var length = (inputdata.length < 14) ? inputdata.length : 14;
	var content = '<table class=\"hor-minimalist-b\"><thead><th>Date</th><th>Open</th><th>Close</th></thead>';
	for (var i = 0; i < length ; i++){
		var line = inputdata[i];
		content = content+'<tr><td>'+line['Date']+'</td><td>'+line['Open']+'</td><td>'+line['Close']+'</td></tr>';
	}
	content = content+'</table>';
	d3.select("#mpcontent").html(content);
}

var mpGraphGen = function(){
	//For image data (png) replace "input" with the handle for the data
	//var link = mpData["input"];
	//$("#mpgraph").html('');
	//var html = '<div><img src="'+link+'" alt="App"/></div>';
	//$("#mpgraph").append(html);


	//For csv data (.data) replace "input" with the handle for the data
	var inputdata = [];
	for (var i = 1 ; i <mpData["input"].length ; i++) {
		var line = mpData["input"][i];
		var datum = [line['Date'], parseFloat(line['Close'])];
		inputdata.push(datum);
	}

	//Use nvd3.js to generate graph
	//
	var input = [{
		area: true,
		values: inputdata,
		key: "Nasdaq",
		color: '#cccccc'
		}
	];

	var chart = nv.models.lineChart()
		.x(function(d) {return Date.parse(d[0])})
		.y(function(d) {return d[1]})
		.options({
			margin: {left: 100, bottom: 100},
			showXAxis: true,
			showYAxis: true,
			forceY:[0,],
			transitionDuration: 250
		});

	chart.xAxis
		.axisLabel("Date")
		.tickFormat(function(d) {
			return d3.time.format('%x')(new Date(d));
		});
		

	chart.yAxis
		.axisLabel('Index')
		.tickFormat(d3.format(',0.1f'));

	d3.select('#mpgraph svg')
		.datum(input)
		.call(chart);

	nv.utils.windowResize(chart.update);

}


var mpAboutGen = function(){
	//About app	
	var alg1= "Demo algorithm";
	var type1= "Algorithm";
	var author1= "Mathpak Inc.";
	var alg2= "Demo visualization";
	var type2= "Visualization";
	var author2= "Mathpak Inc."
	d3.select("#mpaboutapp").html('');
	d3.select("#mpaboutapp").html('<table class=\"hor-minimalist-b\"><thead><th>Component</th><th>Type</th><th>Author</th></thead>'
		+'<tr><td>'+alg1 +'</td><td>'+type1+'</td><td>'+author1+'</td></tr>'
		+'<tr><td>'+alg2 +'</td><td>'+type2+'</td><td>'+author2+'</td></tr>'
		+'</table>'
		);	
	d3.select("#mpaboutmathpak").html('');
	d3.select("#mpaboutmathpak").html('<a href="http://www.mathpak.com">Mathpak</a> is a platform for rapidly building and deploying analytic and visualization apps.');
	d3.select("#mpupdates").html('');
	d3.select("#mpupdates").html('Get the app at the <a href="http://www.mathpak.com"> Mathpak</a> store.');
}




//Call back function. Will be called by mathpak.platform.js after all data is loaded.
var mpBuild = function() {
	mpGraphGen();
	mpContentGen();
	mpAboutGen();
}

//Set local = 1 for local server data (development) (and change js file links in MATHPAKPROJECT/MATHPAKNAME.html from remote to local file links)
//Set local = 0 for mathpak server data (production)
var local=0;
var visual="MATHPAKCOMPONENT";
//Call mathpak initialization function to download all data
mpInit(visual, local);
