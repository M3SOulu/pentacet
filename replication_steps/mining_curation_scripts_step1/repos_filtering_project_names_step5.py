import pandas as pd
import re

patterns = ['example','demo','sample','algorithm','quickstart','patterns','packtpublishing','learn-java-asm','linkedinlearning','hello-streams',
            'helloiot','-old','teaching','howto','template','mock']


def check_proj_name(proj_name):
    matching_stat = False
    for pattern in patterns:
        if re.search(pattern, proj_name.lower()):
            return True
        elif re.search("workshop\Z", proj_name.lower()) or re.search("basics\Z", proj_name.lower()) or re.search("-old\Z", proj_name.lower()):
            return True

    return matching_stat

educ_non_maint_repos_df = pd.read_csv('all_repos_after_lang_empty_desc_license_filtering_contributors_educ_non_maint_repos_desc.csv', header=None)

educ_non_maint_clean_repos = {}
total_repos_without_name_filtering = 0
repos_after_name_filtering = 0

for index, row in educ_non_maint_repos_df.iterrows():
    educ_non_maint_clean_repos[row[0].strip()] = index

with open("_repos_to_download__after_lang_empty_desc_license_filtering_contributors_educ_non_maint_repos_desc_repos_name.csv","w",encoding="utf-8") as fi:
    for proj in educ_non_maint_clean_repos:
        total_repos_without_name_filtering += 1
        proj_name_with_org = proj.split("https://github.com/")[1]
        if check_proj_name(proj_name_with_org):
            print(proj_name_with_org)
            repos_after_name_filtering += 1
        else:
            fi.write(proj + "\n")


print("Total repositories before name filtering: ", total_repos_without_name_filtering)
print("Filtered repositories: ", repos_after_name_filtering)
print("Total repositories after name filtering: ", total_repos_without_name_filtering - repos_after_name_filtering)

