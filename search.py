import os,difflib,math,Levenshtein
import win32ui
import win32gui
from icecream import ic
def similar(s1,s2):
    return (Levenshtein.ratio(s1, s2))/1
def searchmainp(path):
    waitfslect=[]
    path=path.replace("\\", "/")
    name=path.split("/")
    for f in os.listdir(path):
        ftype=f.split(".")[-1]
        if ftype == "exe":
            waitfslect.append(f)
    if len(waitfslect)==0:
        return None
    elif len(waitfslect) == 1:
        return waitfslect[0]
    else:
        for i in range(0,len(waitfslect)):
            # waitfslect[i]=[waitfslect[i],difflib.SequenceMatcher(None, waitfslect[i].split(".")[0].lower(), name[-1].lower()).quick_ratio()]
            waitfslect[i]=[waitfslect[i],similar(waitfslect[i].split(".")[0].lower(),name[-1].lower())]
        for i in range(0,len(waitfslect)):
            large, small = win32gui.ExtractIconEx(path+"/"+waitfslect[i][0],0)
            if len(large)!=0:
                waitfslect[i][1]+=0.1
            if len(small)!=0:
                waitfslect[i][1]+=0.1
            if "unins" in waitfslect[i][0] or "Unins" in waitfslect[i][0] or "inst" in waitfslect[i][0] or "Inst" in waitfslect[i][0] or "update" in waitfslect[i][0] or "Update" in waitfslect[i][0]:
                waitfslect[i][1]+=-0.3
            if "launch" in waitfslect[i][0] or "Launch" in waitfslect[i][0] or "win32" in waitfslect[i][0]:
                waitfslect[i][1]+=0.3
            # print(os.path.getsize(path+"/"+waitfslect[i][0]))
        def s0s(lt):
            return os.path.getsize(path+"/"+lt[0])
        waitfslect.sort(key=s0s)
        waitfslect[-1][1]+=0.2
        def s1(lt):
            return lt[1]
        waitfslect.sort(key=s1)
        # ic(waitfslect)
        return waitfslect[-1][0]

def serchprofiledir(dir_path):
    dir_path=dir_path.replace("\\", "/")
    res = []
    for path in os.listdir(dir_path):
        # check if current path is a file
        if not os.path.isfile(os.path.join(dir_path, path)):
            res.append(path)
    all=[]
    for i in res:
        s=searchmainp(dir_path+"/"+i)
        if s != None:
            all.append([i,searchmainp(dir_path+"/"+i)])
    return all
# ic(serchprofiledir(r'D:\Program Files'))
# ic(searchmainp(r"D:\Program Files (x86)\TeamSpeak 3 Client"))
