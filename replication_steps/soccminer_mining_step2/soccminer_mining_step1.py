import os
import traceback
from soccminer import CommentsMiner
import time
import sys
import glob
import os.path
from pathlib import Path
import shutil

def get_abs_subdir(location):
    if os.path.exists(location) and os.path.isdir(location):
        return [f.path for f in os.scandir(location) if os.path.isdir(f)]
    else:
        return []


def get_elapsed_time(job_start_time):
    return round((time.time_ns() - job_start_time) / 1000000000)


def get_remaining_job_time_in_sec(job_start_time):
    elapsed_time = get_elapsed_time(job_start_time)
    #  3 days (minus 15 mins buffer) is 258300 and reduce the elapsed time to get remaining time of the executing job
    return 258300 - elapsed_time


def job_time_availability(job_start_time):
    return False if get_remaining_job_time_in_sec(job_start_time) < 64800 else True


def update_remaining_projects(proj):
    global remaining_projects
    remaining_projects.remove(proj)

    with open(remaining_proj_file, 'w', encoding="utf-8") as fi:
        for _ in remaining_projects:
            fi.write(_ + '\n')

def update_large_projects(proj):
    global large_projects
    large_projects.append(proj)

    with open(large_proj_file, 'w', encoding="utf-8") as fi:
        for _ in large_projects:
            fi.write(_ + '\n')


def update_completed_projects(proj):
    global completed_projects
    completed_projects.append(proj)

    with open(completed_proj_file, 'w', encoding="utf-8") as fi:
        for _ in completed_projects:
            fi.write(_ + '\n')

def fetch_proj_size(location):
    #print("fetch_proj_size for proj: ",location)
    return len(glob.glob(location + '/**/*.' + "java", recursive=True))

def update_errored_projects(projs):
    with open(errored_proj_file, 'w', encoding="utf-8") as fi:
        for _ in projs:
            fi.write(_ + '\n')

def get_rem_from_file(inp_file):
    clean_repos_list = []
    with open(inp_file, encoding="utf-8") as f:
        repos_list = f.readlines()

    for repo in repos_list:
        repo = repo.strip()
        clean_repos_list.append(repo)
    
    return clean_repos_list

########################
#  Main
########################

part = sys.argv[1]
source_code_dir= sys.argv[2]

print("executing for ",part)
source_code_location = source_code_dir+'/group_'+part  #"/scratch/project_2002565/source_code_repositories_v2/repos_3/group_" + part
print("source_code_dir: ", source_code_location)

output_location = source_code_location
final_output_location = "/scratch/project_2002565/soccminer_mined_data_v2/repos_1/SoCCMiner_Mined_Entities"

remaining_proj_file = "/scratch/project_2002565/soccminer_mining/repos_1/group_" + part + "/" + "remaining_projects_tobe_mined_" + part + ".csv"
completed_proj_file = "/scratch/project_2002565/soccminer_mining/repos_1/group_" + part + "/" + "mining_completed_projects_" + part + ".csv"
errored_proj_file = "/scratch/project_2002565/soccminer_mining/repos_1/group_" + part + "/" + "errored_projects_" + part + ".csv"
large_proj_file = "/scratch/project_2002565/soccminer_mining/repos_1/group_" + part + "/" + "postponed_large_projects_" + part + ".csv"

print("about to start soccminer job")
job_start_time = time.time_ns()
projects_list = get_abs_subdir(source_code_location)
remaining_projects = None
if os.path.exists(remaining_proj_file):
    remaining_projects = get_rem_from_file(remaining_proj_file)
else:
    remaining_projects = get_abs_subdir(source_code_location)
completed_projects = []
errored_projs = []
large_projects = []

print("about to begin processing projects", len(projects_list))
for proj in projects_list:
    if job_time_availability(job_start_time):
        try:
            if proj in remaining_projects:
                if fetch_proj_size(proj) < 15000:
                    print("proj {} size is: {}".format(proj, fetch_proj_size(proj)))
                    #exit(0)
                    project_obj = CommentsMiner(source_url=proj, m_level="all", output_dir=output_location)
                    update_completed_projects(proj)
                    update_remaining_projects(proj)
                else:
                    update_large_projects(proj)
            else:
                print("{} already completed, hence skipping.".format(proj))
        except Exception as ex:
            error_message = traceback.format_exc()
            print("Unexpected error for project {} with {} {}".format(proj, error_message, ex))
            errored_projs.append(proj)
            update_errored_projects(errored_projs)
            continue


print("copying files from: ", output_location+'/SoCCMiner_Mined_Entities')
for directory in [f for f in Path(output_location+'/SoCCMiner_Mined_Entities').iterdir() if f.is_dir()]:
    out_dir = final_output_location + '/' + str(directory).split('/')[-1]
    print("Output dir copy status for {} is: {}".format(str(directory).split('/')[-1], shutil.copytree(str(directory), out_dir)))
    
