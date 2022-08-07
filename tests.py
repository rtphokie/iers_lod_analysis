import unittest
from iers_lod import download, intToRoman, usno, plotit


class MyTestCase(unittest.TestCase):
    def test_dl(self):
        download(2022, 31)

    def test_records(self):
        df = usno()
        # df_rec=df[df['Bull. A LOD'] < -1.4]
        # print(df_rec[['Bull. A LOD']])
        rechigh=None
        reclow=None
        for n, row in df[['Bull. A LOD']].iterrows():
            if rechigh is None:
                rechigh=row['Bull. A LOD']
                reclow = row['Bull. A LOD']
            if rechigh < row['Bull. A LOD']:
                rechigh=row['Bull. A LOD']
                print(f"{n} HI {rechigh}")
            if reclow > row['Bull. A LOD']:
                reclow=row['Bull. A LOD']
                print(f"{n} LW {reclow}")

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

if __name__ == '__main__':
    unittest.main()
