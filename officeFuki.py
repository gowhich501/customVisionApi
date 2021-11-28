import sys
import requests
import json
import glob

BASE_URL = "https://myfirstcvisionapi-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/"
HOST = "japaneast.api.cognitive.microsoft.com"

def predirect(key, projectId, iteration, path):
    end_point = BASE_URL + projectId + "/classify/iterations/"+ iteration +"/image"
    # print(end_point)
    headers = {
        "Content-type" : "application/octet-stream",
        "Prediction-Key" : key
    }

    image = open(path, "rb")
    reqbody = image.read()
    image.close()

    r = requests.post(
        end_point,
        headers = headers,
        data = reqbody
    )
    try:
        response = r.json()
        # print(json.dumps(response,indent=2))
    except Exception as e:
        print(r.json())
    return response

def truncate(num, n):
    integer = int(num * (10**n))/(10**n)
    return float(integer)

def detectManOrWoman(key, path):
    res = predirect(key,"ef6cfd7c-c206-452c-810a-6ac9d888d434", "Iteration1", path)
    sex = ""
    if(res != None):
        # print(json.dumps(res["predictions"]))
        if(res["predictions"][0]["probability"] > 0.7):
            sex = str(res["predictions"][0]["tagName"])
            print(sex + " が検出されました")
        elif(res["predictions"][1]["probability"] > 0.7):
            sex = str(res["predictions"][0]["tagName"])
            print(sex + " が検出されました")
        else:
            print("性別を判定できませんでした")

    return sex

def evaluateFukiForMan(key, path):
    res = predirect(key,"7105aebd-9c33-40b7-a8f9-a37b78ab29ca", "Iteration4", path)
    result = ""
    if(res != None):
        for pred in res["predictions"]:
            if(pred["tagName"] == "office"):
                result = result + " オフィスカジュアル度:" + str(truncate(pred["probability"],2))
            if(pred["tagName"] == "casual"):
                result = result + " カジュアル度:" + str(truncate(pred["probability"],2))
    return result

def evaluateFukiForWoman(key, path):
    res = predirect(key,"4ac4999e-1de8-4405-bedc-cb8ab557cfc8", "Iteration3", path)
    result = ""
    if(res != None):
        for pred in res["predictions"]:
            if(pred["tagName"] == "office"):
                result = result + " オフィスカジュアル度:" + str(truncate(pred["probability"],2))
            if(pred["tagName"] == "casual"):
                result = result + " カジュアル度:" + str(truncate(pred["probability"],2))
    return result

if __name__ == "__main__":
    f = open('keyPredict.txt', 'r')
    key = f.read()
    # print(key)
    args = sys.argv
    print("風紀の乱れは仕事の乱れ。オフィス風紀委員です！")
    sex = detectManOrWoman(key, args[1])
    if(sex == "man"):
        result = evaluateFukiForMan(key, args[1])
        print(result)
    elif(sex == "woman"):
        result = evaluateFukiForWoman(key, args[1])
        print(result)
    else:
        print("判定できませんでした")