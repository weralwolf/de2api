#!/bin/bash

#wget http://dev.weralwolf.com/lab28/de2_samples.tar.gz
#tar xvzf de2_samples.tar.gz

# Update documentation
original=`pwd`

ng_doc=$original/neutral_gas_wats/doc
rm -rf $ng_doc
mkdir $ng_doc
cd $ng_doc

wget ftp://nssdcftp.gsfc.nasa.gov/miscellaneous/documents/b47611.txt
wget ftp://nssdcftp.gsfc.nasa.gov/miscellaneous/documents/b47607.txt
wget ftp://nssdcftp.gsfc.nasa.gov/miscellaneous/documents/b47612.txt
wget ftp://nssdcftp.gsfc.nasa.gov/miscellaneous/documents/b47608.txt
wget ftp://nssdcftp.gsfc.nasa.gov/miscellaneous/documents/b47613.for
wget ftp://nssdcftp.gsfc.nasa.gov/miscellaneous/documents/b47609.for
wget ftp://nssdcftp.gsfc.nasa.gov/miscellaneous/documents/b47610.for

pl_doc=$original/highres_vmsbin/doc
rm -rf $pl_doc
mkdir $pl_doc
cd $pl_doc

wget ftp://nssdcftp.gsfc.nasa.gov/miscellaneous/documents/b46550.txt
wget ftp://nssdcftp.gsfc.nasa.gov/miscellaneous/documents/b46551.txt
wget ftp://nssdcftp.gsfc.nasa.gov/miscellaneous/documents/b46549.txt
wget ftp://nssdcftp.gsfc.nasa.gov/miscellaneous/documents/b46589.txt
wget ftp://nssdcftp.gsfc.nasa.gov/miscellaneous/documents/b46552.txt

cpnu_doc=$original/combined_plasma_neutrals_ua/doc
rm -rf $cpnu_doc
mkdir $cpnu_doc
cd $cpnu_doc

wget ftp://nssdcftp.gsfc.nasa.gov/miscellaneous/documents/b46570.txt
wget ftp://nssdcftp.gsfc.nasa.gov/miscellaneous/documents/b47932.txt
wget ftp://nssdcftp.gsfc.nasa.gov/miscellaneous/documents/b47931.txt
wget ftp://nssdcftp.gsfc.nasa.gov/miscellaneous/documents/b46569.txt