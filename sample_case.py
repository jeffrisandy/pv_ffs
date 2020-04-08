# import Module , don't delete!
from FFS import *

"""
DATA INPUT
"""
###############
# STATIC DATA #
###############

DATA = {
    'NAME': 'Test Fluid Heater Treater Vessel (GAUGING SEPARATOR B)',
    'TAG_NO': '6105-E-580-22-01',
    'AREA': 'AWT SW4',
    'SERIAL_NO': '353SW-ZV-01C',
    'YEAR_BUILT': 1987,
    'PV_ORIENTATION': 'Vertical',  # vertical or horizontal
    'MATERIAL': 'SA-516-70',

    # dimension
    'OD': 96,  # inch, Outside Dia
    'L': 590,  # inch length / height of vessel

    # DESIGN DATA
    'DP': 100,  # psig, design pressure
    'DT': 250,  # F, design temp
    'CA': 0.0625,  # inch, Corrosion Allowance
    'RT': 'Full',  # RT during design: FULL, PARTIAL

    # SHELL DATA
    'S_SHELL': 20000,  # SA 516 Gr 70
    'E_SHELL': 1,
    'T_NOM_SHELL': 0.375,  # inch

    # HEAD DATA
    'HEAD_TYPE': 'Ellipsoidal',  # Ellipsoidal, Hemispherical, Torispherical, Flat
    'S_HEAD': 20000,  # SA 516 Gr 70
    'E_HEAD': 1,
    'T_NOM_HEAD': 0.375,  # inch,

    # factor K for ellipsoidal head 2:1
    'K': 1,

    ###################
    # INSPECTION DATA #
    ###################
    # most inspection data is in milimeters unit

    ### INSPECTION INTERVAL ###
    'INTERVAL': 4,  # YEARS AS PER CERTIFICATION

    ### NOW  ###
    'insp_date_now': '07/01/2020',  # 7 Jan 2020

    # SHELL
    't_nom_shell': 9.525,  # mm, nominal shell thick
    't_now_shell': 7.35,  # mm, min thick in shell from current inspection data

    # HEAD
    't_nom_head': 9.525,  # mm, suggest to use max value of current inspection if actual thick > nominal thick
    'head1_name': 'Top Head',  # TOP / LEFT HEAD
    't_now_head1': 10.38,  # mm, min  top/left head thick of current inspection

    'head2_name': 'Bottom Head',  # BOTTOM / RIGHT HEAD
    't_now_head2': 11.07,  # mm, min bottom/right head thick of current inspection

    ### PREVIOUS ###
    ## If data is not available, type  None for all field

    'insp_date_prev': '28/10/2016',  # date/month/year  7 Jan 2017, type None if not availble

    # SHELL
    't_prev_shell': 8.52,  # mm, min thick shell of previous inspection data, or type None if not available

    # HEAD
    't_prev_head1': 9.69,  # mm, top / left head, type None if not available
    't_prev_head2': 10.84,  # mm,   bottom /right head, type None if not available

    ### NOZZLES ###
    'S_NOZZLE': 20000,  # psi
    'E_NOZZLE': 1,
    'nozzles_name': ['N1', 'N2', 'N3', 'N4', 'N12', 'N13', 'MH1', 'MH2', 'MH3'],
    'nozzles_size': [3, 4, 3, 4, 4, 3, 26, 24, 26],  # NPS in inch

    # inch, height of nozzle location measured from top
    'nozzles_height': [90, 0, 352, 146, 146, 266, 352, 90, 352],

    # mm, nominal thick, mostly fabricated from shell plate,
    # https://www.engineeringtoolbox.com/nominal-wall-thickness-pipe-d_1337.html
    'nozzles_thick_nom': [0.3, 0.337, 0.3, 0.337, 0.337, 0.119, 0.375, 0.375, 0.375],

    # mm, min thick current inspection
    'nozzles_thick_now': [7.02, 9.9, 7.63, 8.85, 8.61, 8.74, 8.13, 9.92, 9.73],

    # mm, min thick previous inspection or type None if not available e.q [None, None, None, None]
    'nozzles_thick_prev': [6.75, 8.20, 7.14, 8.10, 7.98, None, None, None, None]
}

ffs = FFS(DATA)
ffs.summary()