"""
* COSMIC - GALAXY
* Version 3 
@ Yaël Moussouni
@ Unistra, P&E, MSc1-MoFP
@ Observatory of Strasbourg (Intern)
"""

import numpy as np
import matplotlib.pyplot as plt
import amuse.units.units as u
from amuse.ext.galactic_potentials import MWpotentialBovy2015

MilkyWay_Bovy2015 = MWpotentialBovy2015
class MilkyWay_AMUSE(object):
    # THIS IS A COPY OF https://github.com/amusecode/amuse/blob/cdd21cc5cb06e40ccf5ecb86d513d211634e2689/examples/textbook/solar_cluster_in_galaxy_potential.py#L37

    def __init__(self, Mb=1.40592e10| u.MSun,
                 Md=8.5608e10| u.MSun,
                 Mh=1.07068e11 | u.MSun  ):
        self.Mb= Mb
        self.Md= Md
        self.Mh= Mh

    def get_potential_at_point(self,eps,x,y,z):
        r=(x**2+y**2+z**2)**0.5
        R= (x**2+y**2)**0.5
        # buldge
        b1= 0.3873 |u.kpc
        pot_bulge= -u.constants.G*self.Mb/(r**2+b1**2)**0.5 
        # disk
        a2= 5.31 |u.kpc
        b2= 0.25 |u.kpc
        pot_disk = \
            -u.constants.G*self.Md/(R**2 + (a2+ (z**2+ b2**2)**0.5 )**2 )**0.5
        #halo
        a3= 12.0 |u.kpc
        cut_off=100 |u.kpc
        d1= r/a3
        c=1+ (cut_off/a3)**1.02
        pot_halo= -u.constants.G*(self.Mh/a3)*d1**1.02/(1+ d1**1.02) \
                  - (u.constants.G*self.Mh/(1.02*a3))\
                      * (-1.02/c +numpy.log(c) + 1.02/(1+d1**1.02) \
                           - numpy.log(1.0 +d1**1.02) )
        return 2*(pot_bulge+pot_disk+ pot_halo) # multiply by 2 because it
    						# is a rigid potential

       
    def get_gravity_at_point(self, eps, x,y,z): 
        r= (x**2+y**2+z**2)**0.5
        R= (x**2+y**2)**0.5
        #bulge
        b1= 0.3873 |u.kpc
        force_bulge= -u.constants.G*self.Mb/(r**2+b1**2)**1.5 
        #disk
        a2= 5.31 |u.kpc
        b2= 0.25 |u.kpc
        d= a2+ (z**2+ b2**2)**0.5
        force_disk=-u.constants.G*self.Md/(R**2+ d**2 )**1.5
        #halo
        a3= 12.0 |u.kpc
        d1= r/a3
        force_halo= -u.constants.G*self.Mh*d1**0.02/(a3**2*(1+d1**1.02))
       
        ax= force_bulge*x + force_disk*x  + force_halo*x/r
        ay= force_bulge*y + force_disk*y  + force_halo*y/r
        az= force_bulge*z + force_disk*d*z/(z**2 + b2**2)**0.5 + force_halo*z/r 

        return ax,ay,az

    def vel_circ(self, r ):
        z=0 | u.kpc 
        b1= 0.3873 |u.kpc
        a2= 5.31 |u.kpc
        b2= 0.25 |u.kpc
        a3= 12.0 |u.kpc

        rdphi_b = u.constants.G*self.Mb*r**2/(r**2+b1**2)**1.5
        rdphi_d =u.constants.G*self.Md*r**2/(r**2+(a2+(z**2+b2**2)**0.5)**2 )**1.5
        rdphi_h = u.constants.G*self.Mh*(r/a3)**0.02*r/(a3**2*(1+(r/a3)**1.02))

        vel_circb =  rdphi_b
        vel_circd = rdphi_d
        vel_circh = rdphi_h

        return (vel_circb+ vel_circd+ vel_circh)**0.5 

    def stop(self):
        return
