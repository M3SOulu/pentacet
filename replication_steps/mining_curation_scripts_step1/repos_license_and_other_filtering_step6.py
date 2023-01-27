
def parse_repo_meta(repo):
    to_be_proc_meta_info_dict = {}
    to_be_proc_meta_info_dict['repo_url'] = repo.split(',')[4]
    to_be_proc_meta_info_dict['repo_is_archived'] = repo.split(',')[5]
    to_be_proc_meta_info_dict['repo_is_disabled'] = repo.split(',')[6]
    to_be_proc_meta_info_dict['repo_is_fork'] = repo.split(',')[7]
    to_be_proc_meta_info_dict['repo_is_locked'] = repo.split(',')[8]
    to_be_proc_meta_info_dict['repo_is_mirror'] = repo.split(',')[9]
    to_be_proc_meta_info_dict['repo_is_private'] = repo.split(',')[10]
    to_be_proc_meta_info_dict['repo_license'] = repo.split(',')[13]
    to_be_proc_meta_info_dict['repo_topics'] = repo.split(',')[14]
    return to_be_proc_meta_info_dict


if __name__ == '__main__':
    proj_cntr = 0
    result_set = []

    inp_file_30k = 'lang_and_empty_desc_filtered_repos_30k.txt'
    inp_file_1k = 'master_1k_repos_no_desc_filtered.csv'

    inp_30k_meta_file = 'repos_meta_30k_updated.csv'
    inp_1k_meta_file = "master_1k_repos_meta.csv"
    repos_to_be_proc_dict = {}
    invalid_repos = []

    with open(inp_file_30k, encoding="utf-8") as f:
        repos_30k_list = f.readlines()

    with open(inp_file_1k, encoding="utf-8") as f:
        repos_1k_list = f.readlines()

    for repo in repos_1k_list:
        repos_to_be_proc_dict[repo.strip()] = None

    for repo in repos_30k_list:
        repos_to_be_proc_dict[repo.strip()] = None

    print("total repos in 30k file ", len(repos_30k_list))
    print("total repos in 1k file ", len(repos_1k_list))
    print("to be processed repos: ", len(repos_to_be_proc_dict))

    #exit(1)

    with open(inp_1k_meta_file, encoding="utf-8") as fh:
        repos_1k_meta = fh.readlines()

    for repo in repos_1k_meta:
        repo = repo.strip()
        if repo.split(',')[4] in repos_to_be_proc_dict:
            repos_to_be_proc_dict[repo.split(',')[4]] = parse_repo_meta(repo)
        else:
            invalid_repos.append(repo.split(',')[4])

    with open(inp_30k_meta_file, encoding="utf-8") as fh:
        repos_30k_meta = fh.readlines()

    for repo in repos_30k_meta:
        repo = repo.strip()
        if repo.split(',')[4] in repos_to_be_proc_dict:
            repos_to_be_proc_dict[repo.split(',')[4]] = parse_repo_meta(repo)
            #print(repos_to_be_proc_dict[repo.split(',')[4]]['repo_url'])
            #print(repos_to_be_proc_dict[repo.split(',')[4]]['repo_is_private'])
            #print(repos_to_be_proc_dict[repo.split(',')[4]]['repo_license'])
            #print(repos_to_be_proc_dict[repo.split(',')[4]]['repo_topics'])
        else:
            invalid_repos.append(repo.split(',')[4])

    archived_repos = {}
    disabled_repos = {}
    locked_repos = {}
    private_repos = {}
    no_license_repos = {}
    no_topics_repos = {}
    repo_topics = {}

    for repo in repos_to_be_proc_dict:
        if repos_to_be_proc_dict[repo]['repo_is_archived'] != "False":
            archived_repos[repo] = repo

        if repos_to_be_proc_dict[repo]['repo_is_disabled'] != "False":
            disabled_repos[repo] = repo

        if repos_to_be_proc_dict[repo]['repo_is_locked'] != "False":
            locked_repos[repo] = repo

        if repos_to_be_proc_dict[repo]['repo_is_private'] != "False":
            private_repos[repo] = repo

        if repos_to_be_proc_dict[repo]['repo_license'] == "no_assigned_license":
            no_license_repos[repo] = repo

        if repos_to_be_proc_dict[repo]['repo_topics'] == "no_existing_topic":
            no_topics_repos[repo] = repo

    print("Total repos processed: ", len(repos_to_be_proc_dict))
    print("Total archived_repos: ", len(archived_repos))
    print("Total disabled_repos: ", len(disabled_repos))
    print("Total locked_repos: ", len(locked_repos))
    print("Total private_repos: ", len(private_repos))
    print("Total repos_without_license: ", len(no_license_repos))
    print("Total repos_without_topics: ", len(no_topics_repos))

    with open('a_main_repos_lang_desc_license_filtered.csv', 'w', encoding="utf-8") as fi:
        for proj in repos_to_be_proc_dict:
            if proj not in archived_repos and proj not in disabled_repos and proj not in locked_repos and proj not in private_repos and proj not in no_license_repos:
                fi.write(proj + '\n')

    with open('a_lang_desc_filtered_repos_without_license.csv', 'w', encoding="utf-8") as fi:
        for proj in no_license_repos:
            fi.write(proj + '\n')

    with open('a_lang_desc_filtered_repos_archived.csv', 'w', encoding="utf-8") as fi:
        for proj in archived_repos:
            fi.write(proj + '\n')