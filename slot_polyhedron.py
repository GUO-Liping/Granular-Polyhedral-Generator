
# -*- encoding=utf-8 -*-
from yade import plot, polyhedra_utils
import numpy as np

def rotate_x(xyz_array, phi_x):
        x= xyz_array[:,0]
        y= xyz_array[:,1]
        z= xyz_array[:,2]

        xr = x
        yr = y * np.cos(phi_x) - z*np.sin(phi_x)
        zr = y * np.sin(phi_x) + z*np.cos(phi_x)

        xyz = np.vstack((xr, yr, zr))

        return xyz.T

def rotate_y(xyz_array, phi_y):
        x= xyz_array[:,0]
        y= xyz_array[:,1]
        z= xyz_array[:,2]

        xr = x * np.cos(phi_y) + z*np.sin(phi_y)
        yr = y
        zr = -x * np.sin(phi_y) + z*np.cos(phi_y)

        xyz = np.vstack((xr, yr, zr))

        return xyz.T

def rotate_z(xyz_array, phi_z):
        x= xyz_array[:,0]
        y= xyz_array[:,1]
        z= xyz_array[:,2]

        xr = x * np.cos(phi_z) - y*np.sin(phi_z)
        yr = x * np.sin(phi_z) + y*np.cos(phi_z)
        zr = z

        xyz = np.vstack((xr, yr, zr))

        return xyz.T

def translate_xyz(xyz_array, trans_arr):
        x= xyz_array[:,0]
        y= xyz_array[:,1]
        z= xyz_array[:,2]

        xt = x + trans_arr[0]
        yt = y + trans_arr[1]
        zt = z + trans_arr[2]

        xyz = np.vstack((xt, yt, zt))

        return xyz.T

minX = 0
minY = 0
minZ = 0

maxX = 0.44
maxY = 0.27
maxZ = 0.20

minSizeX = 0.02
minSizeY = 0.02
minSizeZ = 0.02

maxSizeX = 0.04
maxSizeY = 0.04
maxSizeZ = 0.04

phi_x = 0
phi_y = np.pi*2/9
phi_z = 0

coor_x = np.arange(minX+0.02, maxX-0.02, 1.5*maxSizeX)
coor_y = np.arange(minX+0.02, maxY-0.02, 1.5*maxSizeY)
coor_z = np.arange(minX+0.02, maxZ-0.02, 1.5*maxSizeZ)

len_x = len(coor_x)
len_y = len(coor_y)
len_z = len(coor_z)
coor_xyz = np.zeros((len_x*len_y*len_z, 3))

for ix in range(len_x):
    for iy in range(len_y):
            for iz in range(len_z):
                coor_xyz[ix+len_x*(iy)+len_x*len_y*(iz), 0] = coor_x[ix]
                coor_xyz[ix+len_x*(iy)+len_x*len_y*(iz), 1] = coor_y[iy]
                coor_xyz[ix+len_x*(iy)+len_x*len_y*(iz), 2] = coor_z[iz]

print(coor_xyz)

coor_xyz = rotate_y(coor_xyz, phi_y)
coor_xyz = translate_xyz(coor_xyz, np.array([-2.002,-0.135,1.706]))

gravel = PolyhedraMat(density = 3070, young = 7e9, poisson = 0.2, frictionAngle = 0.4) #rad
steel = PolyhedraMat(density = 7850, young = 210e9, poisson = 0.3, frictionAngle = 0.3 ) #rad

O.materials.append(gravel) #adds material to yade
# O.materials.append(steel) #adds material to yade

list_poly = []
rows, columns = coor_xyz.shape
for i in range(rows):
        sizeX = minSizeX + (maxSizeX - minSizeX)*np.random.random()
        sizeY = minSizeY + (maxSizeY - minSizeY)*np.random.random()
        sizeZ = minSizeX + (maxSizeZ - minSizeZ)*np.random.random()
        poly = polyhedra_utils.polyhedra(gravel, size=Vector3(sizeX,sizeY,sizeZ), seed=None, v=[], mask=1, fixed=False, color=[-1, -1, -1])
        poly.state.pos=Vector3(coor_xyz[i,0],coor_xyz[i,1],coor_xyz[i,2])
        # poly.state.ori = Quaternion((0,0,1),45)
        # list_poly.append(poly)
        O.bodies.append(poly)

