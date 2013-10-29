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

import MathpakDataStoreFile;
import MathpakEngineIOFile;
import MathpakEngineWorkFlow;
import os;
import sys;

class MathpakEngine:
	def __init__(self, component) :
		if len(sys.argv) > 2:
			self.stagingdir = sys.argv[2];
		else:
			self.stagingdir = os.environ.get('MATHPAK_STAGING')
		self.app=sys.argv[1];
		self.component=component;
		self.func=self.component;
		self.io = MathpakEngineIOFile.MathpakEngineIOFile(self.component, self.app, self.stagingdir);
		self.io.engineDataNamesGet();

	def open(self, handle, mode):
		return self.io.engineOpen(handle, mode);

	def close(self, handle) :
		return self.io.engineClose(handle);

	def read(self, handle, records=0) :
		return self.io.engineRead(handle, records);

	def write(self, handle, data) :
		return self.io.engineWrite(handle, data);
