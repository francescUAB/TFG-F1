import psycopg2
import pandas as pd
import numpy as np
import os


def calculate_age(birth_date, race_date):
    """Calcula l'edat a partir de la data de naixement i la data de la cursa."""
    age = race_date.year - birth_date.year - ((race_date.month, race_date.day) < (birth_date.month, birth_date.day))
    return age


def process_f1_dataset_single_position():
    """Genera el dataset sense agrupació (posicions individuals)."""
    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )
    query = """
    SELECT DISTINCT
        rac.raceid,
        dri.driverid,
        dri.driverref,
        con.constructorid,
        cir.circuitref,
        cir.circuitid,
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
        qual.gap_to_best_time
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
    """
    df = pd.read_sql(query, connection)
    df = df.drop_duplicates()

    # Processar el dataset
    df['dob'] = pd.to_datetime(df['dob'])
    df['date'] = pd.to_datetime(df['date'])
    df['age'] = df.apply(lambda row: calculate_age(row['dob'], row['date']), axis=1)

    df = df.sort_values(by=['constructorid', 'year', 'raceid'])
    for col in ['hability', 'constructor_fiability', 'constructor_performance']:
        df[col] = df.groupby('constructorid')[col].shift(1)

    df = df.dropna(subset=['experience', 'hability', 'constructor_experience', 'constructor_fiability', 'constructor_performance', 'gap_to_best_time'])

   
    df['target'] = df['positionorder']

    if not os.path.exists('datasets'):
        os.makedirs('datasets')

    
    output_path = f"./datasets/f1_top20_target_single_position_all_circuits.csv"
    df.to_csv(output_path, sep=';', encoding='utf-8', index=False)

    print(f"Dataset sense agrupació guardat en: {output_path}")
    connection.close()


def process_f1_dataset_grouped_by_2():
    """Genera el dataset agrupant posicions de 2 en 2."""
    process_f1_dataset_grouped(agrupacio=2)


def process_f1_dataset_grouped_by_4():
    """Genera el dataset agrupant posicions de 4 en 4."""
    process_f1_dataset_grouped(agrupacio=4)


def process_f1_dataset_grouped(agrupacio):
    """Genera el dataset agrupant posicions segons el nivell d'agrupació especificat."""
    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )
    query = """
    SELECT DISTINCT
        rac.raceid,
        dri.driverid,
        dri.driverref,
        con.constructorid,
        cir.circuitref,
        cir.circuitid,
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
        qual.gap_to_best_time
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
    """
    df = pd.read_sql(query, connection)
    df = df.drop_duplicates()

   
    df['dob'] = pd.to_datetime(df['dob'])
    df['date'] = pd.to_datetime(df['date'])
    df['age'] = df.apply(lambda row: calculate_age(row['dob'], row['date']), axis=1)

    df = df.sort_values(by=['constructorid', 'year', 'raceid'])
    for col in ['hability', 'constructor_fiability', 'constructor_performance']:
        df[col] = df.groupby('constructorid')[col].shift(1)

    df = df.dropna(subset=['experience', 'hability', 'constructor_experience', 'constructor_fiability', 'constructor_performance', 'gap_to_best_time'])

    
    df['target'] = (df['positionorder'] - 1) // agrupacio + 1

    if not os.path.exists('datasets'):
        os.makedirs('datasets')

    
    output_path = f"./datasets/f1_top20_target_agrupacio_{agrupacio}_all_circuits.csv"
    df.to_csv(output_path, sep=';', encoding='utf-8', index=False)

    print(f"Dataset agrupació {agrupacio} guardat en: {output_path}")
    connection.close()
