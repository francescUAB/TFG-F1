import psycopg2
from psycopg2 import sql
import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine



def calculate_age(birth_date, race_date):
    age = race_date.year - birth_date.year - ((race_date.month, race_date.day) < (birth_date.month, birth_date.day))
    return age


def process_f1_all_positions_dataset(circuit_id):
    import pandas as pd
    import os
    import psycopg2

   
    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )

    query = f"""
    SELECT DISTINCT
        rac.raceid,
        dri.driverid,
        dri.driverref,
        con.constructorid,
        cir.circuitref,
        res.grid,
        res.positionorder,
        rac.date,
        rac.year,
        dri.dob,
        skill.experience_scaled AS experience,
        skill.habilidad AS hability,
        cons.experience AS constructor_experience,
        cons.fiability AS constructor_fiability,
        cons.performance AS constructor_performance,
        qual.gap_to_best_time -- Gap respecto al mejor tiempo de clasificación
    FROM results res
    JOIN drivers dri ON res.driverid = dri.driverid
    JOIN constructors con ON res.constructorid = con.constructorid
    JOIN races rac ON res.raceid = rac.raceid
    JOIN circuits cir ON rac.circuitid = cir.circuitid
    JOIN (
        SELECT driverid, season_year, MAX(experience_scaled) AS experience_scaled, MAX(habilidad) AS habilidad
        FROM driver_skill_per_season
        GROUP BY driverid, season_year
    ) skill ON skill.driverid = dri.driverid AND skill.season_year = EXTRACT(YEAR FROM rac.date)
    JOIN (
        SELECT constructorid, season_year, MAX(experience) AS experience, MAX(fiability) AS fiability, MAX(performance) AS performance
        FROM constructor_describe_per_season
        GROUP BY constructorid, season_year
    ) cons ON cons.constructorid = con.constructorid AND cons.season_year = EXTRACT(YEAR FROM rac.date)
    LEFT JOIN (
        SELECT raceid, driverid, MIN(gap_to_best_time) AS gap_to_best_time
        FROM qualifying_dataset
        GROUP BY raceid, driverid
    ) qual ON qual.raceid = rac.raceid AND qual.driverid = dri.driverid
    WHERE cir.circuitid = {circuit_id} -- Filtrar por circuito
    """

    df = pd.read_sql(query, connection)

    df = df.drop_duplicates()

    
    df['dob'] = pd.to_datetime(df['dob'])
    df['date'] = pd.to_datetime(df['date'])
    df['age'] = df.apply(lambda row: calculate_age(row['dob'], row['date']), axis=1)

    df = df.sort_values(by=['constructorid', 'year'])
    for col in ['hability', 'constructor_fiability', 'constructor_performance']:
        df[col] = df.groupby('constructorid')[col].shift(1)


    df['target'] = df['positionorder']


    df = df.dropna(subset=['experience', 'hability', 'constructor_experience', 'constructor_fiability', 'constructor_performance', 'gap_to_best_time'])

    if not os.path.exists('datasets'):
        os.makedirs('datasets')

    output_path = f"./datasets/f1_all_positions_target_circuit_{circuit_id}.csv"
    df.to_csv(output_path, sep=';', encoding='utf-8', index=False)

    print(f"Dataset guardado en: {output_path}")

    connection.close()
