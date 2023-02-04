# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 10:41:56 2022

@author: Sarah Scott

The Census Bureau has reviewed this data product to ensure appropriate access,
use, and disclosure avoidance protection of the confidential source data used
to produce this product (Data Management System (DMS) number: P-7504847,
subproject P-7514952, Disclosure Review Board (DRB) approval number:
CBDRB-FY22-EWD001-006).
"""
import pandas as pd
import numpy as np
from functions import signon, notes_data_extraction, \
    trade_data_extraction, agg_filter_data_func, sods_func, save_excel_file

# connect to database
conn = signon('CATS')

# Pull data from mnotepad
notes_tab = notes_data_extraction(conn, max_size=200000)

# Pull and manipulate data for manufacturing dashboard
MANUF_TRADE_VARS = """PAYANN, CSTMTOT, RCPTOT,
                      PAYANPW, INVTOTE, CEXTOT, INVTOTB,
                      (PAYANN + CSTMTOT) AS PAYANN_and_CSTMTOT"""

full_2017_manuf_data = trade_data_extraction(conn,
                                             trade_vars=MANUF_TRADE_VARS,
                                             trade_table="kitten_table",
                                             max_size=400000)

# close connection to oracle database
conn.close()

# import significance level spreadsheet, merge with manuf data
manuf_sig_df = pd.read_excel(r'filepath\ratio_output.xlsx')
manuf_sig_df_filtered = manuf_sig_df[['ID', 'Significance']]

full_2017_manuf_data = full_2017_manuf_data \
    .merge(manuf_sig_df_filtered, how='left', on='ID')

full_2017_manuf_data['Significance'] \
    .fillna(value=np.random.randint(1, 5), inplace=True)

# create list of tuples where each tuple contains target ratio num. and denom.
list_of_manuf_ratios = [('PAYANN', 'ratio_2'),
                        ('CSTMTOT', 'RCPTOT'),
                        ('PAYANN_AND_CSTMTOT', 'RCPTOT'),
                        ('new_ratio', 'second_new_ratio'),
                        ('old_ratio', 'new_ratio'),
                        ('new ratio', 'old_ratio'),
                        ('old_ratio', 'brand_new_ratio'),
                        ('INVTOTE', 'RCPTOT'),
                        ('CEXTOT', 'RCPTOT')]

# State level: groupby FOUR_DIG_NAICS and State; return aggregate dataframe
manuf_agg_dict = {'ID': 'count',
                  'PAYANN': 'sum',
                  'ratio_7': 'sum',
                  'CSTMTOT': 'sum',
                  'RCPTOT': 'sum',
                  'ratio_17': 'sum',
                  'new_ratio': 'sum',
                  'PAYANPW': 'sum',
                  'INVTOTE': 'sum',
                  'CEXTOT': 'sum',
                  'INVTOTB': 'sum',
                  'PAYANN_AND_CSTMTOT': 'sum'}

manuf_state_groupby_list = ['FOUR_DIG_NAICS', 'STATE']
manuf_state_level_scores = agg_filter_data_func(full_2017_manuf_data,
                                                manuf_state_groupby_list,
                                                manuf_agg_dict)

# run SODS function for target ratios
for ratio in list_of_manuf_ratios:
    manuf_state_level_scores = manuf_state_level_scores \
        .groupby('FOUR_DIG_NAICS') \
        .apply(sods_func, name1=ratio[0], name2=ratio[1], u=0.35, a=0.05, c=7)

# M County level: groupby FOUR_DIG_NAICS, COUNTY_CODE; return aggregate df
manuf_county_groupby_list = ['FOUR_DIG_NAICS', 'STATE', 'COUNTY_CODE']
manuf_county_data_agg = agg_filter_data_func(full_2017_manuf_data,
                                             manuf_county_groupby_list,
                                             manuf_agg_dict)

# keep (NAICS+COUNTY) groups with at least 10 counties
manuf_county_level_scores = manuf_county_data_agg \
    .groupby(['FOUR_DIG_NAICS', 'STATE']) \
    .filter(lambda x: len(x) >= 10)

# run SODS function for target ratios
for ratio in list_of_manuf_ratios:
    manuf_county_level_scores = manuf_county_level_scores \
     .groupby(['FOUR_DIG_NAICS', 'STATE']) \
     .apply(sods_func, name1=ratio[0], name2=ratio[1], u=0.35, a=0.05, c=7)

# run SODS function on individual establishments grouped by county_code
manuf_estab_level_county_group_scores = full_2017_manuf_data.copy()

for ratio in list_of_manuf_ratios:
    manuf_estab_level_county_group_scores = \
        manuf_estab_level_county_group_scores \
        .groupby(['FOUR_DIG_NAICS', 'COUNTY_CODE']) \
        .apply(sods_func, name1=ratio[0], name2=ratio[1], u=0.35, a=0.05, c=7)

# run SODS function on individual establishments grouped by state
manuf_estab_level_state_group_scores = full_2017_manuf_data.copy()

for ratio in list_of_manuf_ratios:
    manuf_estab_level_state_group_scores = \
        manuf_estab_level_state_group_scores \
        .groupby(['FOUR_DIG_NAICS', 'STATE']) \
        .apply(sods_func, name1=ratio[0], name2=ratio[1], u=0.35, a=0.05, c=7)

# save manuf state, county, estab level scores to excel
save_excel_file('final_excel_data.xlsx', manuf_state_level_scores,
                manuf_county_level_scores,
                manuf_estab_level_county_group_scores,
                manuf_estab_level_state_group_scores,
                mnotepad_tab)
