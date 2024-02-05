import json
import os  
import glob  

def getFormationConf(fileName):
    if not checkFileExists(fileName):
        print(f"\nNo such file :{fileName}")
        input("\nPlease Press <Enter> to exit...")
        exit(0)
    with open(fileName, 'r') as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"\nError loading, {fileName} could not be loaded by json")
            return False
    return data

def checkFileExists(fileName):
    current_dir = os.getcwd()
    if os.path.isfile(os.path.join(current_dir, fileName)): 
        return True
    else:
        return False

def staticMethod(data, fileName):
    roles = data["role"]
    dataPoints = data["data"]
    contents = getTheBeforeConfTitle(data["version"], "Static")
    finalData = f'{contents}'
    for role in roles:
        number = role["number"]
        number = str(number)
        name = role["name"]
        margin1 = len("Goalie         -49.0")
        margin2 = len("   0.0")
        len_name = len(name)
        for dataPoint in dataPoints:
            X = str(dataPoint[number]['x'])
            Y = str(dataPoint[number]['y'])
            len_x = len(X)
            len_y = len(Y)
            margin1Left = margin1 - len_name - len_x
            margin2Left = margin2 - len_y
            margin1Blank = ''
            margin2Blank = ''
            for _ in range(margin1Left):
                margin1Blank = margin1Blank + ' '
            for _ in range(margin2Left):
                margin2Blank = margin2Blank + ' '
            finalData = finalData + f"{number} {name}{margin1Blank}{X}{margin2Blank}{Y}\n"
    finalData = finalData + "# ---------------------------------------------------------"
    with open(f"{fileName}", "w") as f:
    # with open(f"1.txt", "w") as f:
        f.write(finalData)


def getTheBeforeConfTitle(fileNameSuffix, method):
    contents = ''
    lines = ''
    current_dir = os.getcwd()
    for filename in glob.glob(os.path.join(current_dir, '*')):
        if filename.endswith(f'.conf_{fileNameSuffix}'):
            with open(filename, 'r') as f:
                lines = f.readlines()
    if lines == '':
        print(f"\nCould not find file suffix with .conf_{fileNameSuffix}")
        input("\nPlease Press <Enter> to exit...")
        exit(0)
    if method == "Static":
        keyword = "Goalie"
    if method == "delaunayTriangulation":
        keyword = "Begin Samples"
    for line in lines:
        if keyword in line:
            return contents
        contents = contents + line

def getAllConf(goal_dir):
    allConf= []
    for filename in glob.glob(os.path.join(goal_dir, '*')):
        if filename.endswith('.conf'):
            allConf.append(filename)
    return allConf

def delaunayTriangulationMethod(data, fileName):
    roles = data["role"]
    contents = getTheBeforeConfTitle(data["version"], "delaunayTriangulation")
    dataPoints = data["data"]
    dataPointsLen = len(dataPoints)
    finalData = f'{contents}' + f'Begin Samples 2 {dataPointsLen}\n'
    # ----- 0 -----
    
    for dataPoint in dataPoints:
        X = str(dataPoint['ball']['x'])
        Y = str(dataPoint['ball']['y'])
        finalData = finalData + f'----- {dataPoint["index"]} -----\n'
        finalData = finalData + f'Ball {X} {Y}\n'
        for role in roles:
            number = role["number"]
            number = str(number)
            X = str(dataPoint[number]['x'])
            Y = str(dataPoint[number]['y'])
            finalData = finalData + f"{number} {X} {Y}\n"
            
    finalData = finalData + "End Samples\nEnd"
    with open(f"{fileName}", "w") as f:
    # with open(f"2.txt", "w") as f:
        f.write(finalData)        


def auto():
    goal_dir = os.getcwd()
    allConf = getAllConf(goal_dir)
    for conf in allConf:
        data = getFormationConf(conf)
        if not data:
            continue
        if data["method"] == "Static":
            staticMethod(data, conf)
        if data["method"] == "DelaunayTriangulation":
            delaunayTriangulationMethod(data, conf)

def manual():
    conf = input("\nInput the conf filename (like 'normal-formation.conf'): ")
    data = getFormationConf(conf)
    if not data:
        input("\nPlease Press <Enter> to exit...")
        exit(0)
    if data["method"] == "Static":
        staticMethod(data, conf)
    if data["method"] == "DelaunayTriangulation":
        delaunayTriangulationMethod(data, conf)


if __name__ == '__main__':
    while True:
        print("1. 自动将当前所有阵型文件修改为合适格式")
        print("2. 手动选择特定阵型文件进行修改")
        print("0. 退出")
        print("\nPS: 当所选文件已经为合适的格式或者无法已JSON格式读入的其他格式都会在终端打印下面这句话:\n\n\
              Error loading, path\\file could not be loaded by json")
        choice = input("\nInput your choice (0-2)[default is 1, Press <Enter>]: ")
        if not choice:
            choice = "1"
        if choice == "1":
            auto()
            print("\nAll modifications completed...")
            input("\nPlease Press <Enter> to exit...")
            exit(0)
        if choice == "2":
            manual()
            print("\nAll modifications completed...")
            input("\nPlease Press <Enter> to exit...")
            exit(0)
        if choice == "0":
            break
        print("Wrong choice, input again!!!\n\n\n")
