#!/usr/bin/python
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

import fileinput

#Hadoop streaming: Read data from stdin, write data to stdout
class MathpakDataStoreHadoop:
	def __init__(self, stagingdir, app) :
		self.stagingdir = stagingdir;
		self.app = app;
		self.files = {};
		self.rdata = {};
		self.wdata = {};
		rindex = 0;

	def dsWrite(self, filename, data) :
		#TBD append
		for line in wdata:
			wdata.append(line);


	def dsRead(self, filename, data, records=0) :
		#Read from stdin
		if(records ==0):
			#Read entire input in one read
			for line in rdata:
				data.append(line);
		else:
			#Read n records,
			for count in range(0, records):
				line = rdata[rindex];
				if line  != "":
					rindex = rindex +1;
					data.append(line);

	def dsOpen(self, filename, mode):
		#Copy stdin to local data
		for line in fileinput.input():
			rdata.append(line);

	def dsClose(self, filename):
		for line in wdata:
			print line;
