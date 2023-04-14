import json

jsonFilePath = 'officeName.json'

def check(name):

    result = None

    with open(jsonFilePath, 'r') as file:
        data = json.load(file)

    if name in data:
        result = True
    else: result = False

    return result, data

def save(dict):

    with open(jsonFilePath, 'w') as file:
        json.dump(dict, file)


if __name__ == "__main__":
    
    test = ['aa', 'bb' , 'cc']
    testjson = {}
    for rowData in test:
        # officeInfoDict = {
        # f"{rowData}" : {
        #     "업력" : "",
        #     "기업형태" : "",
        #     "사원수" : "",
        #     "매출액" : ""
        #     }
        # }
        testjson[f'{rowData}'] = {'업력': '', '기업형태': '', '매출액': ''}
        # print(officeInfoDict)
        # testjson[officeInfoDict]
    print(testjson)