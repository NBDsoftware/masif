#!/usr/bin/python
import Bio
from Bio.PDB import * 
import sys
import importlib
import os
import shutil

from default_config.masif_opts import masif_opts
# Local includes
from input_output.protonate import protonate

"""
Script based on /masif/source/data_preparation/00-pdb_download.py
Hard-coded configuration, change accordingly!"
"""

if len(sys.argv) <= 1: 
    print("Usage: "+sys.argv[0]+" PDBID_A_B")
    print("A or B are the chains to include in this pdb.")
    sys.exit(1)

if not os.path.exists(masif_opts['raw_pdb_dir']):
    os.makedirs(masif_opts['raw_pdb_dir'])

if not os.path.exists(masif_opts['tmp_dir']):
    os.mkdir(masif_opts['tmp_dir'])

in_fields = sys.argv[1].split('_')
pdb_id = in_fields[0]

pdb_in_file = masif_opts['in_pdb_dir']+"/"+pdb_id+".pdb"
if not os.path.exists(pdb_in_file):
    # Download pdb
    print ("DOWNLOAD PDB", pdb_id)
    pdbl = PDBList(server='http://ftp.wwpdb.org')
    pdb_filename = pdbl.retrieve_pdb_file(pdb_id, pdir=masif_opts['tmp_dir'],file_format='pdb')
else:
    print("MOVE PDB", pdb_id)
    pdb_filename = masif_opts['tmp_dir']+"/"+pdb_id+".pdb"
    shutil.move(pdb_in_file, pdb_filename)

print ("FILENAME: ", pdb_filename)
print ("IN_NAME:", pdb_in_file)

##### Protonate with reduce, if hydrogens included.
# - Always protonate as this is useful for charges. If necessary ignore hydrogens later.
protonated_file = masif_opts['raw_pdb_dir']+"/"+pdb_id+".pdb"
protonate(pdb_filename, protonated_file)
pdb_filename = protonated_file

