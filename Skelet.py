import openalea.plantscan3d.mtgmanip as mm
from openalea.mtg.aml import MTG
from openalea.mtg.io import write_mtg
from openalea.plantgl.all import *
from openalea.plantscan3d.serial import max_order
from openalea.plantscan3d.xumethod import xu_method
import open3d as o3d

INPUT_POINT_CLOUDS_DIR = "C:/Users/Olav/Documents/School/TI04/Afstudeerstage/pointCloud_appel_boom/Apple/"

def loadPointCloud():
    """
    The loadPointCloud function loads a point cloud file as a pointList.
    When the points are loaded they will be returned.

    :return: scene[0].geometry.pointList
    """
    scene = Scene(INPUT_POINT_CLOUDS_DIR + 'apple.ply')
    points = scene[0].geometry.pointList
    return points

def find_root(points):
    """
    The skeleton function find the bottom centre of the point cloud.
    The bottom centre is the start of the skelet.
    This function is written by plantscan3d the functionality isn't
    100% clear.

    :param points: scene[0].geometry.pointList
    :return : scene[0].geometry.point, zmin, zmax
    """
    center = points.getCenter()
    pminid,pmaxid = points.getZMinAndMaxIndex()
    zmin = points[pminid].z
    zmax = points[pmaxid].z
    initp = center
    initp.z = zmin
    return points.findClosest(initp)[0], zmin, zmax

def skeleton(points, binratio = 50, k = 20):
    """
    The skeleton function creates a skeleton(using xu_method) from a pear tree point_cloud.
    This skeleton is stored in a .mtg file.
    This mtg file could be exported or worked with internally.

    :param points: scene[0].geometry.pointList
    :param binratio: binratio=50
    :param k: k=20
    :return mtg: mtg object
    """
    root, zmin, zmax = find_root(points)

    mtg = mm.initialize_mtg(root)
    zdist = zmax-zmin
    binlength = zdist / binratio

    vtx = list(mtg.vertices(mtg.max_scale()))
    startfrom = vtx[0]
    mtg = xu_method(mtg, startfrom, points, binlength, k)

    return mtg

def readMTGobject(g):
    """
    A mtg object has a lot of data, but only a part of it needed.
    The saveMTGfile function gets the needed information
    and save it in a list so it can be processed later.

    :param g: mtg object
    :return tree: list
    """
    label = g.property('position')
    edgeType = g.property('edge_type')
    branchType = []
    counter = 0
    tree = []

    for id, lab in edgeType.items():
        branchType.append(lab)

    for id, lab in label.items():
        point = []
        if(counter != 0):
            # Point id
            point.append(id)
            # Id of previous point in tree
            point.append(g.parent(id))
            # < or + to indicate if point is a new branch or a continuation of a branch
            point.append(branchType[counter-1])
            # XYZ condinates of this Point
            point.append(lab)
        else:
            point.append(id)
            point.append(g.parent(id))
            point.append(None)
            point.append(lab)
        counter += 1
        tree.append(point)
    return tree

def saveList(tree):
    """
    The saveList function saves the skeleton in a text file,
    so it can be read afterwards.

    :param tree: list
    """
    with open('sortedlist.txt', 'w') as f:
        for x in tree:
            f.write("%s\n" % x)

def main(): 
    """
    The main function of this file is to load a point cloud(of a tree),
    get the skeleton from the point cloud
    and save the skeleton in a list so it can be processed elsewhere.
    """
    points = loadPointCloud()
    mtg = skeleton(points)
    tree = readMTGobject(mtg)
    saveList(tree)

if __name__ == '__main__':
    main()