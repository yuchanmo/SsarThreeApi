import zipfile
import os


zipFilename = "deploy.zip"
azureResourceGroup = "art"
azureServiceName = "artlink"


#gitignore 파일읽기
gitignore = [zipFilename]
f = open(".gitignore", 'r')
while True:
    line = f.readline()
    if not line: break
    gitignore.append(line.strip())
    gitignore.append("./"+line.strip())
f.close()
print("exclude : " , gitignore)

#현재 파일리스트읽기
currentFileList = []
cwd = os.getcwd()
for filename in os.listdir(cwd):
	currentFileList.append(filename)


#이미 압축된거 삭제
if os.path.exists(zipFilename):
    os.remove(zipFilename)

#gitignore에 있는 거 빼고 압축하기
zipFile = zipfile.ZipFile(zipFilename, 'w')


for folder, subfolders, files in os.walk('./'):
    subfolders[:] = [d for d in subfolders if d not in gitignore]

    for file in files:
        if file in gitignore:
            continue
        filepath = os.path.join(folder, file)
        print("zipping : " + filepath)
        zipFile.write(filepath, compress_type = zipfile.ZIP_DEFLATED)
 


zipFile.close()



#애저 deploy
cmd = "az webapp deploy --type zip --name "+azureServiceName+" --resource-group "+azureResourceGroup+" --src-path "+zipFilename
print(cmd)
os.system("cmd /c "+cmd)