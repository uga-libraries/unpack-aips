# unpack-aips
 Scripts that extract the contents of compressed AIP files.

## unpack-aips.py
**AIP Unpacker:** This script identifies all of the AIPs in a directory, unpacks their contents, and moves the files into top-level folders named with the AIP ID. 

unpack-aips.py iterates through a directory and identifies tarred and zipped AIPs (.tar.bz2 files). For each one, it unpacks the contents of the objects folder into a new, top-level directory with the AIP number, then deletes the bag metadata. It leaves the compressed AIP files in place so that the script can be run again and the files re-extracted if needed. The script will skip AIPs that have already been unpacked, which it identifies by an existing top-level folder with the AIP ID.

Script usage: python /path/to/script /path/to/aipdirectory
