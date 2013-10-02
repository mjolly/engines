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

class MathpakDataStoreFile:

	def __init__(self, stagingdir, app) :
		self.stagingdir = stagingdir;
		self.app = app;
		self.files = {};

	def dsWrite(self, filename, data) :
		#TBD append
		for line in data:
			self.files[filename].write(line);

	def dsRead(self, filename, data, records=0) :
		#TBD check number of copies here, improve efficiency?
		if(records ==0):
			#Read entire file in one read
			tdata = self.files[filename].readlines();
			for line in tdata:
				data.append(line);
		else:
			#Read n records,
			for count in range(0, records):
				line = self.files[filename].readline();
				if(line  != ""):
					data.append(line);

	def dsOpen(self, filename, mode):
		if (filename not in self.files.keys()) :
			appdir=self.app.replace("_", "/");
			fullname = self.stagingdir+"/"+appdir+"/"+filename;
			if(mode =='r'):
				self.files[filename] = file(fullname, 'r');
			else:
				self.files[filename] = file(fullname, 'w');

	def dsClose(self, filename):
			self.files[filename].close();
