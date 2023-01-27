

# This script uses graphql GitHub API to extract repository information based on our criterion
# It repeat itself with required wait so that we don't have to run repeatedly;
# run once and leave it for a night, it will give you a list of repositories to download and analyze
# Required parameters: API token, language (set the language 'Csharp'/'java' in _get_json_query method).
import datetime
import json
import time

import requests

URL = 'https://api.github.com/graphql'
API_TOKEN = '' # generate your API token and replace it
MIN_REPO_SIZE = "100"  # in KBs

cursor = ""
PAGE_LIMIT = 99  # maximum permitted is 100 but keep it 99 or below to satisfy 1000 node Pagination limit

#three_year_old_date = (datetime.datetime.now().date() - datetime.timedelta(days=1 * 46))
#print(three_year_old_date)
three_year_old_date = (datetime.datetime.now().date() - datetime.timedelta(days=1 * 1102)) # 734 two year date
print(three_year_old_date)
#exit(1)


current_date = three_year_old_date
# current_date = datetime.date(2019, 10, 6)

ind_num = 0
count = 1
duplicate_count = 0
name_with_owner_list = []
local_name_with_owner_list = []

failed_dates = []
repo_count_exceed_case_dates = []


def _extract_name_with_owner_list(data):
    global ind_num
    global duplicate_count
    global local_name_with_owner_list
    local_name_with_owner_list = []

    for edge in data['data']['search']['edges']:
        proj_homepage = 'None'
        if edge['node']['nameWithOwner'] in name_with_owner_list:
            duplicate_count = duplicate_count + 1
            print("Duplicate = " + str(duplicate_count))
        else:
            for history_node in  edge['node']['defaultBranchRef']['target']['history']['nodes']:
                if str(edge['node']['licenseInfo']) != "None":
                    local_name_with_owner_list.append(str(ind_num) + "," +
                                                  str(edge['node']['name']) + "," +
                                                  str(edge['node']['owner']['login']) + "," +
                                                  str(edge['node']['nameWithOwner']) + "," +
                                                  str(edge['node']['primaryLanguage']['name']) + "," +
                                                  str(edge['node']['stargazers']['totalCount']) + "," +
                                                  str(edge['node']['forks']['totalCount']) + "," +
                                                  str(edge['node']['url']) + "," +
                                                  str(edge['node']['isArchived']) + "," +
                                                      str(edge['node']['isDisabled']) + "," +
                                                      str(edge['node']['isFork']) + "," +
                                                      str(edge['node']['isLocked']) + "," +
                                                      str(edge['node']['isMirror']) + "," +
                                                      str(edge['node']['isPrivate']) + "," +
                                                      str(edge['node']['visibility']) + "," +
                                                  str(edge['node']['updatedAt']) + "," +
                                                  str(edge['node']['createdAt']) + "," +
                                                  str(edge['node']['licenseInfo']['name']) + "," +
                                                  str(edge['node']['defaultBranchRef']['name']) + "," +
                                                  str(edge['node']['defaultBranchRef']['target']['history']['totalCount']) + "," +
                                                  str(history_node['commitUrl']) + "," +
                                                  str(history_node['committedDate']))
                elif str(edge['node']['licenseInfo']) == "None":
                    local_name_with_owner_list.append(str(ind_num) + "," +
                                                      str(edge['node']['name']) + "," +
                                                      str(edge['node']['owner']['login']) + "," +
                                                      str(edge['node']['nameWithOwner']) + "," +
                                                      str(edge['node']['primaryLanguage']['name']) + "," +
                                                      str(edge['node']['stargazers']['totalCount']) + "," +
                                                      str(edge['node']['forks']['totalCount']) + "," +
                                                      str(edge['node']['url']) + "," +
                                                      str(edge['node']['isArchived']) + "," +
                                                      str(edge['node']['isDisabled']) + "," +
                                                      str(edge['node']['isFork']) + "," +
                                                      str(edge['node']['isLocked']) + "," +
                                                      str(edge['node']['isMirror']) + "," +
                                                      str(edge['node']['isPrivate']) + "," +
                                                      str(edge['node']['visibility']) + "," +
                                                      str(edge['node']['updatedAt']) + "," +
                                                      str(edge['node']['createdAt']) + "," +
                                                      "None" + "," +
                                                      #str(edge['node']['collaborators']['totalCount']) + "," +
                                                      str(edge['node']['defaultBranchRef']['name']) + "," +
                                                      str(edge['node']['defaultBranchRef']['target']['history'][
                                                              'totalCount']) + "," +
                                                      str(history_node['commitUrl']) + "," +
                                                      str(history_node['committedDate']))
                ind_num+=1

