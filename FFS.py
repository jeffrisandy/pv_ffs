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
        self.DATA = data
        
        # init Shell
        shell_name = data['shell_name']
        shell_tNow = data['t_now_shell']
        shell_tPrev = data['t_prev_shell']
        self.shells = dict()
        shell_zip = zip(shell_name, shell_tNow, shell_tPrev)
        for name, tNow, tPrev in list(shell_zip):
            self.shells[name] = Shell(data, name, tNow, tPrev)
            
         # init head1 = top or left head
        head_name1 = data['head_cml_name1']
        head_tNow1 = data['t_now_head1']
        head_tPrev1 = data['t_prev_head1']
        head_area1 = data['head_area1']
        self.heads1 = dict()
        head_zip1 = zip(head_name1, head_tNow1, head_tPrev1, head_area1)
        for name, tNow, tPrev, head_area in list(head_zip1):
            self.heads1[name] = Head(data, name, tNow, tPrev, head_area, label="head1")
                          
       # init head2 = bottom or right head
        head_name2 = data['head_cml_name2']
        head_tNow2 = data['t_now_head2']
        head_tPrev2 = data['t_prev_head2']
        head_area2 = data['head_area2']
        self.heads2 = dict()
        head_zip2 = zip(head_name2, head_tNow2, head_tPrev2, head_area2)
        for name, tNow, tPrev, head_area in list(head_zip2):
            self.heads2[name] = Head(data, name, tNow, tPrev, head_area, label="head2")
        
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
        labels = [] #section
        cml_names = []
        isFits = []

        sections = []
        
        for k, v in self.shells.items():
            sections.append(v)
        for k, v in self.heads1.items():
            sections.append(v)
        for k, v in self.heads2.items():
            sections.append(v)
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
            cml_names.append(section.cml_name)
            isFits.append(fit)

        df = pd.DataFrame()
        df['Section'] = labels
        df['CML'] = cml_names
        df['RL'] = rls
        df['MAWP'] = mawps
        df['is_Fit?'] = isFits

        return df

    def summary(self):
        print(f"""
    ====================
    INTEGRITY EVALUATION
    ====================

    NAME            = {self.DATA['NAME']}
    EQ NO           = {self.DATA['EQ_NO']}
    TAG NO          = {self.DATA['TAG_NO']}
    AREA            = {self.DATA['AREA']}
    ORIENTATION     = {self.DATA['PV_ORIENTATION']}
    HEAD TYPE       = {self.DATA['HEAD_TYPE']}
    OUTSIDE DIA     = {self.DATA['OD']} inch
    LENGTH          = {self.DATA['L']} inch
    DESIGN PRESSURE = {self.DATA['DP']} psig
    DESIGN TEMP     = {self.DATA['DT']} F
    MATERIAL        = {self.DATA['MATERIAL']}
    RT              = {self.DATA['RT']}
    YEAR BUILT      = {self.DATA['YEAR_BUILT']}
    INSPECTION DATE = {self.DATA['insp_date_now']}

    == EVALUATION SUMMARY ==
    """)
        print(self.to_dataframe())
        print("""
    ----------------
    SECTION - SHELL
    ----------------""")
        for k,v in self.shells.items():
            print(f"""
    -------------
    SHELL - {k}
    -------------""")
            v.print_summary()
        
        print(f"""
    --------------------------
    SECTION - HEAD 1 {self.DATA['head1_name']}
    --------------------------""")
        for k,v in self.heads1.items():
            print(f"""
    -------------
    HEAD 1 - {self.DATA['head1_name']} - {k}
    -------------""")
            v.print_summary()
 
        print(f"""
    ------------------------------
    SECTION - HEAD 2 {self.DATA['head2_name']}
    ------------------------------""")
        for k,v in self.heads2.items():
            print(f"""
    -------------
    HEAD 2 - {self.DATA['head2_name']} - {k}
    -------------""")
            v.print_summary()
            
        for k, v in self.nozzles.items():
            print(f"""
    -------------
    NOZZLE 2 - {k}
    -------------""")
            v.print_summary()