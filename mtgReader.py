import numpy as np

class mtgReader:
    def __init__(self):
        return

    def sortBranches(self, coords):
        tree = []
        counter = 0
        for x in coords:
            if(x[2] == "<"):
                for y in range(counter):
                    #print(tree[y][-1][0])
                    #print(x[1])
                    if(tree[y][-1][0] == x[1]):
                        tree[y].append(x)
                        break
                    else:
                        continue
            elif(x[2] == "+"):
                branch = []
                branch.append(x)
                tree.append(branch)
                counter += 1
            else:
                branch = []
                branch.append(x)
                tree.append(branch)
                counter += 1
        return tree

    def saveList(self, tree):
        with open('sortedBranchesAppel2.txt', 'w') as f:
            for x in tree:
                f.write("%s\n" % x)

    def angleBranch(self, tree, branchNumber):
        branchCounter = 0
        for x in tree:
            if(x[0][0] == branchNumber):
                break
            else:
                branchCounter += 1
        
        lengthBranch = len(tree[branchCounter])
        if(lengthBranch != 1):
            v1 = np.array([tree[branchCounter][0][3], tree[branchCounter][0][4], tree[branchCounter][0][5]], dtype=float)
            v2 = np.array([tree[branchCounter][-1][3], tree[branchCounter][-1][4], tree[branchCounter][-1][5]], dtype=float)
            #print(v1, v2)
            x = v2[0] - v1[0]
            y = v2[1] - v1[1]
            z = v2[2] - v1[2]
            angle = np.arcsin(z / np.sqrt((x*x) + (y*y) + (z*z)))
            print(180* angle/np.pi)
            print(tree[branchCounter][0][0])
        else:
            print("Branch is to short!")
            print(tree[branchCounter][0][0])

    def lengthBranches(self, tree):
        branchCounter = 0
        lengthBranch = 0
        totalLength = 0
        lengthList = []
        for i in tree:
            lengthBranch = len(i)
            if(lengthBranch == 1):
                lengthList.append(0)
            else:
                for j in range(lengthBranch-1):
                    if(i[0][0] == '2' and j == 0):
                        v1 = np.array([i[j][1], i[j][2], i[j][3]], dtype=float)
                        v2 = np.array([i[j+1][3], i[j+1][4], i[j+1][5]], dtype=float)
                    else:
                        v1 = np.array([i[j][3], i[j][4], i[j][5]], dtype=float)
                        v2 = np.array([i[j+1][3], i[j+1][4], i[j+1][5]], dtype=float)

                    squared_dist = np.sum((v1-v2)**2, axis=0)
                    length = np.sqrt(squared_dist)

                    totalLength += length
                    if(j == lengthBranch-2):
                        lengthList.append(totalLength)
                        #print(lengthList)
                        totalLength = 0
        return lengthList

    def getLeiders(self, tree, lengthList, leiderLength):
        leiders = []
        counter = 0
        for i in lengthList:
            if(i > leiderLength):
                leiders.append(tree[counter][0][0])
                print(leiders)
            counter += 1
        return leiders

    def getVruchthout(self, tree, lengthList):
        leider = []
        leiderLength = 1.0 #1 meter
        leiders = self.getLeiders(tree, lengthList, leiderLength)
        branchCounter = 0

        for i in leiders:
            for j in tree:
                if(j[0][0] == i):
                    break
                else:
                    branchCounter += 1
            for k in tree[branchCounter]:
                leider.append(k[0])

            for l in tree:
                for m in leider:
                    if(l[0][1] == m):
                        self.angleBranch(tree, l[0][0])
                
        #print(leider)
        return

if __name__ == "__main__":
    vruchthout = mtgReader()
    coords = []
    minimumLeiderLength = 1.0

    #reads the mtg file generated from PlantScan3D
    #and save it in a list.
    #The first 3 lines are removed because they aren't relevent
    text_file = open("skeletAppel2.txt", "r")
    lines = text_file.read().splitlines()
    for x in range(3):
        lines.pop(0)

    #The list gets split on whitespaces, so the list becomes easier to read.
    for x in lines:
        coords.append(x.split())
    tree = vruchthout.sortBranches(coords)
    #vruchthout.angleBranch(tree, '177')
    #vruchthout.saveList(tree)
    lengthList = vruchthout.lengthBranches(tree)
    vruchthout.getVruchthout(tree, lengthList)
    text_file.close()