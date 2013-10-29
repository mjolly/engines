<?php
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


function MATHPAKFUNCTION_getproperties() {
	$properties['version'] = "0.0.1";
	return $properties;
}


#main
function MATHPAKFUNCTION($inputnames, $inputdata, $outputnames, $outputdata){

}


$stagingdir = getenv("MATHPAK_STAGING");

$inc =$stagingdir."/engines/php/MathpakEngineIOFile.php";
include ($inc);
$inc =$stagingdir."/engines/php/MathpakEngineWorkFlow.php";
include ($inc);
$inc =$stagingdir."/engines/php/MathpakDataStoreFile.php";
include ($inc);
$inc =$stagingdir."/engines/php/MathpakEngine.php";
include ($inc);

#main
$app=$argv[1];
$component="MATHPAKFUNCTION";
$e = new MathpakEngine($component, $app);
$e->engineOpen();
$io = $e->io;
MATHPAKFUNCTION($io->inputnames, $io->inputdata, $io->outputnames, &$io->outputdata);
$e->engineClose();









?>
