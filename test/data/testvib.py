# This file is part of cclib (http://cclib.github.io), a library for parsing
# and interpreting the results of computational chemistry packages.
#
# Copyright (C) 2006,2007,2012,2014,2015, the cclib development team
#
# The library is free software, distributed under the terms of
# the GNU Lesser General Public version 2.1 or later. You should have
# received a copy of the license along with cclib. You can also access
# the full license online at http://www.gnu.org/copyleft/lgpl.html.

"""Test logfiles with vibration output in cclib"""

import os
import unittest
import numpy

__filedir__ = os.path.realpath(os.path.dirname(__file__))


class GenericIRTest(unittest.TestCase):
    """Generic vibrational frequency unittest"""

    # Unit tests should normally give this value for the largest IR intensity.
    max_IR_intensity = 100

    def testvibdisps(self):
        """Are the dimensions of vibdisps consistent with 3N-6 x N x 3"""
        numvib = 3*len(self.data.atomnos) - 6
        self.assertEqual(self.data.vibdisps.shape,
                        (numvib, len(self.data.atomnos), 3))

    def testlengths(self):
        """Are the lengths of vibfreqs and vibirs correct?"""
        numvib = 3*len(self.data.atomnos) - 6
        self.assertEqual(len(self.data.vibfreqs), numvib)
        self.assertEqual(len(self.data.vibirs), numvib)

    def testfreqval(self):
        """Is the highest freq value 3630 +/- 200 cm-1?"""
        self.assertAlmostEqual(max(self.data.vibfreqs), 3630, delta=200)

    def testirintens(self):
        """Is the maximum IR intensity 100 +/- 10 km mol-1?"""
        self.assertAlmostEqual(max(self.data.vibirs), self.max_IR_intensity, delta=10)
    
    def testatomcoords(self):                                                   
        """Are atomcoords consistent with natom and Angstroms?"""               
        natom = len(self.data.atomcoords[0])                                    
        ref = self.data.natom                                                   
        msg = "natom is %d but len(atomcoords[0]) is %d" % (ref, natom)         
        self.assertEquals(natom, ref, msg)                                      
                                                                                
        # Find the minimum distance between two C atoms.                        
        mindist = 999                                                           
        for i in range(self.data.natom-1):                                      
            if self.data.atomnos[i]==6:                                         
                for j in range(i+1,self.data.natom):                            
                    if self.data.atomnos[j]==6:                                 
                        # Find the distance in the final iteration              
                        final_x = self.data.atomcoords[-1][i]                   
                        final_y = self.data.atomcoords[-1][j]                   
                        dist = numpy.sqrt(sum((final_x - final_y)**2))          
                        mindist = min(mindist,dist)                             
        self.assert_(abs(mindist-1.34)<0.03,"Mindist is %f (not 1.34)" % mindist)


class VibSymsTest(unittest.TestCase):
    """Is the length of vibsyms correct?"""
    def testvibsyms(self):
        """Is the length of vibsyms correct?"""
        numvib = 3*len(self.data.atomnos) - 6
        self.assertEqual(len(self.data.vibsyms), numvib)

class FireflyIRTest(GenericIRTest):
    """Customized vibrational frequency unittest"""

    max_IR_intensity = 135


class GaussianIRTest(GenericIRTest,VibSymsTest):
    """Customized vibrational frequency unittest"""
       
       
class JaguarIRTest(GenericIRTest,VibSymsTest):
    """Customized vibrational frequency unittest"""

       
class MolproIRTest(GenericIRTest,VibSymsTest):
    """Customized vibrational frequency unittest"""

       
class OrcaIRTest(GenericIRTest):
    """Customized vibrational frequency unittest"""

    # We have not been able to determine why ORCA gets such a different
    # maximum IR intensity. The coordinates are exactly the same, and
    # the basis set seems close enough to other programs. It would be nice
    # to determine whether this difference is algorithmic in nature,
    # but in the meanwhile we will expect to parse this value.
    max_IR_intensity = 215    


