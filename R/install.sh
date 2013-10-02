rm -rf mathpak
Rscript package.R
rm -rf mathpak/man
R CMD build mathpak
R CMD INSTALL mathpak
