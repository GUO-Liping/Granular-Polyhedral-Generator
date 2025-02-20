# -*- encoding=utf-8 -*-
from yade import plot, pack, polyhedra_utils

gravel = PolyhedraMat()
gravel.density = 2800  #kg/m^3
gravel.young = 1E7  #Pa
gravel.poisson = 20000 / 1E7
gravel.frictionAngle = 0.294  #rad

steel = PolyhedraMat()
steel.density = 7850  #kg/m^3
steel.young = 10 * gravel.young
steel.poisson = gravel.poisson
steel.frictionAngle = 0.4  #rad

rubber = PolyhedraMat()
rubber.density = 1000  #kg/m^3
rubber.young = gravel.young / 10
rubber.poisson = gravel.poisson
rubber.frictionAngle = 0.7  #rad

frictMat = FrictMat(young=1e9, poisson=.2)

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

# polyhedra_utils.fillBox(( -1.665,-0.135,1.423), (-1.873,0.135,1.859), gravel, sizemin=[0.025, 0.025, 0.025], sizemax=[0.05, 0.05, 0.05], seed=4)
# polyhedra_utils.fillBox(( -2.002,-0.150,1.706), (-1.902,0.000,1.806), gravel, sizemin=[0.03, 0.03, 0.03], sizemax=[0.03, 0.03, 0.03], seed=5)

sp = pack.SpherePack()
# do not use periodic=True
sp.makeCloud((-1.989,-0.135,1.541),(-1.549,0.135,1.741),rMean=0.014, rRelFuzz=0.5, periodic=False)
sp.rotate((0,1,0),2*pi/9)
#sp.translate((0,0,-2))
#sp.toSimulation(rot=Quaternion((0,1,0),2*pi/9))
sp.toSimulation()


def checkUnbalancedI():
	print("iter %d, time elapsed %f,  time step %.5e, unbalanced forces = %.5f" % (O.iter, O.realtime, O.dt, utils.unbalancedForce()))


O.engines = [
        ForceResetter(),
        InsertionSortCollider([Bo1_Polyhedra_Aabb(), Bo1_Sphere_Aabb()]),
        InteractionLoop(
                [Ig2_Sphere_Polyhedra_ScGeom(), Ig2_Sphere_Sphere_ScGeom()],
                [Ip2_FrictMat_PolyhedraMat_FrictPhys(),Ip2_FrictMat_FrictMat_FrictPhys()],  # collision "physics"
                [Law2_ScGeom_FrictPhys_CundallStrack()]  # contact law -- apply forces
        ),
        #GravityEngine(gravity=(0,0,-9.81)),
        NewtonIntegrator(damping=0.3, gravity=(0, 0, -9.81)),
        PyRunner(command='checkUnbalancedI()', realPeriod=5, label='checker')
]

#O.dt=0.25*polyhedra_utils.PWaveTimeStep()
O.dt = 0.0025 * polyhedra_utils.PWaveTimeStep()

from yade import qt
qt.Controller()
V = qt.View()
V.screenSize = (550, 450)
V.sceneRadius = 1
V.eyePosition = (0.7, 0.5, 0.1)
V.upVector = (0, 0, 1)
V.lookAt = (0.15, 0.15, 0.1)
