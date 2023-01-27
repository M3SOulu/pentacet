import pandas as pd
import langid


#inp_csv_file = 'repos_meta_30k_updated.csv'
inp_csv_file = 'repos_list_with_desc_2020_01_till_2023_01.csv'
url_part = 'https://github.com/'


with open(inp_csv_file, encoding="utf-8") as f:
    lines = f.readlines()

cntr=0
proj_url = []
desc = []
nl_catg = []
for line in lines:
    contents = line.split(',')
    #proj_url.append(contents[4])
    if contents[1] is not None and len(contents[1]) > 1:
        print("processing url", url_part + contents[1])
        proj_url.append(url_part + contents[1])
        proj_desc = ','.join(contents[2:]).rstrip()
        proj_desc = proj_desc.replace("None", "no_description")
        nl_catg.append(langid.classify(proj_desc)[0])
        desc.append(proj_desc)

final_df = pd.DataFrame(list(zip(proj_url, desc, nl_catg)))
#final_df.to_csv("repos_desc_with_natural_lang_catg.tsv", header=None, sep="\t", index=False)
final_df.to_csv("repos_desc_with_natural_lang_catg_v2.tsv", header=None, sep="\t", index=False)