def _get_json_query(repo_size, current_date, after_cursor):
    json_query = {'query': """{  search( query: "language:java stars:>10 size:""" + repo_size + """ pushed:""" + str(
        current_date) + """", 
    type: REPOSITORY, first:  """ + str(PAGE_LIMIT) + str(after_cursor) + """)
    {
    edges {
      node {
        ... on Repository {
          name
          owner {
            login
          }
          nameWithOwner
          primaryLanguage {
            name
          }
          stargazers {
            totalCount
          }
          forks {
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
          licenseInfo {
            name
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
                                                committedDate
					                                }
				                                }
			                                }
                            			 }
		                            }
		                        }
        }
      }
    }
    repositoryCount
    
    pageInfo {
      hasNextPage
      endCursor
    }
  }
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
}
"""
            }
    print(json_query)
    return json_query


def _iterate_over_pages_and_append_file(size, possible, current_date, cursor):
    global count
    global duplicate_count
    global local_name_with_owner_list
    #with open('repos_list2.csv', 'a', encoding="utf-8") as fi:
    with open('updated_repos_list.csv', 'a', encoding="utf-8") as fi:
    #with open('repos_without_desc_with_lic_since_2020_01_01.csv', 'a', encoding="utf-8") as fi:
    #    since: "2020-01-01T00:00:00
        while possible:
            after_cursor = ', after: "' + cursor + '"' if not str(cursor) == "" else ""
            json_data = _get_json_query(size, current_date, after_cursor)

            #print(json_data)
#"""
            headers = {'Authorization': 'token %s' % API_TOKEN}
            r = requests.post(url=URL, json=json_data, headers=headers)
            data = json.loads(r.text)
            print(data)
            if r.status_code == 200:
                if data.get("data") is None:
                    failed_dates.append(current_date)
                    print("Failed")
                    print(r.text)
                    break
                print("Repo Count: " + str(data['data']['search']['repositoryCount']))
                #if data['data']['search']['repositoryCount'] > 1000:
                #    _repo_count_exceeded(current_date, cursor, possible, size)
                #    break
                _extract_name_with_owner_list(data)
                count = count + 1

                print("Page " + str(count) + " results:")

                # print(local_name_with_owner_list)
                print("Write :{}".format(local_name_with_owner_list))
                for _ in local_name_with_owner_list:
                    fi.write(_ + '\n')

                page_info = data['data']['search']["pageInfo"]
                rate_limit_info = data['data']['rateLimit']
                print("Call cost = ")
                print(rate_limit_info)
                print("Page limit")
                print(page_info)

                if rate_limit_info['remaining'] == 0:
                    duration = (datetime.datetime.strptime(
                        rate_limit_info['resetAt'], '%Y-%m-%dT%H:%M:%SZ') -
                                datetime.datetime.utcnow()).total_seconds() + 1
                    print("Limit exhausted ")
                    print("Sleep for " + str(duration))
                    time.sleep(duration)
                    continue

                if page_info['hasNextPage']:
                    cursor = page_info['endCursor']
                else:
                    possible = False

            else:
                print("Request failed: ")
                print("Response:" + str(r.text))
                failed_dates.append(current_date)
                possible = False
#"""

def _repo_count_exceeded(current_date, cursor, possible, size):
    print("repo count exceeded")
    if size[0] == ">":
        new_size = size[1:] + ".." + str(int(size[1:]) + 100)
        _iterate_over_pages_and_append_file(new_size, possible, current_date, cursor)
        new_size = ">" + str(int(size[1:]) + 100)
        _iterate_over_pages_and_append_file(new_size, possible, current_date, cursor)
    elif size[0] == "<":
        new_size = str(int(size[1:]) - 100) + ".." + size[1:]
        _iterate_over_pages_and_append_file(new_size, possible, current_date, cursor)
        new_size = "<" + str(int(size[1:]) - 100)
        _iterate_over_pages_and_append_file(new_size, possible, current_date, cursor)
    else:
        split = size.split("..")
        upper_limit = int(split[1])
        lower_limit = int(split[0])
        mid_limit = int((upper_limit + lower_limit) / 2)
        size = str(lower_limit) + ".." + str(mid_limit)
        _iterate_over_pages_and_append_file(size, possible, current_date, cursor)
        size = str(mid_limit) + ".." + str(upper_limit)
        _iterate_over_pages_and_append_file(size, possible, current_date, cursor)
    repo_count_exceed_case_dates.append(current_date)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while not current_date == datetime.datetime.now().date() - datetime.timedelta(days=1 * 8):
        print("Date records : " + str(current_date))
        possible = True
        cursor = ""
        current_date = (current_date + datetime.timedelta(days=1))
        size = ">" + MIN_REPO_SIZE  # Default limit can be set here
        _iterate_over_pages_and_append_file(size, possible, current_date, cursor)

    print("All records checked!")
    print("Dates which caused a fail : ")
    print(failed_dates)
    print("Repos with exceeded limit")
    print(repo_count_exceed_case_dates)


