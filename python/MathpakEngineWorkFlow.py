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


import xml.etree.ElementTree as ET;



class MathpakEngineWorkFlow:
	def __init__(self, name):
		self.name=name;

	def engineDataNamesGet(self, file, component) :
		data = {};
		tree = ET.parse(file)
		root = tree.getroot();
		for c in root:
			if(c.tag == component):
				for s in c:
					if 'data' in s.attrib.keys():
						d = s.attrib['data'];
						h = s.attrib['handle'];
						args = d.split("_");
						cl = args[0];
						type = args[1];
						user = args[2];
						name = args[3];
						#Fix the ordering of user/typein directory structure
						ddir = cl+"/"+user+"/"+type+"/"+name;
						dname = "/"+ddir+"/"+name+".data";
						data[h] = dname;
		return data;
