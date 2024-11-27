"""Module containing methods to generate
   json schema shapes from dataverse based metadata tsv files
"""
import sys
import glob
from datetime import datetime
import pandas as pd
from unidecode import unidecode

help = """
Usage: python tsv2schema.py <file.tsv>
       (runs script for specified tsv file)
   or:
       python tsv2schema.py --all
       (runs script for all tsv files in current directory)
   or:
       python tsv2schema.py --help
       (prints this help page)
"""
def getJsonType(type):
    # maps dataverse types ("none", "date", "email", "text", "textbox", "url", "int", "float") 
    # to JSON schema types ("null", "boolean", "object", "array", "number", or "string")
    json_type = "null"
    if type is not None:
        match type:
            case "none":
                return "object"
            case "date" | "email" | "text" | "textbox" | "url":
                return "string"
            case "float":
                return "number"
            case "int":
                return "integer"
            case _:
                return json_type

def tsv2schema(infile=None):
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
        outfile = md_df.name[0] + '_schema.json'
        time = datetime.now()
        parent_open = False
        print('The schema is written to ' + outfile)
        with open(outfile,'w') as fid:
            fid.write('{' + "\n")
            fid.write('"$schema": "http://json-schema.org/draft-04/schema#",' + "\n")
            
            for ii in range(0,indxDS):
                fid.write(f'"$id": "https://darus.uni-stuttgart.de/{md_df.name[ii]}",' + "\n")
                fid.write(f'"title": "{md_df.displayName[ii]} metadata for a dataset",' + "\n")
            fid.write('"type": "object"' + "\n")
            fid.write('"properties": {' + "\n")

            for ii in range(indxDS+1,indxCV):
                name = md_df.name[ii]
                title = md_df.title[ii]
                description = md_df.description[ii]
                fieldtype = md_df.fieldType[ii]
                multiple = md_df.allowmultiples[ii]
                parent = md_df.parent[ii]
                hasCV = md_df.hasControlledVocabulary[ii]
                if fieldtype == "none": # is a parent field
                if parent == "FALSE":
                    if multiple == "FALSE":
                        fid.write(f'"{name}" : {{ "title": {title} "description": "{description}", "type": "{getJsonType(fieldtype)}"}} " + "\n")
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
            fid.write('}' + "\n")

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
