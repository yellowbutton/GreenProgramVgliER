print("加载包及数据")

import sys,json,os,search,searchweb,Levenshtein
from icecream import ic
from pypinyin import lazy_pinyin

def similar(s1,s2):
    return (Levenshtein.ratio(s1, s2))/1
def get1(l):
    return l[1]
cmd=sys.argv

init={
    "sets":{"deepofsearch":1,"maxsearch":10},
    "prms":[{"path":"/"+cmd[0],"search":{"name":"greenvgliER","en":"a green program clean uper","zh":"绿色软件整理"}}]
}

# print(cmd)
try:
    f=open("data.json","r",encoding="utf-8")
    data=json.loads(f.read())
    f.close()
except:
    print("初始化")
    f=open("data.json","w",encoding="utf-8")
    f.write(json.dumps(init))
    f.close()
    print("└ 完成")
finally:
    pass


f=open("data.json","r",encoding="utf-8")
data=json.loads(f.read())
f.close()
print("└ 完成")

def findafile(dir,next=0):
    print("搜索")
    name=search.searchmainp(dir.replace("\\", "/"))
    if name==None:
        if next==data["sets"]["deepofsearch"]:
            print("└ 错误-没有找到可执行文件")
            return
        else:
            print("└ 错误-向下查找")
            try:
                os.listdir(dir)
            except PermissionError:
                print("错误-权限不足")
                return
            ll=os.listdir(dir)
            if len(ll)==0:
                print("└ 错误-没有找到文件夹")
                return
            else:
                for z in ll:
                    if not os.path.isfile(os.path.join(dir, z)):
                        findafile(os.path.join(dir, z),next=next+1)
                return
    # ic(name)
    prmname=dir.replace("\\", "/").split("/")[-1]
    fullpath=dir.replace("\\", "/")+"/"+name
    webs=searchweb.searchweb(prmname)
    if webs==None:
        en=prmname
        zh=searchweb.translate(prmname)
    else:
        en=webs[0]
        zh=webs[1]
    print("└ 完成\n写入")
    if {"path":fullpath,"search":{"name":prmname,"en":en,"zh":zh}} not in data["prms"]:
        data["prms"].append({"path":fullpath,"search":{"name":prmname,"en":en,"zh":zh}})
        f=open("data.json","w",encoding="utf-8")
        f.write(json.dumps(data))
        f.close()
        print("└ 完成")
    else:
        print("└ 错误-重复录入")

# print(len(cmd))
if len(cmd)==1:
    pass
else:
    if cmd[1]=="init":
        if "y" in cmd:
            pass
        else:
            asr=input("[y/N]")
            if asr == "y" or asr=="Y":
                pass
            else:
                sys.exit(0)
        print("初始化")
        f=open("data.json","w",encoding="utf-8")
        f.write(json.dumps(init))
        f.close()
        print("└ 完成")
    elif cmd[1]=="cleandata":
        if "y" in cmd:
            pass
        else:
            asr=input("[y/N]")
            if asr == "y" or asr=="Y":
                pass
            else:
                sys.exit(0)
        print("清除数据")
        os.remove("data.json")
        print("└ 完成")
    elif cmd[1]=="find1":
        if len(cmd)==2:
            print("错误-无路径提供")
            sys.exit(0)
        else:
            findafile(cmd[2])
            sys.exit(0)
    elif cmd[1]=="s":
        if len(cmd)==2:
            print("错误-无名称提供")
            sys.exit(0)
        else:
            prmname=cmd[2]
            maylist=[]
            for i in data["prms"]:
                sls=0
                sls+=similar(prmname.lower(),i["search"]["name"].lower())
                if prmname in i["search"]["en"]:
                    sls+=0.3
                elif prmname in i["search"]["zh"]:
                    sls+=0.6
                else:
                    pinyind=""
                    for k in lazy_pinyin(i["search"]["zh"]):
                        pinyind+=k
                    if prmname in pinyind:
                        sls+=0.5
                if sls<=0.2:
                    pass
                else:
                    maylist.append([i["search"]["name"],sls,i["search"]["zh"],i["search"]["en"],i["path"]])
            maylist.sort(key=get1)
            maylist.reverse()
            if len(maylist)!=0:
                pass
            else:
                print("未找到")
                sys.exit(0)
            for i in range(0,min(data["sets"]["deepofsearch"],len(maylist))):
                print(str(i)+". "+str(maylist[i][0])+"\t"+str(maylist[i][2])+"\t\t"+str(maylist[i][4]))#,maylist[i][1])
            if "y" in cmd:
                os.startfile(maylist[0][4])
                sys.exit(0)
            else:
                asr=input("[Y/n/0-9]")
                if asr == "n" or asr=="N":
                    sys.exit(0)
                else:
                    if asr == "y" or asr=="Y" or asr=="0" or asr=="":
                        os.startfile(maylist[0][4])
                        sys.exit(0)
                    else:
                        try:
                            maylist[int(asr)][4]
                        except:
                            print("输入不合理")
                            sys.exit(0)
                        else:
                            os.startfile(maylist[int(asr)][4])
                            sys.exit(0)
    elif cmd[1]=="findf":
        if len(cmd)==2:
            print("错误-无路径提供")
            sys.exit(0)
        else:
            dir_path=cmd[2]
            dir_path=dir_path.replace("\\", "/")
            res = []
            try:
                os.listdir(dir_path)
            except PermissionError:
                print("错误-权限不足")
                sys.exit(0)
            for path in os.listdir(dir_path):
                # check if current path is a file
                if not os.path.isfile(os.path.join(dir_path, path)):
                    res.append(path)
            for i in res:
                findafile(dir_path+"/"+i)
            # findafile(cmd[2])
            sys.exit(0)
    elif cmd[1]=="list":
        ic(data)
