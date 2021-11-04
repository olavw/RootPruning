from BranchAnalysis import BranchAnalysis
from Skeletonization import Skeletonization


def main(): 
    branch = BranchAnalysis()
    skelet = Skeletonization()
    tree = skelet.main()
    sortedTree = branch.sortBranches(tree)
    #print(sortedTree)
    lengthList = branch.lengthBranches(sortedTree)
    print(lengthList)

if __name__ == '__main__':
    main()