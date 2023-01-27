import pandas as pd


all_valid_repos_contributors_df = pd.read_csv('_repos_after_lang_empty_desc_license_educ_non_maint_desc_name_filtered_repo_attributes_filtered_v2_contributors_out.csv', header=None)
all_error_repos_contributors_df = pd.read_csv('_repos_after_lang_empty_desc_license_educ_non_maint_desc_name_filtered_repo_attributes_filtered_v2_contributors_err.csv', header=None)


all_repos_contributors_dict = {}

repos_catg_dict = {'LOW_TO_NO':[], 'ONE_CONTRIBUTOR':[], 'MORE_THAN_ONE_CONTRIBUTOR':[]}

for index, row in all_valid_repos_contributors_df.iterrows():
    if '|' in row[1]:
        all_repos_contributors_dict[row[0]] = row[1].split('|')
        repos_catg_dict['MORE_THAN_ONE_CONTRIBUTOR'].append(row[0])
    else:
        all_repos_contributors_dict[row[0]] = [row[1]]
        repos_catg_dict['ONE_CONTRIBUTOR'].append(row[0])

for index, row in all_error_repos_contributors_df.iterrows():
    all_repos_contributors_dict[row[0]] = [0]
    repos_catg_dict['LOW_TO_NO'].append(row[0])

print("Total repositories: ", len(all_repos_contributors_dict))
print("Repositories with more than one active contributors: ", len(repos_catg_dict['MORE_THAN_ONE_CONTRIBUTOR']))
print("Repositories with one active contributor: ", len(repos_catg_dict['ONE_CONTRIBUTOR']))
print("Repositories with little to no activity or removed repositories: ", len(repos_catg_dict['LOW_TO_NO']))

contrib_split_dict = {}
contrib_1_dict = []
contrib_2_3_dict = []
contrib_4_to_10_dict = []
contrib_greater_than_11_dict = []

for repos in repos_catg_dict['ONE_CONTRIBUTOR']:
    contrib_1_dict.append(repos)

for repos in repos_catg_dict['MORE_THAN_ONE_CONTRIBUTOR']:
    contrib_len = len(all_repos_contributors_dict[repos])
    if contrib_len not in contrib_split_dict:
        contrib_split_dict[contrib_len] = 1
    else:
        contrib_split_dict[contrib_len] = contrib_split_dict[contrib_len] + 1

    if contrib_len <= 3:
        contrib_2_3_dict.append(repos)
    elif contrib_len > 3 and contrib_len <= 10:
        contrib_4_to_10_dict.append(repos)
    else:
        contrib_greater_than_11_dict.append(repos)

for contrib_catg in sorted(contrib_split_dict.keys()):
    print(contrib_catg, contrib_split_dict[contrib_catg])

all_filtered_repos = []

for repos in contrib_1_dict:
    #print(repos)
    all_filtered_repos.append(repos)

for repos in contrib_2_3_dict:
    #print(repos)
    all_filtered_repos.append(repos)

for repos in contrib_4_to_10_dict:
    #print(repos)
    all_filtered_repos.append(repos)

for repos in contrib_greater_than_11_dict:
    #print(repos)
    all_filtered_repos.append(repos)


all_df = pd.DataFrame(all_filtered_repos)
all_df.to_csv("_all_filtered_repos_contributors_v2.csv", index=False, header=None)

contrib_1_df = pd.DataFrame(contrib_1_dict)
contrib_1_df.to_csv("_filtered_repos_1_contributor_v2.csv", index=False, header=None)

contrib_2_3_df = pd.DataFrame(contrib_2_3_dict)
contrib_2_3_df.to_csv("_filtered_repos_2_3_contributor_v2.csv", index=False,header=None)

contrib_4_10_df = pd.DataFrame(contrib_4_to_10_dict)
contrib_4_10_df.to_csv("_filtered_repos_4_10_contributor_v2.csv", index=False, header=None)

contrib_great_11_df = pd.DataFrame(contrib_greater_than_11_dict)
contrib_great_11_df.to_csv("_filtered_repos_greater_than_10_contributor_v2.csv", index=False, header=None)

print("Total 1 contrib all repos: ", len(contrib_1_dict))
print("Total 2 to 3 contrib all repos: ", len(contrib_2_3_dict))
print("Total 4 to 10 contrib all repos: ", len(contrib_4_to_10_dict))
print("Total greater than 10 contrib all repos: ", len(contrib_greater_than_11_dict))
