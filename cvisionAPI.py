import sys
import requests
import json
import glob

BASE_URL = "https://japaneast.api.cognitive.microsoft.com/customvision/v3.3/Training/"
HOST = "japaneast.api.cognitive.microsoft.com"

def makeProject(key, name):
    end_point = BASE_URL + "projects?name="+ name +"&classificationType=Multiclass"
    headers = {
        "Content-type" : "application/json",
        "HOST" : HOST,
        "Training-key" : key
    }

    r = requests.post(
        end_point,
        headers = headers
    )
    try:
        projectId = r.json()["id"]
        #print(projectId)
    except Exception as e:
        projectId = None
        print(r.json())
    return projectId

def makeTag(key, projectId, tagName):
    end_point = BASE_URL + "projects/"+ projectId +"/tags?name=" + tagName
    headers = {
        "Content-type" : "application/json",
        "HOST" : HOST,
        "Training-key" : key
    }

    r = requests.post(
        end_point,
        headers = headers
    )
    try:
        tagId = r.json()["id"]
        #print(tagId)
    except Exception as e:
        tagId = None
        print(r.json())
    return tagId

def getTags(key, projectId):
    end_point = BASE_URL + "projects/"+ projectId +"/tags"
    headers = {
        "Content-type" : "application/json",
        "HOST" : HOST,
        "Training-key" : key
    }

    r = requests.get(
        end_point,
        headers = headers
    )
    try:
        tags = r.json()
        #print(tagId)
    except Exception as e:
        tags = None
        print(r.json())
    return tags

def uploadImageData(key, projectId, path, tagId):
    end_point = BASE_URL + "projects/"+ projectId +"/images?tagIds={" + tagId + "}"
    print(end_point)
    headers = {
        "Content-type" : "application/octet-stream",
        "HOST" : HOST,
        "Training-key" : key
    }
    files = glob.glob(path + "\\*")
    fileList = [file for file in files]
    print(files)

    for file in files:
        lfile = file.lower()
        if '.png' in lfile or '.jpg' in lfile :
            print(file)
            image = open(file, "rb")
            reqbody = image.read()
            image.close()

            r = requests.post(
                end_point,
                data = reqbody,
                headers = headers
            )
            try:
                response = r.json()
                print(json.dumps(response,indent=2))
            except Exception as e:
                error = None
                print(json.dumps(error,indent=2))

if __name__ == "__main__":
    f = open('key.txt', 'r')
    key = f.read()
    # print(key)

    args = sys.argv
    if args[1:2] :
        print(args[1])

        # プロジェクト作成
        if args[1] == "makeProject" :
            if args[2:3] :
                projectId = makeProject(key, args[2])
                print("Project was successfully made. The project ID is " + projectId)
            else:
                print ("Input prject name.")
            exit()

        # タグの作成
        if args[1] == "makeTag" :
            if args[2:4] :
                tagId = makeTag(key, args[2], args[3])
                print("Tag was successfully made. The tag ID is " + tagId)
            else:
                print ("Input prject ID and tag name.")
            exit()

        # タグの一覧
        if args[1] == "getTags" :
            if args[2:3] :
                tags = getTags(key, args[2])
                print(json.dumps(tags,indent=2))
            else:
                print ("Input prject ID.")
            exit()

        # 画像のアップロードとタグ付け
        if args[1] == "uploadImages" :
            if args[2:5] :
                #tags = getTags(key, args[2])
                uploadImageData(key, args[2], args[3], args[4])

            else:
                print ("Input directory path.")
            exit()

        # 学習の実行

        # テスト

        # 制御コマンド(第一引数)が不正
        else :
            print ("Invalid control command.")
            exit()

    else : 
        print ("Input control command.")
        

