#!/usr/bin/python3
import logging
import os
import subprocess
import datetime
import traceback
import pandas as pd
import requests
import json
import time
import re

REPO_BASE_PATH = 'C:\\Users\\msridhar20\\for_pysoccer\\downloaded_repositories_1'
URL = 'https://api.github.com/graphql'
API_TOKEN = "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"  # "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"  # # generate your API token and replace it


def clone_repo(url, folder):
    ret_code = 1  # 1 for failure 0 for success
    try:
        os.chdir(folder)
        process = subprocess.Popen(['git', 'clone', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        msg, err = process.communicate()  # do not remove communicate, if removed process exits with None or Null returncode
        ret_code = process.returncode
    except Exception as pexcep:
        error_message = traceback.format_exc()
        print("Error occured with url: {}, ERROR: {}".format(url, error_message))
        return ret_code
    else:
        return ret_code


def is_empty_file(file_loc):
    # validate if file is empty
    return os.stat(file_loc).st_size == 0


def is_existing_file(file_loc):
    # validate if file exists
    return os.path.isfile(file_loc)


def download_repo_from_url(repo):
    """
    Accepts github repo url and clones the repo in local directory
    :param repo: contains the repo url of source code download to local dir
    :return: status code 1 indicates error with repo download, 0 indicates success
    """
    repo = repo.replace("\n", "")
    local_folder = repo.split("https://github.com/")
    local_folder = local_folder[-1].replace("/", "_")
    repo_url = repo + ".git"
    ret_code = None

    if not os.path.exists(REPO_BASE_PATH):
        os.makedirs(REPO_BASE_PATH)
    os.chdir(REPO_BASE_PATH)
    logging.debug("Validating if local directory exists for {} ".format(local_folder))
    if not os.path.isdir(os.path.join(REPO_BASE_PATH, local_folder)):
        logging.debug("Creating local directory as it does not exist for {} ".format(local_folder))
        os.mkdir(local_folder)

        try:
            # depth=1 for latest snapshot, remove it to fetch full repository
            ret_code = clone_repo(repo_url, local_folder)
        except subprocess.CalledProcessError as repo_downloader:
            logging.debug("Exception occurred while downloading repo {} ".format(repo_url))
            logging.debug("Error Occured".format(repo_downloader.returncode, repo_downloader.output))
            return 1
        except Exception as gen_error:
            return 1
        else:
            logging.debug("Completed repo download for repo {} with return code {}".format(repo, ret_code))
            return ret_code
    else:
        return 100  # for repos that already exist


def read_csv_and_process_download(inp_file):
    urls = {} # to hold non duplicate urls
    url_status = {'FAILED_URLS':[], 'PASSED_URLS':[], 'EXISTING_URLS':[]}
    if not is_existing_file(inp_file):
        print("Input CSV file {} does not exist or inaccessible".format(inp_file))
        return False
    elif is_empty_file(inp_file):
        print("Input CSV file {} is empty".format(inp_file))
        return False
    else:
        try:
            # csv header #sno	#project	#language	#url	#last_commit
            df = pd.read_csv(inp_file)
            processed_urls = 0
            duplicate_urls = 0
            existing_repos = 0
            for index, row in df.iterrows():
                if processed_urls == 1251:  # fetch only 1251 urls
                    break
                processed_urls += 1
                if row['url'] not in urls:
                    urls[row['url']] = processed_urls
                    logging.debug("Processing project with url {}".format(row['url']))
                    print("Processing for ", row['url'])
                    ret_code = download_repo_from_url(row['url'])
                    if ret_code == 0:
                        url_status['PASSED_URLS'].append(row['url'])
                    elif ret_code == 1 or ret_code is None:
                        url_status['FAILED_URLS'].append(row['url'])
                    elif ret_code == 100:
                        url_status['EXISTING_URLS'].append(row['url'])
                else:
                    duplicate_urls += 1
            print("Total processed urls: {}".format(processed_urls))
            print("Total duplicate urls: {}".format(duplicate_urls))
            print("Total successful repo downloads : {}".format(len(url_status['PASSED_URLS'])))
            print("Total failed repo downloads: {}".format(len(url_status['FAILED_URLS'])))
            print("Total existing repositories: {}".format(len(url_status['EXISTING_URLS'])))
        except Exception as ex:
            print("Unexpected error: {}".format(ex))
            return False
        else:
            return True


def validate_repo_url(repo_url):
    ret_stat = True
    try:
        r = requests.get(repo_url)
        if r.status_code != 200:
            print("Invalid URL: {} failed with return code {}".format(repo_url, r.status_code))
            ret_stat = False
            return ret_stat
        else:
            print("Valid Repo URL: {}".format(repo_url, r.status_code))
            return ret_stat
    except requests.exceptions.Timeout:
        print("URL: {} failed with timeout exception".format(repo_url))
        ret_stat = False
        return ret_stat
    except requests.exceptions.TooManyRedirects:
        print("URL: {} failed with too many redirect exception".format(repo_url))
        ret_stat = False
        return ret_stat
    except requests.exceptions.HTTPError as err:
        print("URL: {} failed with HTTP error {}".format(repo_url, err.strerror))
        ret_stat = False
        return ret_stat
    except requests.exceptions.RequestException as e:
        print("URL: {} failed with ambiguous exception {}".format(repo_url, e.strerror))
        ret_stat = False
        return ret_stat


def extract_data(data, proj_url):
    global result_set, invalid_url_counter, invalid_url_list
    topics = []
    commit_url = None
    commited_date = None
    license_info = "no_assigned_license"

    if 'errors' in data:
        for error_meta_dict in data['errors']:
            if 'type' in error_meta_dict:
                invalid_url_counter += 1
                invalid_url_list.append(proj_url)
                return

    if data['data']['repositoryOwner'] is None:
        invalid_url_counter += 1
        invalid_url_list.append(proj_url)
        return

    if data['data']['repositoryOwner']['repository']['repositoryTopics']['nodes'] is None:
        topics.append("no_existing_topic")
    else:
        for topic in data['data']['repositoryOwner']['repository']['repositoryTopics']['nodes']:
            topics.append(topic['topic']['name'])

    if len(topics) == 0:
        topics.append("no_existing_topic")

    if data['data']['repositoryOwner']['repository']['licenseInfo'] != None:
        license_info = data['data']['repositoryOwner']['repository']['licenseInfo']['name']

    description_text = None
    if data['data']['repositoryOwner']['repository']['description'] != None:
        description_text = data['data']['repositoryOwner']['repository']['description']
    else:
        description_text = 'no_description'

    for history_node in data['data']['repositoryOwner']['repository']['defaultBranchRef']['target']['history']['nodes']:
        commit_url = history_node['commitUrl']
        commited_date = history_node['committedDate']

    result_set.append(str(proj_index) + "," +
                      str(data['data']['repositoryOwner']['repository']['name']) + "," +
                      str(data['data']['repositoryOwner']['repository']['stargazers']['totalCount']) + "," +
                      str(data['data']['repositoryOwner']['repository']['forks']['totalCount']) + "," +
                      str(data['data']['repositoryOwner']['repository']['url']) + "," +
                      str(data['data']['repositoryOwner']['repository']['isArchived']) + "," +
                      str(data['data']['repositoryOwner']['repository']['isDisabled']) + "," +
                      str(data['data']['repositoryOwner']['repository']['isFork']) + "," +
                      str(data['data']['repositoryOwner']['repository']['isLocked']) + "," +
                      str(data['data']['repositoryOwner']['repository']['isMirror']) + "," +
                      str(data['data']['repositoryOwner']['repository']['isPrivate']) + "," +
                      str(data['data']['repositoryOwner']['repository']['visibility']) + "," +
                      str(data['data']['repositoryOwner']['repository']['updatedAt']) + "," +
                      str(license_info) + "," +
                      str('|'.join(topics)) + "," +
                      str(data['data']['repositoryOwner']['repository']['defaultBranchRef']['name']) + "," +
                      str(data['data']['repositoryOwner']['repository']['defaultBranchRef']['target']['history']['totalCount']) + "," +
                      str(commit_url) + "," +
                      str(commited_date) + "," +
                      str(description_text))


def get_query(owner, proj_name):
    query = """query
           {
            repositoryOwner(login:""" +'"'+ owner +'"'+ """) {
            repository(name: """ +'"'+ proj_name +'"'+ """ ) {
            id
            name
            description
            stargazers
            {
                totalCount
            }
            forks
            {
                totalCount
            }
            issues
            {
                totalCount
            }
            pullRequests{
                totalCount
            }
            url
            isArchived
            isDisabled
            isFork
            isLocked
            isMirror
            isPrivate
            visibility
            updatedAt
            createdAt
            licenseInfo
            {
                name
            }
            repositoryTopics(first: 100) {
                nodes
                {
                    topic
                    {
                        name
                    }
                }
            }
            defaultBranchRef {
                name
                target {
                    ... on Commit {
                        history(first: 1, since: "2020-01-01T00:00:00") {
                            totalCount
                                nodes {
                                    ... on Commit {
                                        commitUrl
                                        oid
                                        committedDate
					                    }
				                    }
			            }
                    }
		        }
		    }
        }
        }
    rateLimit {
    limit
    cost
    remaining
    resetAt
    }
    }"""

    return query


def execute_query(status):
    proj_query_cntr = 0
    global proj_index
    failed_proj_url = []

    headers = {'Authorization': 'token %s' % API_TOKEN}
    for proj_url in all_proj_dict:
        proj_index += 1
        owner = proj_url.split('https://github.com/')[1].split('/')[0]
        proj_name = proj_url.split('https://github.com/')[1].split('/')[1]
        proj_query_cntr += 1
        json_query = {'query': get_query(owner, proj_name)}
        r = requests.post(url=URL, json=json_query, headers=headers)
        data = json.loads(r.text)
        print(data)

        if r.status_code == 200:
            if data.get("data") is None:
                failed_proj_url.append(proj_url)
                print(r.text)

        extract_data(data, proj_url)
        rate_limit_info = data['data']['rateLimit']
        print(rate_limit_info)

        if rate_limit_info['remaining'] < 5:
            duration = (datetime.datetime.strptime(
                rate_limit_info['resetAt'], '%Y-%m-%dT%H:%M:%SZ') -
                        datetime.datetime.utcnow()).total_seconds() + 6
            print("Limit exhausted ")
            print("Sleep for " + str(duration))
            time.sleep(duration)
            continue

    op_file_name = "repos_meta_1_" + status + ".csv"
    with open(op_file_name, 'w', encoding="utf-8") as fi:
        for _ in result_set:
            fi.write(_ + '\n')


def initialize_projs():
    proj_cntr = 0
    proj_dict = {}
    with open(meta_inp_file, encoding="utf-8") as f:
        repos_list = f.readlines()

    for repo in repos_list:
        repo = repo.strip().split(',')[0]
        if re.search("https://github\.com", repo.lower()):
            proj_cntr += 1
            proj_dict[repo] = repo.split('https://github.com/')[1]
            if proj_cntr == 1251:
                break

    return proj_dict


inp_csv_file = 'repos_meta_1_by_commits_desc.csv'
invalid_url_counter = 0
invalid_url_list = []
proj_index = 0
result_set = []
meta_inp_file = "repos_meta_1_by_commits_desc.csv"
all_proj_dict = initialize_projs()

if __name__ == '__main__':
    execute_query("before")
    print("before downloading repos invalid urls: ", invalid_url_list)
    print("Total invalid repos before downloading repos (i.e., repos deleted or removed after getting repo meta: ", len(invalid_url_list))

    logging.basicConfig(filename=os.getcwd() + '\\' + "repos_downloader_1" + datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + '.log', level=logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    read_csv_and_process_download(inp_csv_file)

    invalid_url_counter = 0
    invalid_url_list = []
    proj_index = 0
    execute_query("after")
    print("after downloading repos invalid urls: ", invalid_url_list)
    print("Total invalid repos after downloading repos (i.e., repos deleted or removed after getting repo meta: ", len(invalid_url_list))


