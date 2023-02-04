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
import cx_Oracle


def signon(database_name):
    '''The signon function takes in a database name. It will prompt you
    to type in your username and password - then it'll attempt to connect
    to the database with those credentials.

    Parameters
    ----------
    database_name : STRING
        database name; user can type in 'cats', 'dogs', 'moose'

    Returns
    -------
    con : connection to Oracle database

    '''

    user = input('Please type in your username: ')
    pword = input('Please type in your password: ')

    if dbname == 'CATS':
        dbase = "CATS/KITTENS"
    elif dbname == 'DOGS':
        dbase = "DOGS/PUPPIES"
    elif dbname == 'MOOSE':
        dbase = "MOOSE/BABY MOOSE"
    else:
        raise ValueError(f'{database_name} is not a correct database name')
    try:
        con = cx_Oracle.connect(user, pword, dbase, encoding="UTF-8")
    except cx_Oracle.Error as error:
        print(error)
    return con


def notes_data_extraction(connection, max_size=100000):
    '''
    This function pulls data from the NOTES data table.

    Parameters
    ----------
    max_size : INTEGER
        Represents the maximum number of records to pull into df
        from SQL query. The default is 100000.

    Returns
    -------
    data : DATAFRAME
        Dataframe with all rows from NOTES

    '''

   NOTES_string = """SELECT NOTEDATE, NOTEID, NOTEIDTY,
                     NOTETXT, REFPER, USERID,
                     CASE WHEN NOTEIDTY = 'EST' THEN NOTEID END ID,
                     CASE WHEN NOTEIDTY = 'ENT' THEN NOTEID END PARENT_ID,
                     CASE WHEN NOTEIDTY = 'EIN' THEN NOTEID END EIN
                     FROM NOTES
                     WHERE REFPER = '2017'
                     AND NOTEID IS NOT NULL
                     """
    try:
        cur = connection.cursor()
        curexec = cur.execute(NOTES_string)

        # Set max data size:
        results = curexec.fetchmany(numRows=max_size)
        data = pd.DataFrame([list(i) for i in results],
                            columns=[i[0] for i in list(curexec.description)])

    except cx_Oracle.Error as error:
        print(error)

    return data


def trade_data_extraction(connection,
                          trade_vars="", trade_table="", max_size=100000):
    '''
    The data_extraction function appends additional filters through a basic SQL
    statement, allowing the user to quickly customize their SQL query based
    on trade team.

    Parameters
    ----------
    connection : Connection object of cx_Oracle module
        Use Signon function above to define connection object; use variable
        name here for Connection
    trade_vars : STRING, optional
        All variables unique to each trade. The default is "".
    trade_table : STRING, optional
        Name of trade table of interest in DATABASE (i.e. CATS_table).
        The default is "".
    max_size : INTEGER, optional
        Represents the maximum number of records to pull into dataframe
        from SQL query. The default is 100000.

    Returns
    -------
    data : DATAFRAME
        Dataframe with relevant rows from trade team of interest.

    '''

    trade_team_string = f"""SELECT {trade_vars}, BIG_PLACE, NAME1
                    , {trade_table}.USERID, NAICNEW
                    , STFIPS, STATE, ACTYFIPS, ID, PARENT_ID, EIN
                    , CONCAT("STFIPS", "ACTYFIPS") AS county_code, NOTESTAT
                    , SUBSTR(NAICNEW, 1, 4) AS four_dig_naics
                    ,{trade_table}.REFPER, REVIEWED
                    FROM TABLE.trade_table}
                    LEFT JOIN database.musers
                    ON {trade_table}.USERID = musers.USERID
                    WHERE {trade_table}.REFPER = '2017U1'
                    AND {trade_table}.TABSTAT = 'Y'"""

    try:
        cur = connection.cursor()
        curexec = cur.execute(trade_team_string)

        # Set max data size:
        results = curexec.fetchmany(numRows=max_size)
        data = pd.DataFrame([list(i) for i in results],
                            columns=[i[0] for i in list(curexec.description)])

    except cx_Oracle.Error as error:
        print(error)

    return data


def agg_filter_data_func(full_data, groupby_list, agg_dict):
    '''
    This takes in a dataframe, groups the dataframe by a list
    of variables, and runs various aggregate functions on columns of interest.
    Then, the function filters the df to only include groups equal to or
    with more than 10 estabs per group.

    Parameters
    ----------
    full_data : DATAFRAME
        Dataframe with relevant information from trade team of interest
    groupby_list : LIST
        list of variables to groupby
    agg_dict : DICTIONARY
        dictionary object where keys are the names of columns,
        values are the type of aggregation you want to do on
        the column (i.e. sum)

    Returns
    -------
    agg_filter_df : DATAFRAME
        Aggregate dataframe
    '''

    # assert statement checking if agg_dict has ID as a key
    assert agg_dict.get('ID'), "'ID' must be a key in agg_dict"
    full_data = full_data.groupby(groupby_list).agg(agg_dict)
    full_data.rename(columns={"ID": "ID_GROUP_CNT"}, inplace=True)
    agg_filter_df = full_data[full_data["ID_GROUP_CNT"] >= 10] \
        .reset_index()
    return agg_filter_df


