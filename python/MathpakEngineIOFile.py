
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
import MathpakEngineWorkFlow;

class MathpakEngineIOFile :

	def __init__(self, mode, component, app, stagingdir) :
		self.app=app;
		self.stagingdir =stagingdir;
		self.wf = MathpakEngineWorkFlow.MathpakEngineWorkFlow(app);
		self.dsf = MathpakDataStoreFile.MathpakDataStoreFile(self.stagingdir, self.app);
		self.data = {};
		self.component=component;
		self.app=app;
		self.mode=mode;

	def engineDataNamesGet(self):
		appdir=self.app.replace("_", "/");
		self.file = self.stagingdir+"/"+appdir+"/"+self.app+".xml";
		self.data = self.wf.engineDataNamesGet(self.file, self.component);
		for handle in self.data.keys() :
			print("Handle: "+handle+" Data:"+self.data[handle]);

	def engineRead(self, handle, records=0) :
		f = self.data[handle];
		f = f.strip();
		tarray = [];
		self.dsf.dsRead(f, tarray, records);
		return tarray;
	
	def engineWrite(self, handle, data) :
		f = self.data[handle];
		f = f.strip();
		self.dsf.dsWrite(f, data);

	def engineOpen(self, handle, mode):
		f = self.data[handle];
		f = f.strip();
		self.dsf.dsOpen(f, mode);
	
	def engineClose(self, handle):
		f = self.data[handle];
		f = f.strip();
		self.dsf.dsClose(f);
