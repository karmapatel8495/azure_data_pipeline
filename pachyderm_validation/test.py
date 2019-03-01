import os
  
def validateEndLines(File_Name):
    validateStatus = True
    print("File Name is")
    print(File_Name)
    Open_file = open(path+File_Name,'rb').readlines()
    print(Open_file)
    for line in Open_file:
        print(line)
        if(b'\r\n' not in line):
            print(line)
            validateStatus = False
            #break
    return validateStatus

#path = '/pfs/query/'
#path = "C:/Users/rajat/Downloads/RCAFiles/RCAFiles/"
path = "/Users/yuvraj/Documents/Test/"
for filename in os.listdir(path):
    if validateEndLines(filename):
        print(filename,":Success")
    else:
        print(filename,":Fail")