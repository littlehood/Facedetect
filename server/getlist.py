import os

def GetFileList(dir,fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir,s)
            GetFileList(newDir,fileList)
    #newfileList = map(lambda x: 'templates\\'+x, fileList)
    return fileList

#list = GetFileList('images',[])
