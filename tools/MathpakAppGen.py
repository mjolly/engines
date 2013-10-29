#!/usr/bin/env python

import curses
import os
from os import system
from curses import wrapper
import xml.etree.ElementTree as ET;

class MathpakAppGen:
	def __init__(self, stdscr):
		self.mpAppName = "";
		#List of code components
		self.mpCodeComponents= [];
		#Hash table of data components, indexed by code component
		self.mpDataComponents = {}
		
		#Current value as user traverses the options
		self.mpCurrentCodeComponent= "";
		self.mpCurrentDataName= "";
		self.mpCurrentDataHandle= "";
		self.screen =stdscr;

	def get_param(self, screen, prompt_string, offset):
		curses.echo();
		offset = self.mpAppDisp();
		self.screen.addstr(offset+2, 2, prompt_string)
		self.screen.refresh()
		input = self.screen.getstr(offset+5, 10, 60)
		curses.noecho();
		return input
	
	def execute_cmd(self, cmd_string):
		system("clear")
		a = system(cmd_string)
		print ""
		if a == 0:
			print "Command executed correctly"
		else:
			print "Command terminated with error"
		raw_input("Press enter")
		print ""

	def mpMain(self):
		x = 0
		while x != ord('7'):
			self.screen.clear()
			self.screen.border(0)
			offset = self.mpAppDisp();
			self.screen.addstr(offset+2, 2, "Please enter a number.")
			self.screen.addstr(offset+4, 4, "1 - Add a new app")
			self.screen.addstr(offset+5, 4, "2 - Add code/data to current app "+self.mpAppName)
			self.screen.addstr(offset+6, 4, "3 - Delete current app "+self.mpAppName)
			self.screen.addstr(offset+7, 4, "4 - Load app file")
			self.screen.addstr(offset+8, 4, "5 - Generate app file (overwrite, if exists)")
			self.screen.addstr(offset+9, 4, "6 - Generate app directory structure (overwrite, if exists)")
			self.screen.addstr(offset+10, 4, "7 - Exit")
			self.screen.refresh()

			x = self.screen.getch()
			if x == ord('1'):
				self.mpAppAdd();
				curses.endwin()
			if x == ord('2'):
				self.mpAppModify();
				curses.endwin()
			if x == ord('3'):
				self.mpAppDelete();
				curses.endwin()
			if x == ord('4'):
				self.mpAppFileLoad();
				curses.endwin()
			if x == ord('5'):
				self.mpAppFileGen();
				curses.endwin()
			if x == ord('6'):
				self.mpAppDirGen();
				curses.endwin()
		curses.endwin()
	
	def mpAppAdd(self):
		x=0;
		self.screen.clear()
		self.screen.border(0)
		offset = self.mpAppDisp();
		appname = self.get_param(self.screen, "Enter the app name. Use the fully qualified name: Eg: app_utham_Demo", 2+offset)
		self.mpAppName = self.mpAppNameValidate(appname, 6+offset);
		curses.endwin()

	def mpAppModify(self):
		x=0;
		while x != ord('3'):
			self.screen.clear()
			self.screen.border(0)
			offset = self.mpAppDisp();
			self.screen.addstr(2+offset, 2, "Please enter a number.")
			self.screen.addstr(4+offset, 4, "1 - Add a new code component to app "+self.mpAppName)
			self.screen.addstr(5+offset, 4, "2 - Add/delete data to/from an existing code component in app "+self.mpAppName)
			self.screen.addstr(6+offset, 4, "3 - Delete a code component in app "+self.mpAppName)
			self.screen.addstr(7+offset, 4, "4 - Return")
			self.screen.refresh()
			x = self.screen.getch()
			if x == ord('1'):
				self.mpCodeAdd();
				curses.endwin()
			if x == ord('2'):
				self.mpCodeModify();
				curses.endwin()
			if x == ord('3'):
				self.mpCodeDelete();
				curses.endwin()
		curses.endwin()

	def mpAppDelete(self):
		self.mpAppName = "";
		for code in self.mpCodeComponents:
			self.mpDataComponents[code] = [];
		self.mpCodeComponents = [];

		
	def mpAppNameValidate(self, appname, offset):
		fields = appname.split("_");
		if len(fields) != 3 :
			self.screen.addstr(offset, 4, "Error: App name must have 3 fields <app>_<user>_<name>")
			y = self.screen.getch()
			return "";
		if(fields[0] != "app" ) :
			self.screen.addstr(offset, 4, "Error: App name must start with 'app_'")
			y = self.screen.getch()
			return "";
		user = fields[1].lower(); #Must be user name, convert to lower case
		name = fields[0]+"_"+user+"_"+fields[2];
		return name;

				
	def mpDataNameValidate(self, codename, offset):
		fields = codename.split("_");
		if len(fields) != 4 :
			self.screen.addstr(offset, 4, "Error: Data name must have 3 fields <data>_<type>__<user>_<name>")
			y = self.screen.getch()
			return "";
		if fields[0] != "data" :
			self.screen.addstr(offset, 4, "Error: Code name must start with 'code_'")
			y = self.screen.getch()
			return "";
		if fields[2] != "file":
			self.screen.addstr(offset, 4, "Error: Data type (data_user_<type>) must be 'file'");
			y = self.screen.getch()
			return "";
		user = fields[1].title(); #Must be user name, convert first char to upper case
		name = fields[0]+"_"+user+"_"+fields[2]+"_"+fields[3];
		return name;

				
	def mpCodeNameValidate(self, codename, offset):
		fields = codename.split("_");
		if len(fields) != 4 :
			self.screen.addstr(offset, 4, "Error: Code name must have 3 fields <code>_<type>__<user>_<name>")
			y = self.screen.getch()
			return "";
		if fields[0] != "code" :
			self.screen.addstr(offset, 4, "Error: Code name must start with 'code_'")
			y = self.screen.getch()
			return "";
		if(fields[2] != "visual") and (fields[2] != "alg") and (fields[2] != "conn") and (fields[2] != "conv") :
			self.screen.addstr(offset, 4, "Error: Code type (code_user_<type>) must be one of 'alg', 'conn', 'conv' or 'visual'");
			y = self.screen.getch()
			return "";
		user  = fields[1].lower(); #Must be user name, convert first char to lower case
		name = fields[0]+"_"+user+"_"+fields[2]+"_"+fields[3];
		return name;

	def mpCodeAdd(self):
		self.screen.clear()
		self.screen.border(0)
		offset = self.mpAppDisp();
		codename = self.get_param(self.screen, "Enter the code name. Use the fully qualified name, eg. code_utham_alg_DemoCode", 6+offset)
		self.mpCurrentCodeComponent = self.mpCodeNameValidate(codename, 7+offset);
		if self.mpCurrentCodeComponent != "":
			self.mpCodeComponents.append(self.mpCurrentCodeComponent);
			self.mpDataComponents[self.mpCurrentCodeComponent] = [];
		curses.endwin()
	
	def mpCodeModify(self):
		y=0;
		while y != ord('3'):
			self.screen.clear()
			self.screen.border(0)
			offset =self.mpAppDisp();
			self.screen.addstr(2+offset, 2, "Please enter a number.")
			self.screen.addstr(3+offset, 4, "1 - Add data to code")
			self.screen.addstr(4+offset, 4, "2 - Delete data from code")
			self.screen.addstr(5+offset, 4, "3 - Return")
			self.screen.refresh()
			y = self.screen.getch()
			if y == ord('1'):
				self.screen.clear()
				self.screen.border(0)
				offset = self.mpAppDisp();
				codename = self.get_param(self.screen, "Enter the code name. Use the fully qualified name, eg. code_utham_alg_DemoCode", 6+offset)
				self.mpCurrentCodeComponent = self.mpCodeNameValidate(codename, 7+offset);
				self.mpDataAdd(8+offset)
			if y == ord('2'):
				self.screen.clear()
				self.screen.border(0)
				offset = self.mpAppDisp();
				codename = self.get_param(self.screen, "Enter the code name. Use the fully qualified name, eg. code_utham_alg_DemoCode", 6+offset)
				self.mpCurrentCodeComponent = self.mpCodeNameValidate(codename, 7+offset);
				self.mpDataDelete(8+offset)

	def mpCodeDelete(self):
		found = 0;
		self.screen.clear()
		self.screen.border(0)
		offset = self.mpAppDisp();
		codename = self.get_param(self.screen, "Enter the code name. Use the fully qualified name, eg. code_utham_alg_DemoCode", 6+offset)
		self.mpCurrentCodeComponent = self.mpCodeNameValidate(codename, 7+offset);
		for code in self.mpCodeComponents:
			if code == self.mpCurrentCodeComponent:
				if code in self.mpDataComponents:
					self.mpDataComponents[code] = [];
				self.mpCodeComponents.remove(code);
				found =1;
		if found ==0:	
			self.screen.addstr("Error: Code does not exist");
		else:
			self.screen.addstr("Code deleted");


	def mpDataAdd(self, offset):
		self.screen.clear()
		self.screen.border(0)
		offset = self.mpAppDisp();
		self.mpCurrentDataHandle = self.get_param(self.screen, "Enter data handle for "+self.mpCurrentCodeComponent, offset)
		dataname = self.get_param(self.screen, "Enter data name for "+self.mpCurrentCodeComponent+" , handle "+self.mpCurrentDataHandle+". Use the fully qualified name, eg. data_utham_file_DemoInput", offset +2)
		self.mpCurrentDataName = self.mpDataNameValidate(dataname, offset+3);
		if self.mpCurrentDataName != "":
			self.mpDataComponents[self.mpCurrentCodeComponent].append((self.mpCurrentDataHandle, self.mpCurrentDataName));


	def mpDataDelete(self, offset):
		self.screen.clear()
		self.screen.border(0)
		offset = self.mpAppDisp();
		self.mpCurrentDataHandle = self.get_param(self.screen, "Enter data handle for "+self.mpCurrentCodeComponent, offset)
		for t in self.mpDataComponents[self.mpCurrentCodeComponent]:
			self.screen.addstr("Checking: "+t[0]+" "+t[1]+ " in "+self.mpCurrentCodeComponent);
			if self.mpCurrentDataHandle == t[0]:
				self.screen.addstr("Data deleted");
				self.mpDataComponents[self.mpCurrentCodeComponent].remove(t);
			else:
				self.screen.addstr("Error: Data does not exist for "+self.mpCurrentCodeComponent);
			
	#No mpDataModify()

	def mpAppDisp(self):
		appname =self.mpAppName;
		self.screen.addstr(2, 2, "Mathpak App file generator");
		self.screen.addstr(4, 2, "<"+appname+">");
		i=0;
		for code in self.mpCodeComponents:
			codename="\t<"+code+">";
			self.screen.addstr(5+i, 4, codename);
			i = i+1;
			for data in self.mpDataComponents[code]:
				dataline= "\t\t<"+data[0]+" handle=\""+data[0]+"\" data=\""+data[1]+"\">";
				dataline2= "\t\t</"+data[0]+">";
				self.screen.addstr(5+i, 4, dataline);
				i = i+1;
				self.screen.addstr(5+i, 4, dataline2);
				i = i+1;
			self.screen.addstr(5+i, 4, "\t</"+code+">");
			i = i+1;
		self.screen.addstr(5+i, 2, "</"+appname+">");
		i=i+1;
		
		#self.screen.addstr(7+i, 4, "Current code component:"+self.mpCurrentCodeComponent);
		#self.screen.addstr(8+i, 4, "Current data handle: "+self.mpCurrentDataHandle);
		#self.screen.addstr(9+i, 4, "Curent data name: "+self.mpCurrentDataName);
		return (7+i);

	def mpAppFileGen(self):
		fields = self.mpAppName.split("_");
		stagingdir = os.environ.get('MATHPAK_STAGING')
		dir = stagingdir+"/"+ fields[0]+"/"+fields[1]+"/"+fields[2];
		cmdstring = "mkdir -p "+dir;
		a = system(cmdstring)
		fullname =self.mpAppName+".xml";
		f = file(dir+"/"+fullname, 'w');
		content = "<"+self.mpAppName+">\n";
		for code in self.mpCodeComponents:
			codename="\t<"+code+">\n";
			content+=codename;
			for data in self.mpDataComponents[code]:
				dataline= "\t\t<"+data[0]+" handle=\""+data[0]+"\" data=\""+data[1]+"\">\n";
				dataline2= "\t\t</"+data[0]+">\n";
				content += dataline;
				content += dataline2;
			content+= "\t</"+code+">\n";
		content+="</"+self.mpAppName+">\n";
		f.write(content);
		f.close();	
	
	def mpTemplateGen(self, cdir, component, name, ext):
		stagingdir = os.environ.get('MATHPAK_STAGING')
		fr = file(stagingdir+"/tools/templates/TemplateCode."+ext, 'r');
		fw = file(cdir+"/"+name+"."+ext, 'w');
		data=[];
		tdata = fr.readlines();
		print("Writing code file "+name+"."+ext);
		for line in tdata:
			print(line);
			line = line.replace("MATHPAKCOMPONENT", component);
			line = line.replace("MATHPAKFUNCTION", name);
			line = line.replace("MATHPAKAPP", self.mpAppName);
			fw.write(line);

	def mpGenDir(self, component, app):
		stagingdir = os.environ.get('MATHPAK_STAGING')
		fields = component.split("_");
		if fields[0] == "app":
			self.mpAppFileGen();
		elif fields[0] == "code":
			name = fields[3];
			cdir = stagingdir+"/"+ fields[0]+"/"+fields[2]+"/"+fields[1]+"/"+fields[3];
			cmdstring = "mkdir -p "+cdir;
			a = system(cmdstring)
			print("Generating code file"+cmdstring);
			if fields[1] == "visual":
				self.mpTemplateGen(cdir, component, name, "html");
				self.mpTemplateGen(cdir, component, name, "css");
				self.mpTemplateGen(cdir, component, name, "js");
			else:
				self.mpTemplateGen(cdir, component, name, "py");
				self.mpTemplateGen(cdir, component, name, "R");
		elif fields[0] == "data":
			name = fields[3];
			dir = stagingdir+"/"+fields[0]+"/"+fields[2]+"/"+fields[1]+"/"+fields[3];
			cmdstring = "mkdir -p "+dir;
			a = system(cmdstring)
			print("Generating data file"+cmdstring);
			cmdstring = "touch "+dir+"/"+name+".data";
			a = system(cmdstring)
			print("Generating data file"+cmdstring);

	def mpAppDirGen(self):
		self.mpGenDir(self.mpAppName, self.mpAppName);
		for code in self.mpCodeComponents:
			self.mpGenDir(code, self.mpAppName);
			for data in self.mpDataComponents[code]:
				self.mpGenDir(data[1], self.mpAppName);
		return;
	
	
	def mpAppFileLoad(self):
		self.screen.clear()
		self.screen.border(0)
		offset = self.mpAppDisp();
		self.mpAppName = self.get_param(self.screen, "Enter app name. Use the fully qualified name, e.g. app_utham_Demo", offset)
		args = self.mpAppName.split("_");
		user = args[1];
		name = args[2];
		file ="./app/"+user+"/"+name+"/"+self.mpAppName+".xml";
		self.screen.addstr("Loading file "+file);
		
		#Traverse XML file
		data = {};
		tree = ET.parse(file)
		root = tree.getroot();
		for c in root:
			code = c.tag;
			self.mpCurrentCodeComponent = code;
			self.mpCodeComponents.append(self.mpCurrentCodeComponent);
			self.mpDataComponents[self.mpCurrentCodeComponent] = [];
			for s in c:
				if 'data' in s.attrib.keys():
					d = s.attrib['data'];
					h = s.attrib['handle'];
					self.mpDataComponents[self.mpCurrentCodeComponent].append((h, d));

def main(stdscr):
	ms = MathpakAppGen(stdscr);
	ms.mpMain();



if  not 'MATHPAK_STAGING' in os.environ.keys():
	print "Error: MATHPAK_STAGING not set.";
	exit();
wrapper(main)
