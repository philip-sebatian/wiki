import os
def listofmds():
    path="entries"
    listofmd=os.listdir(path)
    for i in range(len(listofmd)):
        x=listofmd[i].split(".")
        listofmd[i]=x[0]
    return listofmd


print(listofmds())