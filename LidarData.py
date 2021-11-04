import csv
from os import pipe
import matplotlib.pyplot as plt
import numpy as np
import struct

INPUT_CSV_DIR = "C:/Users/Olav/Documents/School/TI04/Afstudeerstage/Data van WUR/AppleSpil/"

class lidarToPly():
    lat = 0.0
    long = 0.0
    alt = 0.0

    def setLatLongAlt(self, gpslat, gpslong, gpsalt):
        self.lat = gpslat
        self.long = gpslong
        self.alt = gpsalt

    def __init__(self):
        return

    def hoekverdraaiing(self):
        thetaList = []
        for i in range(1440):
            thetaList.append((-np.pi / 2 ) + ( 2 * np.pi / 1439 * i))
        return thetaList

    def pol2cart(self, theta, rho):
        x = rho * np.cos(theta)
        y = rho * np.sin(theta)
        return(x, y)

    def rangeFilter(self, csvReader):
        theta = self.hoekverdraaiing()
        #counter = 0
        theta1 = []
        rho = []
        for i in range(1440):
            if (float(csvReader[(i+9)]) < 3.5):
                theta1.append(float(theta[i]))
                rho.append(float(csvReader[i+9]))
        x, y = self.pol2cart(theta1, rho)
        #print(x, y)
        #counter += 1
        #plotGraph(x, y, counter)
        return x, y
        
    def plotGraph(self, x, y, counter):
        if(counter == 1300):
            plt.plot(x, y, 'b-')
            plt.show()
        return

    def readCSV(self):
        csvfile = INPUT_CSV_DIR + "laserscanR2000.csv"
        csvReader = []
        with open(csvfile, newline='') as csvfile:
            csv_reader  = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                csvReader.append(row)
        csvReader.pop(0)
        return csvReader

    def write_pointcloud(self, filename, x, y, z, rgb_points=None):

        """ creates a .pkl file of the point clouds generated
        """

        arr = np.array(x)
        #assert xyz_points.shape[1] == 3,'Input XYZ points should be Nx3 float array'
        if rgb_points is None:
            r_points = np.ones(arr.shape).astype(np.uint8)*255
            g_points = np.ones(arr.shape).astype(np.uint8)*255
            b_points = np.ones(arr.shape).astype(np.uint8)*255
        #assert xyz_points.shape == rgb_points.shape,'Input RGB colors should be Nx3 float array and have same size as input XYZ points'

        # Write header of .ply file
        fid = open(filename,'wb')
        fid.write(bytes('ply\n', 'utf-8'))
        fid.write(bytes('format binary_little_endian 1.0\n', 'utf-8'))
        fid.write(bytes('element vertex %d\n'%len(x), 'utf-8'))
        fid.write(bytes('property float x\n', 'utf-8'))
        fid.write(bytes('property float y\n', 'utf-8'))
        fid.write(bytes('property float z\n', 'utf-8'))
        fid.write(bytes('property uchar red\n', 'utf-8'))
        fid.write(bytes('property uchar green\n', 'utf-8'))
        fid.write(bytes('property uchar blue\n', 'utf-8'))
        fid.write(bytes('end_header\n', 'utf-8'))

        # Write 3D points to .ply file
        for i in range(len(x)):
            fid.write(bytearray(struct.pack("fffccc",x[i],y[i],z[i],
                                            r_points[i].tobytes(),g_points[i].tobytes(),
                                            b_points[i].tobytes())))
        fid.close()

    def getXYZ(self, csvReader):
        x = [] 
        y = []
        z = []
        counter = 0
        for i in csvReader:
            tempX, tempZ = self.rangeFilter(i)
            lat = float(i[3])
            long = float(i[4])
            alt = float(i[5])
            for item in tempX:
                x.append(self.gpsToMeter(self.long, long) + item)
                y.append(self.gpsToMeter(self.lat, lat))
            for item in tempZ:
                z.append(self.alt - alt + item)
        return x, y, z

    def gpsToMeter(self, v1, v2):
        r = 6371000 #straal aarde in meter
        #print(v1, v2)
        return (2 * np.pi * r * ((v2 - v1) / 360))

    def saveGpsData(self, csvReader):
        with open('gpsDatapeer.txt', 'w') as f:
            for item in csvReader:
                f.write("%s, " % item[3])
                f.write("%s\n" % item[4])

    def checkDistanceBetweenLines(self, csvReader):
        distance = []
        for i in range(len(csvReader)-1):
            distance.append(self.gpsToMeter(float(csvReader[i][3]), float(csvReader[(i+1)][3])))
        print(sum(distance)/len(distance))
        #with open('gpsDistance2.txt', 'w') as f:
            #for item in distance:
                #f.write("%s,\n" % item)

    def main(self): 
        csvReader = self.readCSV()
        #self.setLatLongAlt(float(csvReader[0][3]), float(csvReader[0][4]), float(csvReader[0][5]))
        #x, y, z = self.getXYZ(csvReader)
        #print(x, y, z)
        #print(len(x))
        #self.write_pointcloud('pcTwoHead.ply', x, y, z)
        #self.saveGpsData(csvReader)
        self.checkDistanceBetweenLines(csvReader)

if __name__ == '__main__':
    ply = lidarToPly()
    ply.main()