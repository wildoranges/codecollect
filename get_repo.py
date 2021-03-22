import json
import os
os.environ["GIT_PYTHON_REFRESH"] = "quiet"
import git
import shutil

def get_repo(valpath:str,info_path = './repos-info/',repo_path = './repos/'):
    isfile = os.path.isfile(valpath)
    if not isfile:
        print('cannot find valid_repos.json,run get_repo_info.py and select_repo.py first')
        exit(1)
    isexist = os.path.exists(repo_path)
    if not isexist:
        os.makedirs(repo_path)
    isfolder = os.path.isdir(repo_path)
    if not isfolder:
        print('error: {} is not a folder'.format(repo_path))
        exit(1)
    f = open(valpath,'r')
    valid_info = json.load(f)
    f.close()
    names = valid_info['valid_repos']
    pattern = info_path + '{}/{}.json'
    got_repos = os.listdir(repo_path)
    for name in names:
        if name not in got_repos:
            try:
                print('now getting repo : '+name)
                path = pattern.format(name,name)
                isfile = os.path.isfile(path)
                if not isfile:
                    print('warning:possibly missing file {}'.format(path))
                    continue
                f = open(path,'r')
                repo_info = json.load(f)
                f.close()
                git.Repo.clone_from(url=repo_info['clone_url'],to_path=repo_path+name)
            except Exception as e:
                print(e)
                if os.path.isdir(repo_path+name):
                    shutil.rmtree(repo_path+name)
                elif os.path.isfile(repo_path+name):
                    os.remove(repo_path+name)
                continue
