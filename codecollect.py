from get_repo import get_repo
from get_repo_info import get_info
from select_repo import select_repo
import json

def codecollect(lang:str,per_page:int,pages:int,sort:str,order:str,isselect=False):
    get_info(lang,per_page,pages,sort,order)
    if isselect:
        select_repo()
    else:
        f = open('valid_repos.json','w+')
        init_info = {'valid_repo_num':0,'valid_repos':[]}
        json.dump(init_info,f,indent=4)
        f.close()
        f = open('valid_repos.json','r')
        all_info = json.load(f)
        f.close()
        cnt = all_info['valid_repo_num']
        valid_repos = all_info['valid_repos']
        valid_info = all_info
        #pattern = './repos-info/{}/{}.json'
        f = open('repo_name.json','r')
        all_repo = json.load(f)
        names = all_repo['repos']
        f.close() 

        for name in names:
            if name not in valid_repos:
                cnt += 1
                valid_repos.append(name)

        valid_info['valid_repo_num'] = cnt
        valid_info['valid_repos'] = valid_repos
        f = open('valid_repos.json','w+')
        json.dump(valid_info,f,indent=4)
        f.close()

    get_repo('valid_repos.json')

if __name__=='__main__':
    codecollect('C',10,1,'stars','desc')

