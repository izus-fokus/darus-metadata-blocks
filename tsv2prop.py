"""Module containing methods to generate
   properties from custom metadata tsv
"""
import pandas as pd

print("This script generates properties from custom metadata tsv")

def tsv2prop():
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
        outfile = infile.split('.')[0] + '.properties'
        print(outfile)
        with open(outfile,'w') as fid:
            for ii in range(0,indxDS):
                fid.write('metadatablock.name=' + md_df.name[ii] + '\n')
                fid.write('metadatablock.displayName=' + md_df.displayName[ii] + '\n')
            for ii in range(indxDS+1,indxCV):
                fid.write('datasetfieldtype.' + md_df.name[ii] + '.title=' + md_df.dataverseAlias[ii] + '\n')
                fid.write('datasetfieldtype.' + md_df.name[ii] + '.description=' + md_df.dataverseAlias[ii] + '\n')
                fid.write('datasetfieldtype.' + md_df.name[ii] + '.watermark=' + md_df.dataverseAlias[ii] + '\n')
            for ii in range(indxCV+1,indxEnd):
                fid.write('controlledvocabulary.' + md_df.name[ii] + '.' 
                        + md_df.displayName[ii] + '=' + md_df.dataverseAlias[ii] + '\n')

    except FileNotFoundError:
        print("File does not exist") 
            
if __name__ == '__main__':
    tsv2prop()