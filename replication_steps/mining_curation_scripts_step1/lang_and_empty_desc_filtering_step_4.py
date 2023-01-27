import pandas as pd

#inp_csv_file = 'repos_meta_30k_updated.csv'
#inp_tsv_file = 'repos_desc_with_natural_lang_catg.tsv'
inp_tsv_file = 'repos_desc_with_natural_lang_catg_v2.tsv'

repos_desc_df = pd.read_csv(inp_tsv_file, sep="\t", header=None)

repos_desc_dict = {}
repos_lang_dict = {}
unique_lang_dict = {}
repos_by_lang_dict = {}
no_desc_repos = {}

# language filtering through description
for index, row in repos_desc_df.iterrows():
    repos_lang_dict[row[0]] = row[2]
    repos_desc_dict[row[0]] = row[1]
    if row[1] == "no_description":
        no_desc_repos[row[0]] = row[1]

    if row[2] not in unique_lang_dict:
        unique_lang_dict[row[2]] = 1
    else:
        unique_lang_dict[row[2]] = unique_lang_dict[row[2]] + 1

    if row[2] not in repos_by_lang_dict:
        repos_by_lang_dict[row[2]] = [row[0]]
    else:
        repos_by_lang_dict[row[2]].append(row[0])

print("Total repositories: ", len(repos_lang_dict))
print("Unique languages mined (total): ", len(unique_lang_dict))
print("Unique languages are: ", list(unique_lang_dict.keys()))
print("No description/Empty description repos count: ", len(no_desc_repos.keys()))
total_repos = 0
for lang in unique_lang_dict:
    print("Language: {} has {} repos".format(lang, unique_lang_dict[lang]))
    total_repos += unique_lang_dict[lang]

#for lang in repos_by_lang_dict:
    #if lang in ["zh", "ko", "ja", "pt", "ru"]:
        #print(lang, len(repos_by_lang_dict[lang]))

#op_fh = open("lang_and_empty_desc_filtered_repos_30k.txt", mode="w", encoding="utf-8")
op_fh = open("lang_and_empty_desc_filtered_repos_v2.txt", mode="w", encoding="utf-8")
for repos in repos_lang_dict:
    #if repos_lang_dict[repos] not in ["zh", "ko", "ja", "pt", "ru"]:
    if repos_lang_dict[repos] in ["en"]:
        if repos not in no_desc_repos:
          op_fh.write(repos + "\n")
