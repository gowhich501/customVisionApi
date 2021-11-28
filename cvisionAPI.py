import sys
import requests
import json
import glob

BASE_URL = "https://japaneast.api.cognitive.microsoft.com/customvision/v3.3/Training/"
HOST = "japaneast.api.cognitive.microsoft.com"

'''

'''
def makeProject(key, name):
    end_point = BASE_URL + "projects?name="+ name +"&classificationType=Multilabel"
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

def getProjects(key):
    end_point = BASE_URL + "/projects"
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
        projects = r.json()
    except Exception as e:
        projects = None
        print(r.json())
    return projects

def uploadImageData(key, projectId, path, tagId):

    tagIds = tagId.split(',')
    print(tagIds)
    tagIdString = ""
    for s in tagIds:
        if tagIdString == "" :
            tagIdString = s
        else:
            tagIdString = tagIdString + "," + s

    end_point = BASE_URL + "projects/"+ projectId +"/images?tagIds={" + tagIdString + "}"
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

def train(key, projectId):
    end_point = BASE_URL + "projects/"+ projectId +"/train"
    print(end_point)
    headers = {
        "HOST" : HOST,
        "Training-key" : key
    }

    r = requests.post(
        end_point,
        headers = headers
    )
    try:
        tags = r.json()
    except Exception as e:
        tags = None
        print(r.json())
    return tags

def test(key, projectId, imageFile, iterationId):
    end_point = BASE_URL + "projects/"+ projectId +"/quicktest/image?iterationId=" + iterationId
    print(end_point)
    headers = {
        "Content-type" : "application/octet-stream",
        "HOST" : HOST,
        "Training-key" : key
    }

    image = open(imageFile, "rb")
    reqbody = image.read()
    image.close()

    r = requests.post(
        end_point,
        data = reqbody,
        headers = headers
    )
    try:
        tags = r.json()
    except Exception as e:
        tags = None
        print(r.json())
    return tags

## -------------------------------------------------
# メインプログラム
## -------------------------------------------------
if __name__ == "__main__":
    f = open('key.txt', 'r')
    key = f.read()
    # print(key)

    args = sys.argv
    if args[1:2] :
        print(args[1])

        # プロジェクトの作成 makeProject 
        # params: PROJECT_NAME
        if args[1] == "makeProject" :
            if args[2:3] :
                projectId = makeProject(key, args[2])
                print("Project was successfully made. The project ID is " + projectId)
            else:
                print ("Input prject name.")
            exit()

        # タグの作成 makeTag 
        # params: PROJECT_ID, TAG_NAME
        if args[1] == "makeTag" :
            if args[2:4] :
                tagId = makeTag(key, args[2], args[3])
                print("Tag was successfully made. The tag ID is " + tagId)
            else:
                print ("Input prject ID and tag name.")
            exit()

        # タグの一覧 get Tags
        # params: PROJECT_ID
        if args[1] == "getTags" :
            if args[2:3] :
                tags = getTags(key, args[2])
                print(json.dumps(tags,indent=2))
            else:
                print ("Input prject ID.")
            exit()

        # プロジェクトの一覧 getProjects
        # params: 
        if args[1] == "getProjects" :
            tags = getProjects(key)
            print(json.dumps(tags,indent=2))
            exit()

        # 画像のアップロードとタグ付け uploadImages
        # params: PROJECT_ID, PATH, TAG_IDs
        if args[1] == "uploadImages" :
            if args[2:5] :
                uploadImageData(key, args[2], args[3], args[4])

            else:
                print ("Input directory path.")
            exit()

        # 学習の実行
        # params: PROJECT_ID
        if args[1] == "train" :
            if args[2:3] :
                tags = train(key, args[2])
                print(json.dumps(tags,indent=2))
            else:
                print ("Input prject ID.")
            exit()

        # テスト
        # params: PROJECT_ID, IMAGE_FILE_PATH, ITERATION_ID
        if args[1] == "test" :
            if args[2:5] :
                tags = test(key, args[2], args[3], args[4])
                print(json.dumps(tags,indent=2))
            else:
                print ("Input prject ID.")
            exit()

        # 制御コマンド(第一引数)が不正
        else :
            print ("Invalid control command.")
            exit()

    else : 
        print ("Input control command.")
        

