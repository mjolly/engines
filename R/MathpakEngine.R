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

mpdata <- list();
mpstagingdir <-"";
mpapp <- "";
mpInit <-function()  {
	stagingdir <<- Sys.getenv(c("MATHPAK_STAGING"));
	cmdargs <- commandArgs();
	mpapp <<- cmdargs[6];

	cat("Staging directory: ", stagingdir, "\n");
	cat("App:", mpapp, "\n");
	cat("Code:", mpcomponent, "\n");
	engineDataNamesGet();
	cat("Data:");
	print(mpdata);
}

mpRead <- function (handle, records=0) {
	engineRead(handle, records);
}

mpWrite <- function( handle, value, mode) {
	engineWrite(handle, value, mode);
}

mpOpen <- function (handle, mode) {
	engineOpen(handle, mode);
}

mpClose <- function (handle) {
	engineClose(handle);
}
