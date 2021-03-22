import requests
import os
import json
import time

#url_by_stars = 'https://api.github.com/search/repositories?q=language:go&sort=stars&order=desc&per_page=100&page='
#url_by_forks = 'https://api.github.com/search/repositories?q=language:go&sort=forks&order=desc&per_page=100&page='
#url_by_watchers = 'https://api.github.com/search/repositories?q=language:go&sort=watchers&order=desc&per_page=100&page='

#urls = [url_by_stars,url_by_forks,url_by_watchers]

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:                   
        os.makedirs(path)            
        print("new folder: %s" % path)

def get_info(lang:str,per_page:int,pages:int,sort='stars',order='desc'):
    url_ptn = 'https://api.github.com/search/repositories?q=language:{}&sort={}&order={}&per_page={}&page='
    isfile = os.path.isfile('repo_name.json')
    spec_url = url_ptn.format(lang,sort,order,per_page)
    urls = [spec_url,]

    if not isfile:
        f = open('repo_name.json','w+')
        json.dump({'repo_num':0,'repos':[]},f,indent=4)
        f.close()

    f = open('repo_name.json','r')
    repo_list = json.load(f)
    repo_num = repo_list['repo_num']
    all_repos = repo_list['repos']
    f.close()

    for i in range(1,pages+1):
        try:
            for url in urls:
                print('now getting page: %s' % str(i))
                r = requests.get(url+str(i))
                result = json.loads(r.content)
                #result = json.loads(r.content.decode('UTF-8'))
                for repo in result['items']:
                    try:
                        name = repo['name']
                        if name not in all_repos:
                            repo_num += 1
                            all_repos.append(name)
                            mkdir('./repos-info/'+name)
                            with open('./repos-info/'+name+'/'+name+'.json','w+') as f:
                                json.dump(repo,f,indent=4)
                                f.close()
                    except Exception as e:
                        print(e)
                #time.sleep(1.0)
        except Exception as e:
            print(e)

    repo_list['repo_num'] = repo_num
    repo_list['repos'] = all_repos
    print('repo_num:'+str(repo_num))
    f = open('repo_name.json','w+')
    json.dump(repo_list,f,indent=4)
    f.close()

