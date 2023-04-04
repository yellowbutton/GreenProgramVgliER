import sys,json,os,search,searchweb,time,Levenshtein
from icecream import ic


def similar(s1,s2):
    return (Levenshtein.ratio(s1, s2))/1
def get1(l):
    return l[1]
cmd=sys.argv

init={
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
    if cmd[1]=="cleandata":
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
    if cmd[1]=="find1":
        if len(cmd)==2:
            print("错误-无路径提供")
            sys.exit(0)
        else:
            print("搜索")
            name=search.searchmainp(cmd[2].replace("\\", "/"))
            prmname=cmd[2].replace("\\", "/").split("/")[-1]
            fullpath=cmd[2].replace("\\", "/")+"/"+name
            webs=searchweb.searchweb(prmname)
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
    if cmd[1]=="s":
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
            for i in range(0,min(10,len(maylist))):
                print(str(i)+". "+str(maylist[i][0])+"\t"+str(maylist[i][2])+"\t\t"+str(maylist[i][3]))#,maylist[i][1])
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
