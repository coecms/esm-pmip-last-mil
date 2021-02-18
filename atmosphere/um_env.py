vars = {
'AINITIAL': '',
'ASTART': 'INPUT/pre-industrial.astart', 
'AUSCOM_CPL': 'true',
'DATAW': '{work_path}',
'FASTRUN': 'true',
'IDEALISE': '',
'PAREXE': 'parexe',
'PRINT_STATUS': 'PrStatus_Diag',
'RPSEED': '',
'RUNID': 'PI-01',
'TYPE': 'NRUN',
'UM_ATM_NPROCX': '4',
'UM_ATM_NPROCY': '5',
'UM_NAM_MAX_SECONDS': '300',
'UM_NPES': '20',
'UM_SECTOR_SIZE': '2048',
'UM_STDOUT_FILE': 'atm.fort6.pe',
'VN' : '7.3',

# Config input paths
'UNIT01': '',
'UNIT02': 'prefix',
'UNIT04': 'STASHC', 
'UNIT05': 'namelists',
'UNIT07': 'PI-01.out2',
'UNIT08': '/dev/null',
'UNIT09': 'CONTCNTL',
'UNIT10': 'xhist',
'UNIT11': 'ihist', 
'UNIT12': 'thist',
'UNIT14': 'errflag',
'UNIT15': '',
'UNIT58': '',
'UNIT22': 'INPUT/STASHmaster',
'UNIT57': 'INPUT/spec3a_sw_hadgem1_6on',
'UNIT80': 'INPUT/spec3a_lw_hadgem1_6on',
'STASETS_DIR': 'INPUT/stasets',
'VERT_LEV': 'INPUT/vertlevs_G3',

# Ancillary files
'ARCLBIOG': 'INPUT/biogenic_351sm.N96L38',
'BIOMASS': 'INPUT/Bio_1850_ESM1.anc',
'CHEMOXID': 'INPUT/sulpc_oxidants_N96_L38',
'DMSCONC': 'INPUT/DMS_conc.N96',
'NDEPFIL': 'INPUT/Ndep_1850_ESM1.anc',
'OCFFEMIS': 'INPUT/OCFF_1850_ESM1.anc',
'OZONE': 'INPUT/ozone_1850_ESM1.anc',
'SOOTEMIS': 'INPUT/BC_hi_1850_ESM1.anc',
'SULPEMIS': 'INPUT/scycl_1850_ESM1_v4.anc',
'VEGINIT': 'INPUT/cable_vegfunc_N96.anc',
}

import mule

# Current date according to the UM
mf = mule.load_umfile('work/atmosphere/restart_dump.astart')
year = mf.fixed_length_header.t2_year

print(f"Updating ozone for year {year}")

if year <= 850:
    ozone = 'ozone_esm_pmip_0850-0850.anc'
elif year <= 1050:
    ozone = 'ozone_esm_pmip_0851-1050.anc'
elif year <= 1250:
    ozone = 'ozone_esm_pmip_1051-1250.anc'
elif year <= 1450:
    ozone = 'ozone_esm_pmip_1251-1450.anc'
elif year <= 1650:
    ozone = 'ozone_esm_pmip_1451-1650.anc'
elif year <= 1850:
    ozone = 'ozone_esm_pmip_1651-1850.anc'

vars['OZONE'] = 'INPUT/' + ozone
