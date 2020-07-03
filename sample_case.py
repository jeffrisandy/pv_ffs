# import Module , don't delete!
from FFS import *

"""
DATA INPUT
"""
# import Module , don't delete!

from FFS import *
"""
DATA INPUT
"""
###############
# STATIC DATA #
###############

DATA = {
    'NAME': "AWT Separator B",
    'EQ_NO': "DRI-V-01020",
    'TAG_NO' : "8124.V.0701.B",
    'AREA' : "AWT 12 S",
    'SERIAL_NO' : "SBS-00807",
    'YEAR_BUILT' : 2008,
    'PV_ORIENTATION' : "Vertical", # vertical or horizaontal
    'MATERIAL' : "SA 516 Gr. 70",

    # dimension
    'OD' : 72, # inch, Outside Dia
    'L' : 113, # inch length / height of vessel

    # DESIGN DATA
    'DP' : 100, # psig, design pressure
    'DT' : 400, # F, design temp
    'CA' : 0.125, # inch, Corrosion Allowance
    'RT' : "SPOT",     # RT during design: FULL, PARTIAL
    

    # SHELL DATA
    'S_SHELL' : 20000, # SA 516 Gr 70
    'E_SHELL' : 0.85,
    'T_NOM_SHELL' : 0.3937, # inch

    # HEAD DATA
    'HEAD_TYPE' : "Ellipsoidal", # Ellipsoidal, Hemispherical, Torispherical, Flat
    'S_HEAD' : 20000, # SA 516 Gr 70
    'E_HEAD' : 1, # seamless head
    'T_NOM_HEAD' : 0.5, # inch,

    # factor K for ellipsoidal head 2:1
    'K' : 1,

    ###################
    # INSPECTION DATA #
    ###################
    # most inspection data is in milimeters unit

    ### INSPECTION INTERVAL ###
    'INTERVAL': 4, # YEARS AS PER CERTIFICATION

    ### INSPECTION DATE  ### 
    'insp_date_now' : "6/08/2019", # 7 Jan 2020
    'insp_date_prev' : "22/09/2016", # date/month/year  7 Jan 2017, type None if not availble

    ### SHELL ###
    't_nom_shell' : 10, # mm, nominal shell thick
    'shell_name': ['S1A', 'S1B', 'S2A', 'S2B', 'S3A', 'S3B', 'S4A', 'S4B'], # CML name
    't_now_shell': [8.72, 8.51, 8.76, 8.69, 8.61, 8.62, 8.866, 8.6 ], # in mm
    't_prev_shell': [9.35, 8.72, 9.56, 9.5, 9.02, 9.11, 9.16, 9 ], # in mm
    
    ### HEAD ###
    't_nom_head' : 12.8 , # mm, suggest to use max value of current inspection if actual thick > nominal thick
    'head1_name' : "TOP HEAD", # TOP / LEFT HEAD
    'head2_name' : "BOTTOM HEAD", # BOTTOM / RIGHT HEAD
 
    
    ### HEAD 1 : TOP OR LEFT HEAD ###
    'head_cml_name1': ['TH'], # CML name
    'head_area1' : ['knuckle'], # define head CML area in gead : knuckle or center
    't_now_head1': [ 10.81], # in mm
    't_prev_head1': [11.09], # in mm

    ### HEAD 2 : BOTTOM OR RIGHT HEAD ###
    'head_cml_name2': ['BH-A', 'BH-B'], # CML name
    'head_area2': ['knuckle', 'center'], # define head CML area in gead : knuckle or center
    't_now_head2': [ 11.56, 11.31],
    't_prev_head2': [11.76, 11.81],
    
    ### NOZZLES ###
    'S_NOZZLE' : 17100, # psi
    'E_NOZZLE' : 1, # seamless 
    'nozzles_name' : [ "N2", "N3", "N8", "MH"],
    'nozzles_size' : [ 6, 3, 3, 24 ], # NPS in inch

    # inch, height of nozzle location measured from top
    'nozzles_height': [10, 10, 90, 333], 

    # mm, nominal thick, mostly fabricated from shell plate,  
    # https://www.engineeringtoolbox.com/nominal-wall-thickness-pipe-d_1337.html
    'nozzles_thick_nom' : [11.31, 11.31, 11.38, 9.8], 

    # mm, min thick current inspection
    'nozzles_thick_now' : [11.11, 11.07, 11.32, 9.13], 

    # mm, min thick previous inspection or type None if not available e.q [None, None, None, None]
    'nozzles_thick_prev' : [10.2, 10.93, 10.98, 9.52] 
}

 

ffs = FFS(DATA)
ffs.summary()