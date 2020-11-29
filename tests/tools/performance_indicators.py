from geneticpython.tools.performance_indicators import *
import unittest
import math
import numpy as np

class PerformanceIndicators(unittest.TestCase):
    def test_hypervolume_2d(self):
        s = [[5, 2], [4, 3], [3, 4], [1, 10]]
        r = [6, 11]
        s = [[0.375, 0.08291787855333962], [0.275, 0.15979529634119613], [0.325, 0.09027472419873726], [0.45, 0.06315191376225904], [0.55, 0.055376284334288255], [0.475, 0.05776432540394618], [0.525, 0.057601454900038686], [0.4, 0.076899982994278], [0.425, 0.07651581021064964], [0.575, 0.04893823172437412], [0.225, 0.26029571463035367], [0.3, 0.11155085632421569], [0.35, 0.08466522010857935]]
        r = [1, 1]
        hv = HV_2d(s, r)
        self.assertEqual(hv, 26)

    def test_generational_distance(self):
        s = [[5, 2], [4, 3], [3, 4], [1, 10]]
        p = [[4.9, 1.9], [4.8, 1.95], [2, 3], [0, 9]]
        gd = GD(s, p)
        bfgd = 0
        for i in range(len(s)):
            min_r = float('inf')
            for j in range(len(p)):
                norm = 0
                for k in range(len(s[i])):
                    norm += (s[i][k] - p[j][k]) ** 2
                norm = math.sqrt(norm)
                min_r = min(min_r, norm)
            bfgd += np.power(min_r, 2)
        bfgd = np.power(bfgd, 1/2) / 4
        self.assertEqual(gd, bfgd)

    def test_inverted_generational_distance(self):
        s = [[5, 2], [4, 3], [3, 4], [1, 10]]
        p = [[4.9, 1.9], [4.8, 1.95], [2, 3], [0, 9]]
        igd = IGD(s, p)
        bfigd = 0
        for i in range(len(p)):
            min_r = float('inf')
            for j in range(len(s)):
                norm = 0
                for k in range(len(s[i])):
                    norm += (s[j][k] - p[i][k]) ** 2
                norm = math.sqrt(norm)
                min_r = min(min_r, norm)

            bfigd += np.power(min_r, 2)
        bfigd = np.power(bfigd, 1/2) / 4
        self.assertEqual(igd, bfigd)

if __name__ == '__main__':
    unittest.main()
