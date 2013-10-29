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
import sys
import storm
from uuid import uuid4


#Storm: Read data from stdin, write data to stdout
class MathpakDataStoreStormBolt:
	def __init__(self, stagingdir, app) :
		self.stagingdir = stagingdir;
		self.app = app;
		storm.MODE = storm.Bolt;
		setupInfo = storm.readMsg()
		storm.sendpid(setupInfo['pidDir']);

	def dsWrite(self, filename, data) :
		for line in data:
			storm.emit([line]);

	def dsRead(self, filename, data, records=0) :
		#Read from stdin
		#Copy stdin to local data
		tup = storm.readTuple();
		storm.ANCHOR_TUPLE = tup;
		data.append(tup);
		storm.ack(tup);

	def dsOpen(self, filename, mode):
		return;
	def dsClose(self, filename):
		return;

class MathpakDataStoreStormSpout:
	def __init__(self, stagingdir, app) :
		self.stagingdir = stagingdir;
		self.app = app;
		storm.MODE = storm.Spout;
		setupInfo = storm.readMsg()
		storm.sendpid(setupInfo['pidDir']);

	def dsWrite(self, filename, data) :
		id = str(uuid4())
		for line in data:
			storm.emit([line]); #, id);

	def ack(self, id):
		pass
	def fail(self, id):
		pass

	def dsRead(self, filename, data, records=0) :
		#Read from stdin
		#Copy stdin to local data
		msg = storm.readCommand()
		if msg["command"] == "next":
			data.append("next");
		if msg["command"] == "ack":
			self.ack(msg["id"])
		if msg["command"] == "fail":
			self.fail(msg["id"])
		storm.sync()

	def dsOpen(self, filename, mode):
		return;
	def dsClose(self, filename):
		return;

