
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
import MathpakDataStoreHadoop;
import MathpakDataStoreStorm;
import MathpakEngineWorkFlow;

class MathpakEngineIOFile :

	def __init__(self, component, app, stagingdir) :
		self.app=app;
		self.stagingdir =stagingdir;
		self.wf = MathpakEngineWorkFlow.MathpakEngineWorkFlow(app);
		self.dsf = {};
		self.data = {};
		self.component=component;
		self.app=app;

	def engineDataNamesGet(self):
		appdir=self.app.replace("_", "/");
		self.file = self.stagingdir+"/"+appdir+"/"+self.app+".xml";
		self.data = self.wf.engineDataNamesGet(self.file, self.component);
		for handle in self.data.keys() :
			
			dtyp = self.data[handle].split("/")[3];  #data starts with /, hence field 3
			ctyp = self.component.split("_")[1];
			if dtyp == "file":
				self.dsf[handle] = MathpakDataStoreFile.MathpakDataStoreFile(self.stagingdir, self.app);
			elif dtyp == "hadoop":
				self.dsf[handle] = MathpakDataStoreHadoop.MathpakDataStoreHadoop(self.stagingdir, self.app);
			elif dtyp == "storm":
				if ctyp == "conn":
					self.dsf[handle] = MathpakDataStoreStorm.MathpakDataStoreStormSpout(self.stagingdir, self.app);
				else:
					self.dsf[handle] = MathpakDataStoreStorm.MathpakDataStoreStormBolt(self.stagingdir, self.app);

	def engineRead(self, handle, records=0) :
		f = self.data[handle];
		f = f.strip();
		tarray = [];
		self.dsf[handle].dsRead(f, tarray, records);
		return tarray;
	
	def engineWrite(self, handle, data) :
		f = self.data[handle];
		f = f.strip();
		self.dsf[handle].dsWrite(f, data);

	def engineOpen(self, handle, mode):
		f = self.data[handle];
		f = f.strip();
		self.dsf[handle].dsOpen(f, mode);
	
	def engineClose(self, handle):
		f = self.data[handle];
		f = f.strip();
		self.dsf[handle].dsClose(f);
