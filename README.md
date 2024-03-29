# PENTACET
## _A large Curated Contextual Code Comments per Contributor and SATD data_

PENTACET (or 5C - Curated Contextual Code Comments data per Contributor and SATD) dataset contains contextual code comments of 9096 OSS Java repositories. The OSS repositories are identified using a well-defined curation rules that include multiple filtering criteria to exclude non-maintenance, academic repositories and to get active repositories after filtering non-licensed, archived and non-english repositories based on the description text.  The mined comments are then treated for noise removal such as comment symbols '//','/\*\*','\*/','\#\#\#', '----',\*\*\*\*'. Upon noise removal, the empty or blank comments are identified as 'INVALID'. Further, the remaining comments are classified into either 'NL' (Natural Language) or *Not'. The identified natural language comments are then fed through an iterative semi-automated labeling process, to detect 'Hard to Find' SATD features such as 'went horribly wrong', 'not sure if this will work', etc.,. As a result, PENTACET contains more than 16 million contextual natural language source code comments with more than 500,000 SATD comments.

The dataset is stored in a PostGRESQL DB dump file. 


Important tools involved in PENTACET data construction:
| Tool | README |
| ------ | ------ |
| SoCCMiner | [M3SOulu/soccminer#readme][PlDb] |
| NLoN | [M3SOulu/NLoN#readme][PlGh] |
| Sense2Vec | [explosion/sense2Vec#readme][PS2v] |
| langid | [saffsd/langid#readme][PELI] |

## 500000 SATD FILE
For convenience, the 500,000+ SATD comments are stored in a separate TSV (tab separated) file along with comment_id.
[500000_SATD_FILE][dill]

## PENTACET DB DUMP
[raw_soccminer_mined_data_and_db_dump][dill]

### DB DUMP LOADING STEPS 
 #### For Windows:
1.  Open PGADMIN4 and connect to the PostgreSQL server (localhost or any other server)	
2.	Create a dummy database (name same as dataset – pentacet)
3.	Set the binary path at File -> Preferences -> Paths -> Binary paths (Choose the bin folder from the location were postgres is installed)
4.	Set the binary path from step 3 as default and save it.
5.	In the next window, at left pane choose the dummy database that was created in step 2 and right click and choose restore
6.	Choose the 'pentacet_clean_and_load_dump.sql' file from local download directory or where ever it is saved – This starts the restoration process and the DB will be restored for use within 30-40 minutes in system equipped with 16 GB RAM.

 #### For Linux based systems:
 #####
 Restore using plain sql
 ```sh
 psql -U username -f /location/pentacet_plain_sql_dump.sql
 ```
 
 #####
 Restore using pg_dump blob
 ```sh
 pg_restore -C -d pentacet /location/pentacet_clean_and_load_dump.sql
 ```

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://zenodo.org/record/7757462#.ZCW08fZBxPY>

   [PlDb]: <https://github.com/M3SOulu/soccminer#readme>
   [PlGh]: <https://github.com/M3SOulu/NLoN#readme>
   [PS2v]: <https://github.com/explosion/sense2vec#readme>
   [PELI]: <https://github.com/saffsd/langid.py#readme>
   
