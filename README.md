# darus-metadata-blocks
Customized metadata blocks of our Dataverse installation [DaRUS](https://darus.uni-stuttgart.de). 
The master branch represents the state of the production system,
the demodarus branch represents the state of the testing system (only available within University network).

If you want to change something, please make a pull request.

## Metadata customization
[See also dataverse documentation](https://guides.dataverse.org/en/5.9/admin/metadatacustomization.html)
and maybe corresponding [pull request](https://github.com/IQSS/dataverse/pull/5251).

`curl -s http://localhost:8080/api/admin/datasetfield/load -X POST --data-binary @mdblock-definition-file -H "Content-type: text/tab-separated-values"` 

where "mdblock-definition-file" is the name of a TSV format file, typically ending in the extension “.tsv” (by convention).

Getting fields of all schemas:

`curl http://localhost:8080/api/admin/index/solr/schema > fields.txt`

As a final step the fields of the schema.xml file (/usr/local/solr-7.3.0/server/solr/collection1/conf) have to be updated.
