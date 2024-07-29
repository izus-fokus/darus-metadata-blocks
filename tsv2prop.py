"""Module containing methods to generate
   properties from custom metadata tsv
"""
import sys
import glob
import pandas as pd
from unidecode import unidecode

help = """
Usage: python tsv2prop.py <file.tsv>
       (runs script for specified tsv file)
   or:
       python tsv2prop.py --all
       (runs script for all tsv files in current directory)
   or:
       python tsv2prop --help
       (prints this help page)
"""

def tsv2prop(infile=None):
    if not infile:
        infile = input('Enter name of tsv file: ')
    try:
        # read tsv data
        with open(infile,'r') as fid:
            md_df = pd.read_csv(infile, sep='\t')
        
        # convert and write out to properties file
        indxDS = md_df.index[md_df['#metadataBlock']=='#datasetField'].tolist()[0]
        indxCV = md_df.index[md_df['#metadataBlock']=='#controlledVocabulary'].tolist()[0]
        indxEnd = md_df.shape[0]
        ## DEBUG
        #print(indxDS)
        #print(indxCV)
        #print(indxEnd)
        ## DEBUG
        outfile = md_df.name[0] + '.properties'
        print('The properties are written to ' + outfile)
        with open(outfile,'w') as fid:
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
        
        print("This script generates properties files from custom metadata tsv")
        if arg == '--all':
            filelist = [f for f in glob.glob("*.tsv")]
            for f in filelist:
                tsv2prop(infile=f)
            exit
        
        tsv2prop(infile = arg)
    
    except IndexError:
        raise SystemExit(help)        

if __name__ == '__main__':
    main()
