
if __name__ == '__main__':
    invalid_url_counter = 0
    invalid_url_list = []
    all_proj_dict = {}
    proj_index = 0
    proj_cntr = 0
    result_set = []
    proj_commits = {}
    all_proj_name = {}
    req_reroute_proj_url = {}


    #inp_file = "_repos_1_contrib_after_lang_empty_desc_license_educ_non_maint_desc_name_filtering_contributors.csv"
    #inp_meta_file = "repos_meta_1.csv"
    inp_file = "_filtered_repos_greater_than_10_contributor_v2.csv"
    inp_meta_file = "repos_meta_greater_than_10_v2.csv"
    with open(inp_file, encoding="utf-8") as f:
        repos_list = f.readlines()

    for repo in repos_list:
        repo = repo.strip()
        proj_cntr += 1
        all_proj_dict[repo] = proj_cntr
        proj_nm = repo.split("https://github.com/")[1].split("/")[1]
        all_proj_name[proj_nm.lower()] = repo

    with open(inp_meta_file, encoding="utf-8") as f:
        repos_meta = f.readlines()

    for metadata in repos_meta:
        metadata = metadata.strip()
        proj_name = metadata.split(',')[4].split("https://github.com/")[1].split("/")[1].lower()
        #print(metadata)
        proj_url = metadata.split(',')[4]
        commits = metadata.split(',')[16]
        if proj_url in all_proj_dict:
            proj_commits[proj_url] = commits
        else:
            if proj_name in all_proj_name:
                proj_commits[all_proj_name[proj_name]] = commits
                req_reroute_proj_url[all_proj_name[proj_name]] = proj_url
            else:
                print("missing url: ", proj_url)
                invalid_url_counter += 1
                invalid_url_list.append(proj_url)

    print("Total repositories processed with single contributors : ", len(all_proj_dict))
    print("Total invalid repositories processed with contributors : ", len(invalid_url_list))
    print("Total valid repositories processed with contributors : ", len(proj_commits))
    print("Total rerouted urls: ", len(req_reroute_proj_url))
    for old_url in req_reroute_proj_url:
        print(old_url + " --> " + req_reroute_proj_url[old_url])

    print("Invalid URLs: ", invalid_url_list)
    proj_commits = {k: v for k, v in sorted(proj_commits.items(), key=lambda item: int(item[1]), reverse=True)}
    #for proj in proj_commits:
    #    print(proj, proj_commits[proj])
    with open('repos_meta_greater_than_10_by_commits_desc_v2.csv', 'w', encoding="utf-8") as fi:
        for proj in proj_commits:
            fi.write(proj + "," + proj_commits[proj] + '\n')