def sods_func(geo_group_df, name1, name2, u=0.35, a=0.05, c=7):
    '''
    Function is based "Outlier Detection for the Manufacturing, Mining, and
    Construction Sectors in the 2012 Economic Census" by Nicole M. Czaplicki
    and Katherine J. Thompson, pages 3136-8. Paper can be accessed here:

    http://www.asasrms.org/Proceedings/y2013/files/309457_82715.pdf

    The sods function takes in a dataframe, two metrics, two parameters,
    and a threshold, and returns a dataframe with an indicator
    of whether the row is an outlier or not.

    Parameters:
    ----------
    geo_group_df : dataframe 
    name1 : ARRAY
        Numerator of ratio
    name2 : ARRAY
        Denominator of ratio
    U : INT
        Variable that allows us to control the importance placed on the
        magnitude of the data; will be a value between 0 and 1 where
        if U is closer to 1, more importance is given to the size of
        the estimate when identifying outliers. Default value is 0.35.
    A : INT
        Variable that helps keep D1SR, D3SR, D1ESR, and D3ESR from
        being overly sensitive threshold. Default value is 0.05.
    C : INT
        arbitrary threshold, here any score above threshold will be
        deemed an outlier. Default value is 7.

    Returns:
    ----------
    geo_group_df : DATAFRAME
        Dataframe with additional indicator columns tagging each cell as
        an outlier (1) or not an outlier (0)
    '''
    if geo_group_df.shape[0] <= 10:
        unique_outlier_indicator = f'outlier_ind_{name1}_{name2}'
        geo_group_df[unique_outlier_indicator] = 0
        return geo_group_df

    else:
        # calculate Standardized Ratio (SR), centering distribution around 0
        metric_1 = np.array(geo_group_df[name1])  # numerator of target ratio
        metric_2 = np.array(geo_group_df[name2])  # denominator of target ratio

        target_ratio = metric_1/metric_2

        sr = np.where(target_ratio >= np.nanmedian(target_ratio),
                      (target_ratio/np.nanmedian(target_ratio))-1,
                      1-(np.nanmedian(target_ratio)/target_ratio))

        # calculate the Ratio Effect (ESR), a transformation that allows us to
        # control the importance placed on magnitude of the data using
        # parameter U
        sr_max = np.max([metric_1, metric_2*np.nanmedian(target_ratio)],
                        axis=0)
        sr_u = np.power(sr_max, u)

        esr = sr * sr_u

        # calculate quantiles for SR
        [sr_q1, sr_median, sr_q3] = np.nanpercentile(sr, [25, 50, 75])

        # calculate quantiles for ESR
        [esr_q1, esr_median, esr_q3] = np.nanpercentile(esr, [25, 50, 75])

        # calculate ratio deviation for SR
        d1sr = max((sr_median - sr_q1), abs(a*sr_median))
        d3sr = max((sr_q3 - sr_median), abs(a*sr_median))

        # calculate ratio deviation for ESR
        d1esr = max((esr_median-esr_q1), abs(a*sr_median))
        d3esr = max((esr_q3-esr_median), abs(a*esr_median))

        # calculate QSR, which indicates how far the estimate is from the
        # median relative to D1SR and D3SR
        QSR = np.where(sr > sr_median, ((sr - sr_median)/d3sr),
                       ((sr_median - sr)/d1sr))

        # calculate QSER, which indicates how far the estimate is
        # from the median relative to D1ESR and D3ESR
        QESR = np.where(esr > esr_median,
                        ((esr - esr_median)/d3esr),
                        ((esr_median - esr)/d1esr))

        # create indicator variable where 1 = outlier, 0 = not an outlier
        unique_outlier_indicator = f'outlier_ind_{name1}_{name2}'
        geo_group_df[unique_outlier_indicator] = np.where((abs(QESR) > c) &
                                                          (abs(QSR) > c),
                                                          1, 0)

        return geo_group_df


def save_excel_file(filename, state_sheet, county_sheet, estab_county_sheet,
                    estab_state_sheet, note_sheet):
    '''
    The save_excel_file function takes in the name of the file, as well as 4
    dataframes, and saves the file to your computer. Note that nothing is
    returned in the python console.

    Parameters:
        filename = string that includes filename. Must end with .xlsx
        [i.e. 'good_morning.xlsx']
        state_sheet = name of dataframe containing state related data
        county_sheet = name of dataframe containing county related data
        estab_sheet = name of dataframe containing estab related data
        note_sheet = name of dataframe containing note related data

    Returns:
        None

    '''
    writer = pd.ExcelWriter(f'{filename}')
    state_sheet.to_excel(writer, sheet_name='State')
    county_sheet.to_excel(writer, sheet_name='County')
    estab_county_sheet.to_excel(writer, sheet_name='Estab_by_county')
    estab_state_sheet.to_excel(writer, sheet_name='Estab_by_state')
    note_sheet.to_excel(writer, sheet_name='Notes')
    writer.save()
