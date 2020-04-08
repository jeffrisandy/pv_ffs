import pandas as pd
import numpy as np
import datetime
from IntegrityAnalysis import IntegrityAnalysis
from Vessel import *


class FFS():
    def __init__(self, data):
        print(f"""
    =======================
    DATA CONSTRUCTION NOTES
    =======================""")
        self.shell = Shell(data)
        self.head1 = Head(data, label="head1")
        self.head2 = Head(data, label="head2")

        # init nozzles
        nozzleIDS = data['nozzles_name']
        sizes = data['nozzles_size']
        heights = data['nozzles_height']
        tNoms = data['nozzles_thick_nom']
        tNows = data['nozzles_thick_now']
        tPrevs = data['nozzles_thick_prev']
        S = data['S_NOZZLE']
        E = data['E_NOZZLE']

        self.nozzles = dict()
        zippis = zip(nozzleIDS, sizes, heights, tNoms, tNows, tPrevs)

        for nozzleID, size, height, tNom, tNow, tPrev in list(zippis):
            self.nozzles[nozzleID] = Nozzle(data, nozzleID, size, height, tNom, tNow, tPrev, S, E)

    def to_dataframe(self):
        rls = []
        mawps = []
        labels = []
        isFits = []

        sections = [self.shell, self.head1, self.head2]
        for k, v in self.nozzles.items():
            sections.append(v)
        for section in sections:
            rl = section.rl
            mawp = section.calc_mawp()
            label = section.part_name
            fit = section.isFit()
            rls.append(rl)
            mawps.append(mawp)
            labels.append(label)
            isFits.append(fit)

        df = pd.DataFrame()
        df['Section'] = labels
        df['RL'] = rls
        df['MAWP'] = mawps
        df['is_Fit?'] = isFits

        return df

    def summary(self):
        print(f"""
    ====================
    INTEGRITY EVALUATION
    ====================

    NAME            = {self.shell.DATA['NAME']}
    TAG NO          = {self.shell.DATA['TAG_NO']}
    AREA            = {self.shell.DATA['AREA']}
    ORIENTATION     = {self.head1.DATA['PV_ORIENTATION']}
    HEAD TYPE       = {self.head1.DATA['HEAD_TYPE']}
    OUTSIDE DIA     = {self.shell.OD} inch
    LENGTH          = {self.head1.L} inch
    DESIGN PRESSURE = {self.shell.DP} psig
    DESIGN TEMP     = {self.shell.DATA['DT']} F
    YEAR BUILT      = {self.shell.year_built}
    INSPECTION DATE = {self.shell.date_now}

    == EVALUATION SUMMARY ==
    """)
        print(self.to_dataframe())
        print("""
    ----------------
    SECTION - SHELL
    ----------------""")
        self.shell.print_summary()
        print(f"""
    --------------------------
    SECTION - HEAD 1 {self.head1.part_name}
    --------------------------""")
        self.head1.print_summary()
        print(f"""
    ------------------------------
    SECTION - HEAD 2 {self.head2.part_name}
    ------------------------------""")
        self.head2.print_summary()
        for k, v in self.nozzles.items():
            print(F"""
    -------------
    NOZZLE - {k}
    -------------""")
            v.print_summary()