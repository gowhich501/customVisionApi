import sys
import requests
import json

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
                print("Project was successfully made. The id is " + projectId)
            else:
                print ("Input prject name.")
            exit()

        # タグの作成

        # 画像のアップロードとタグ付け

        # 学習の実行

        # テスト

        # 制御コマンド(第一引数)が不正
        else :
            print ("Invalid control command.")
            exit()

    else : 
        print ("Input control command.")
        