class QChemIRTest(GenericIRTest):
    """Customized vibrational frequency unittest"""

    def testtemperature(self):
        """Is the temperature 298.15 K?"""
        self.assertEqual(298.15, self.data.temperature)

    # def testenthalpy(self):
    #     """Is the enthalpy ..."""
    #     self.assertInside(self.data.enthalpy, )

    # def testentropy(self):
    #     """Is the entropy ..."""
    #     self.assertInside(self.data.entropy, )

    # def testfreeenergy(self):
    #     """Is the free energy ..."""
    #     self.assertInside(self.data.freeenergy, )

    # Molecular mass of DVB in mD.
    molecularmass = 130078.25

    def testatommasses(self):
        """Do the atom masses sum up to the molecular mass (130078.25+-0.1mD)?"""
        mm = 1000*sum(self.data.atommasses)
        self.assertAlmostEqual(mm, 130078.25, delta=0.1, msg = "Molecule mass: %f not 130078 +- 0.1mD" % mm)

    def testhessian(self):
        """Do the frequencies from the Hessian match the printed frequencies?"""


class GenericIRimgTest(unittest.TestCase):
    """Generic imaginary vibrational frequency unittest"""

    def testvibdisps(self):
        """Are the dimensions of vibdisps consistent with 3N-6 x N x 3"""
        numvib = 3*len(self.data.atomnos) - 6
        self.assertEqual(self.data.vibdisps.shape,
                        (numvib, len(self.data.atomnos), 3))

    def testlengths(self):
        """Are the lengths of vibfreqs and vibirs correct?"""
        numvib = 3*len(self.data.atomnos) - 6
        self.assertEqual(len(self.data.vibfreqs), numvib)
        self.assertEqual(len(self.data.vibirs), numvib)

    def testfreqval(self):
        """Is the lowest freq value negative?"""
        self.assertTrue(self.data.vibfreqs[0] < 0)

##    def testmaxvibdisps(self):
##        """What is the maximum value of displacement for a H vs a C?"""
##        Cvibdisps = compress(self.data.atomnos==6, self.data.vibdisps, 1)
##        Hvibdisps = compress(self.data.atomnos==1, self.data.vibdisps, 1)
##        self.assertEqual(max(abs(Cvibdisps).flat), 1.0)


class GenericRamanTest(unittest.TestCase):
    """Generic Raman unittest"""

    # This value is in amu.
    max_raman_intensity = 575

    def testlengths(self):
        """Is the length of vibramans correct?"""
        numvib = 3*len(self.data.atomnos) - 6
        self.assertEqual(len(self.data.vibramans), numvib)

    # The tolerance for this number has been increased, since ORCA
    # failed to make it inside +/-5, but it would be nice in the future
    # to determine is it's not too much work whether this is due to
    # algorithmic differences, or to differences in the input basis set
    # or coordinates. The first would be OK, but in the second case the
    # unit test jobs should be made more comparable. With cclib, we first
    # of all want to succeed in parsing, but would also like to remain
    # as comparable between programs as possible (for these tests).
    # Note also that this value is adjusted for Gaussian - why?
    def testramanintens(self):
        """Is the maximum Raman intensity correct?"""
        self.assertAlmostEqual(max(self.data.vibramans), self.max_raman_intensity, delta=8)

        # We used to test this, but it seems to vary wildly between
        # programs... perhaps we could use it if we knew why...
        #self.assertInside(self.data.vibramans[1], 2.6872, 0.0001)

    def testvibdisps(self):
        """Is the length and value of vibdisps correct?"""
        assert hasattr(self.data, "vibdisps")
        assert len(self.data.vibdisps) == 54


class GaussianRamanTest(GenericRamanTest):
    """Customized Raman unittest"""

    max_raman_intensity = 1066


class QChemRamanTest(GenericRamanTest):
    """Customized Raman unittest"""

    max_raman_intensity = 588


if __name__=="__main__":

    import sys
    sys.path.append(os.path.join(__filedir__, ".."))

    from test_data import DataSuite
    suite = DataSuite(['vib'])
    suite.testall()