#O.bodies.append(list_poly)

O.bodies.append(
        polyhedra_utils.polyhedra(
                gravel,
                v=((-0.013,-0.150,-0.015), (-0.013,0.150,-0.015), (-2.257,0.150,1.868), (-2.257,-0.150,1.868), (0.000,-0.150,0.000), (0.000,0.150,0.000), (-2.245,0.150,1.883), (-2.245,-0.150,1.883)),
                fixed=True,
                color=(0.35, 0.35, 0.35)
        )
)

O.bodies.append(
        polyhedra_utils.polyhedra(
                gravel,
                v=((0.000,-0.160,0.000), (0.225,-0.160,0.268), (-2.020,-0.160,2.151), (-2.245,-0.160,1.883), (0.000,-0.150,0.000), (0.225,-0.150,0.268), (-2.020,-0.150,2.151), (-2.245,-0.150,1.883)),
                fixed=True,
                color=(0.35, 0.35, 0.35)
        )
)

O.bodies.append(
        polyhedra_utils.polyhedra(
                gravel,
                v=((0.000,0.150,0.000), (0.225,0.150,0.268), (-2.020,0.150,2.151), (-2.245,0.150,1.883), (0.000,0.160,0.000), (0.225,0.160,0.268), (-2.020,0.160,2.151), (-2.245,0.160,1.883)),
                fixed=True,
                color=(0.35, 0.35, 0.35)
        )
)

O.bodies.append(
        polyhedra_utils.polyhedra(
                gravel,
                v=((0.015,-0.150,-0.013), ( 0.015,0.150,-0.013), (0.272,0.150,0.294), (0.272,-0.150,0.294), (-0.000,-0.150,0.000), (0.000,0.150,0.000), (0.257,0.150,0.306), (0.257,-0.150,0.306)),
                fixed=True,
                color=(0.35, 0.35, 0.35)
        )
)

#O.bodies.append(utils.wall(0,axis=1,sense=1, material = gravel))
#O.bodies.append(utils.wall(0,axis=0,sense=1, material = gravel))
#O.bodies.append(utils.wall(0.3,axis=1,sense=-1, material = gravel))
#O.bodies.append(utils.wall(0.3,axis=0,sense=-1, material = gravel))

#polyhedra_utils.fillBox(( -2.002,-0.150,1.706), (-1.902,0.000,1.806), gravel, sizemin=[0.03, 0.03, 0.03], sizemax=[0.03, 0.03, 0.03], seed=4)

def checkUnbalancedI():
        print("iter %d, time elapsed %f,  time step %.5e, unbalanced forces = %.5f" % (O.iter, O.realtime, O.dt, utils.unbalancedForce()))


O.engines = [
        ForceResetter(),
        InsertionSortCollider([Bo1_Polyhedra_Aabb(), Bo1_Wall_Aabb(), Bo1_Facet_Aabb()]),
        InteractionLoop(
                [Ig2_Wall_Polyhedra_PolyhedraGeom(),
                 Ig2_Polyhedra_Polyhedra_PolyhedraGeom(),
                 Ig2_Facet_Polyhedra_PolyhedraGeom()],
                [Ip2_PolyhedraMat_PolyhedraMat_PolyhedraPhys()],  # collision "physics"
                [Law2_PolyhedraGeom_PolyhedraPhys_Volumetric()]  # contact law -- apply forces
        ),
        #GravityEngine(gravity=(0,0,-9.81)),
        NewtonIntegrator(damping=0.8, gravity=(0, 0, -9.81)),
        PyRunner(command='checkUnbalancedI()', realPeriod=5, label='checker'),
        VTKRecorder(virtPeriod=0.01,fileName='slot_polygon/slot-poly-',recorders=[])
]

# O.dt = 0.25 * polyhedra_utils.PWaveTimeStep()
O.dt = 0.000025
O.trackEnergy = True
O.saveTmp()

#from yade import qt
#qt.Controller()
#V = qt.View()
#V.screenSize = (800, 600)
#V.sceneRadius = 8
#V.eyePosition = (2, 0, 2)
#V.upVector = (0, 0, 1)
#V.lookAt = (-2, 0, 2)