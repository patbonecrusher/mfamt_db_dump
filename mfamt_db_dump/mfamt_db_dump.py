print("Hello from mfamt_db_dump!")

import pandas as pd
import sqlite3
import datetime
from person import Person, parse_person


# ZCONCLUSIONTYPE1: 
#       149 baptism?
#       148 immigration?
#       144 place of residance?
#
#
#
# ZPERSON1: relation
# ZASSIGNEDPLACE: id of where something happened

# Z_ENT (defined in ZPRIMARYKEY table)
#   23 events
#   24 family events (3 - 4) (Event field? notes or description)
#   25 person events
#   15 persons
#   28 locations
#   14 famillies (MEN and WOMEN)
#   11 source
#   18 medias-pdfs
#   19 medias-pictures
#   22 Dnas
#   6  Text
#   27 occupations?
#   29 story
#   9?  Not sure but only 1 entry
#   31 todos
#   32 ? Seems related to sources

# ZCHILDRELATION
#   child id mapped to familly id

# ZCOORDINATE
#   coordinate for locations

# ZLABEL
#   labels

# ZLABELRELATION
#   Relation to Baseobject

# ZMEDIARELATION
#   Relation with media

# ZTODORELATION
#   Relations with todo



# 1688 - pat

def save_blob(blob, fname):
    print(f'{fname=}')
    with open(fname, 'wb') as f:
        f.write(blob)
    
def dump_conclusion_type(con):
    df = pd.read_sql_query(f'SELECT * from ZCONCLUSIONTYPE', con)
    df = df[df['ZICONPNGDATA'].notna()].transpose()
    df.apply(
        lambda row: 
            save_blob(row['ZICONPNGDATA'], f'icons/{row["ZIDENTIFIER"]}.png')
    )
    print(df)
    

def dump_entry(p):
    print(p[p[0].notna()].transpose().to_json(orient='records',lines=True))

def find_place(con, place_pk):
    p = pd.read_sql_query(f'SELECT * from ZBASEOBJECT where Z_PK = {place_pk}', con)
    dump_entry(p.transpose())

def find_events(con, event_kind_pk, person_id):
    df_event = pd.read_sql_query(f'SELECT * from ZBASEOBJECT where Z_ENT = {event_kind_pk} and ZPERSON1 = {person_id}', con).transpose()
    dump_entry(df_event)
    # print(df_event.to_dict('records'))

    # df_event.apply(
    #     lambda e:
    #         find_place(con, e['ZASSIGNEDPLACE'])
    # )

def find_person(con, person_id):
    p = pd.read_sql_query(f'SELECT * from ZBASEOBJECT where Z_PK = {person_id}', con)
    pjson = p.to_json(orient='records',lines=True);
    
    pj: Person = parse_person(pjson)
    print(pj)
    # find_events(con, 25, person_id)

def mfamt_db_dump():
    
    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("./database.sqlite")
    # dump_conclusion_type(con)
    find_person(con, 1688)
    
    # Get parent in ZCHILDRELATION table
    # ZFAMILLY
    #  For family id 250 = zbaseobject id 250 and ZMAN, ZWOMAN
    
    # For each event, get location
    # ZASSIGNEDPLACE
    
    # Get the kind of event
    # ZCONCLUSIONTYPE
    
    df_fam = pd.read_sql_query("SELECT * FROM ZCHILDRELATION where ZCHILD = '1688'", con)
    # print(df_fam["ZFAMILY"])

    df_par = pd.read_sql_query("SELECT * FROM ZBASEOBJECT where Z_PK = '250'", con)
    # print(df_par["ZMAN"])
    # print(df_par["ZWOMAN"])

    find_person(con, df_par["ZMAN"][0])
    find_person(con, df_par["ZWOMAN"][0])


    con.close()

    return "Hello from mfamt_db_dump!"

def mfamt_db_dump2():
    return "Hello from mfamt_db_dump2!"

def main():
    """MY MAIN"""
    print(mfamt_db_dump())
    # print(mfamt_db_dump2())

if __name__ == "__main__":
    # execute only if run as a script
    main()