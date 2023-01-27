# PENTACET
## _A large Curated Contextual Code Comments and SATD data_

PENTACET (or 5C - Curated Contextual Code Comments data per Contributor and Technical Debt) dataset contains contextual code comments of 9096 OSS Java repositories. The OSS repositories are identified using a well-defined curation rules that include multiple filtering criteria to exclude non-maintenance, academic repositories and to get active repositories after filtering non-licensed, archived and non-english repositories based on the description text.  The mined comments are then treated for noise removal such as comment symbols '//','/\*\*','\*/','\#\#\#', '----',\*\*\*\*'. Upon noise removal, the empty or blank comments are identified as 'INVALID'. Further, the remaining comments are classified into either 'NL' (Natural Language) or *Not'. The identified natural language comments are then fed through an iterative semi-automated labeling process, to detect 'Hard to Find' SATD features such as 'went horribly wrong', 'not sure if this will work', etc.,. As a result, PENTACET contains more than 16 million contextual natural language source code comments with more than 500,000 SATD comments.

The dataset is stored in a PostGRESQL DB dumb file. 


Important tools involved in PENTACET data construction:
| Tools     | README                      |
| ----------|---------------------------- |
| SoCCMiner | [M3SOulu/soccminer#readme][PlDb] |
| NLoN      | [M3SOulu/NLoN#readme][PlGh] |

PENTACET DB DUMP
[raw_soccminer_mined_data_and_db_dump][dill]


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://unioulu-my.sharepoint.com/:f:/g/personal/msridhar20_univ_yo_oulu_fi/EmINC-0m1qBKjXs7mVn8otQBCAVDfefmCPIiP7d9FO3bTA?e=UBf1NWr>

   [PlDb]: <https://github.com/M3SOulu/soccminer#readme>
   [PlGh]: <https://github.com/M3SOulu/NLoN#readme>
   
