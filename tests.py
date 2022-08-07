import unittest
from iers_lod import download, intToRoman, usno, plotit


class MyTestCase(unittest.TestCase):
    def test_dl(self):
        download(2022, 31)

    def test_usno_finals(self):
        df = usno()
        import datetime
        plotit(df, start=datetime.datetime(2019,1,1), trend=False, filename='LOD2020on.png')
        plotit(df, start=datetime.datetime(1972,1,1), trend=True, filename='LODall.png')

    def test_roman_numerals(self):
        data = {'100': 'C',
                '1000': 'M',
                '1010': 'MX',
                '35': 'XXXV',
                }
        for i, r1 in data.items():
            r2 = intToRoman(int(i))
            self.assertEqual(r1, r2, f'for {i} expected {r1} got {r2}')

    def testjkl(self):
        import matplotlib.pyplot as plt
        import numpy as np
        from scipy.interpolate import interp1d

        x = np.linspace(0, 10, num=11, endpoint=True)
        y = np.cos(-x ** 2 / 9.0)
        f1 = interp1d(x, y, kind='nearest')
        f2 = interp1d(x, y, kind='zero')
        f3 = interp1d(x, y, kind='quadratic')

        xnew = np.linspace(0, 10, num=1001, endpoint=True)
        plt.plot(x, y, 'o')
        plt.plot(xnew, f1(xnew), '-', xnew, f2(xnew), '--', xnew, f3(xnew), ':')
        plt.legend(['data', 'nearest', 'zero', 'quadratic'], loc='best')
        plt.show()


if __name__ == '__main__':
    unittest.main()
