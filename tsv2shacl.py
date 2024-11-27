"""Module containing methods to generate
   SHACL shapes from dataverse based metadata tsv files
"""
import sys
import glob
from datetime import datetime
import pandas as pd
from unidecode import unidecode

help = """
Usage: python tsv2shacl.py <file.tsv>
       (runs script for specified tsv file)
   or:
       python tsv2shacl.py --all
       (runs script for all tsv files in current directory)
   or:
       python tsv2shacl --help
       (prints this help page)
"""
def tsv2shacl(infile=None):
    if not infile:
        infile = input('Enter name of tsv file: ')
    try:
        # read tsv data
        with open(infile,'r') as fid:
            md_df = pd.read_csv(infile, sep='\t')
        
        # identify row index for metadata fields and controlled vocabulary
        indxDS = md_df.index[md_df['#metadataBlock']=='#datasetField'].tolist()[0]
        indxCV = md_df.index[md_df['#metadataBlock']=='#controlledVocabulary'].tolist()[0]
        indxEnd = md_df.shape[0]
        ## DEBUG
        #print(indxDS)
        #print(indxCV)
        #print(indxEnd)
        ## DEBUG
        outfile = md_df.name[0] + '_shape.ttl'
        time = datetime.now()
        print('The shapes are written to ' + outfile)
        with open(outfile,'w') as fid:
            fid.write('@prefix dcterms: <http://purl.org/dc/terms/> .' + "\n")
            fid.write('@prefix m4i: <http://w3id.org/nfdi4ing/metadata4ing#> .' + "\n")
            fid.write('@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .' + "\n")
            fid.write('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .' + "\n")
            fid.write('@prefix schema: <http://schema.org/> .' + "\n")
            fid.write('@prefix sh: <http://www.w3.org/ns/shacl#> .' + "\n")
            fid.write('@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .' + "\n")
            fid.write('@prefix aps: <https://w3id.org/nfdi4ing/profiles/> .' + "\n")
            fid.write('@prefix darus: <https://darus.uni-stuttgart.de/> .' + "\n")

            fid.write('darus:shapes/' 
                      + md_df.name[ii] 
                      + ' dcterms:created "' 
                      +  time.strftime("%Y-%M-%D") + '"^^xsd:date ;' 
                      + " \n")
            fid.write("	dcterms:license <http://spdx.org/licenses/CC0-1.0> ;\n")
            fid.write(f'	dcterms:title  "DaRUS metadata schema for {md_df.name[ii]} "' + ";\n")
            fid.write('	a rdfs:Class, sh:NodeShape ;' + "\n")




            for ii in range(0,indxDS):
                fid.write('metadatablock.name=' + md_df.name[ii] + '\n')
                fid.write('metadatablock.displayName=' + md_df.displayName[ii] + '\n')
            for ii in range(indxDS+1,indxCV):
                fid.write('datasetfieldtype.' + md_df.name[ii] + '.title=' + md_df.dataverseAlias[ii] + '\n')
                fid.write('datasetfieldtype.' + md_df.name[ii] + '.description=' + md_df.displayName[ii] + '\n')
                if str(md_df.blockURI[ii]) != 'nan':
                    fid.write('datasetfieldtype.' + md_df.name[ii] + '.watermark=' + str(md_df.blockURI[ii]) + '\n')
                else:
                    fid.write('datasetfieldtype.' + md_df.name[ii] + '.watermark=\n')
            for ii in range(indxCV+1,indxEnd):
                displayName = md_df.dataverseAlias[ii].replace(" ","_")
                displayName = unidecode(displayName)
                fid.write('controlledvocabulary.' + md_df.name[ii] + '.' 
                        + displayName.lower() + '=' + md_df.dataverseAlias[ii] + '\n')
    except FileNotFoundError:
        raise SystemExit("File does not exist")

def main():
    try:
        arg = sys.argv[1]
        if arg == '--help':
            exit(help)
        
        print("This script generates shacl shapes from metadata tsv")
        if arg == '--all':
            filelist = [f for f in glob.glob("*.tsv")]
            for f in filelist:
                tsv2dshacl(infile=f)
            exit
        
        tsv2shacl(infile = arg)
    
    except IndexError:
        raise SystemExit(help)        

if __name__ == '__main__':
    main()
