import psycopg2
from psycopg2 import sql
import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine


def change_null(value):
    return None if value == r'\N' else value

def import_circuits():
    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )
    print(connection)

    file= pd.read_csv('archive/circuits.csv')

    cursor=connection.cursor()

    for index, row in file.iterrows():
        cursor.execute("""
        INSERT INTO circuits (circuitId, circuitRef, name, location, country, lat, lng, alt, url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (row['circuitId'], row['circuitRef'], row['name'], row['location'], row['country'], 
        row['lat'], row['lng'], row['alt'], row['url']))
    connection.commit()
    cursor.close()
    connection.close()

    print("Dades pujades correctament")

def import_constructors():
    file = pd.read_csv('archive/constructors.csv')
    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )
    cursor = connection.cursor()
    for index, row in file.iterrows():
        cursor.execute("""
        INSERT INTO constructors (constructorid, constructorref, name, nationality, url)
        VALUES (%s, %s, %s, %s, %s)
    """, (row['constructorId'], row['constructorRef'], row['name'], row['nationality'], row['url']))   
    connection.commit()
    cursor.close()
    connection.close()
    print("Dades pujades correctament")

def import_constructors_results():

        file = pd.read_csv('archive/constructor_results.csv')

        connection = psycopg2.connect(
            host="127.0.0.1",
            database="f1_data",
            user="postgres",
            password="francesc1998",
            port=5432
        )
        cursor = connection.cursor()

        for index, row in file.iterrows():
            cursor.execute("""
            INSERT INTO constructor_results (constructor_resultsid, raceid, constructorid, points, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            change_null(row['constructorResultsId']),
            change_null(row['raceId']),
            change_null(row['constructorId']),
            change_null(row['points']),
            change_null(row['status'])
        ))

        connection.commit()

        cursor.close()
        connection.close()

        print("Dades pujades correctament")

def import_races():
    file = pd.read_csv('archive/races.csv')

    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )
    cursor = connection.cursor()

    for index, row in file.iterrows():
        cursor.execute("""
        INSERT INTO races (raceid, year, round, circuitId, name, date, time, url, 
                           fp1_date, fp1_time, fp2_date, fp2_time, 
                           fp3_date, fp3_time, quali_date, quali_time, 
                           sprint_date, sprint_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (row['raceId'], row['year'], row['round'], row['circuitId'], row['name'], 
          change_null(row['date']), change_null(row['time']), row['url'],
          change_null(row['fp1_date']), change_null(row['fp1_time']), 
          change_null(row['fp2_date']), change_null(row['fp2_time']),
          change_null(row['fp3_date']), change_null(row['fp3_time']),
          change_null(row['quali_date']), change_null(row['quali_time']),
          change_null(row['sprint_date']), change_null(row['sprint_time'])))

    connection.commit()

    
    cursor.close()
    connection.close()

    print("Dades pujades correctament")

def import_drivers():
    file = pd.read_csv('archive/drivers.csv')

    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )
    cursor = connection.cursor()

    for index, row in file.iterrows():
        cursor.execute("""
        INSERT INTO drivers (driverid, driverref, number, code, forename, surname, dob, nationality, url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (row['driverId'], row['driverRef'], 
          change_null(row['number']), change_null(row['code']), row['forename'], row['surname'], 
          change_null(row['dob']), row['nationality'], row['url']))
    connection.commit()
    cursor.close()
    connection.close()

    print("Dades pujades correctament")

def import_results():
    file = pd.read_csv('archive/results.csv')

    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )
    cursor = connection.cursor()

    for index, row in file.iterrows():
        cursor.execute("""
            INSERT INTO results (
                resultid, raceid, driverid, constructorid, number, grid, position, 
                positiontext, positionorder, points, laps, time, miliseconds, 
                fastestlap, rank, fastestlaptime, fastestlapspeed, statusid
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            change_null(row['resultId']),
            change_null(row['raceId']),
            change_null(row['driverId']),
            change_null(row['constructorId']),
            change_null(row['number']),
            change_null(row['grid']),
            change_null(row['position']),
            change_null(row['positionText']),
            change_null(row['positionOrder']),
            change_null(row['points']),
            change_null(row['laps']),
            change_null(row['time']),
            change_null(row['milliseconds']),
            change_null(row['fastestLap']),
            change_null(row['rank']),
            change_null(row['fastestLapTime']),
            change_null(row['fastestLapSpeed']),
            change_null(row['statusId'])
        ))
    connection.commit()
    cursor.close()
    connection.close()

    print("Dades pujades correctament")

def import_status():

    file = pd.read_csv('archive/status.csv')

    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )
    cursor = connection.cursor()

    for index, row in file.iterrows():
        cursor.execute( """
            INSERT INTO status (statusid, status)
            VALUES (%s, %s)
        """, (change_null(row['statusId']), change_null(row['status'])))
    connection.commit()
    cursor.close()
    connection.close()

    print("Dades pujades correctament")
   
def import_lap_times():
    file = pd.read_csv('archive/lap_times.csv')

    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )
    cursor = connection.cursor()

    for index, row in file.iterrows():
        cursor.execute( """
            INSERT INTO laptimes (raceid, driverid, lap, position, time, miliseconds)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            change_null(row['raceId']), 
            change_null(row['driverId']),
            change_null(row['lap']), 
            change_null(row['position']), 
            change_null(row['time']),
            change_null(row['milliseconds'])
        )
        )
    connection.commit()
    cursor.close()
    connection.close()

    print("Dades pujades correctament")

def import_pit_stops():
    file = pd.read_csv('archive/pit_stops.csv')

    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )
    cursor = connection.cursor()

    for index, row in file.iterrows():
        cursor.execute(  """
            INSERT INTO pitstops (raceid, driverid, stop, lap, time, duration, miliseconds)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            change_null(row['raceId']),
            change_null(row['driverId']),
            change_null(row['stop']),
            change_null(row['lap']),
            change_null(row['time']),
            change_null(row['duration']),
            change_null(row['milliseconds'])
        )
        )
    connection.commit()
    cursor.close()
    connection.close()

    print("Dades pujades correctament")

def import_qualifying():
    file = pd.read_csv('archive/qualifying.csv')

    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )
    cursor = connection.cursor()

    for index, row in file.iterrows():
        cursor.execute( """
            INSERT INTO qualifying (qualifyId, raceId, driverId, constructorId, number, position, q1, q2, q3)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            change_null(row['qualifyId']),
            change_null(row['raceId']),
            change_null(row['driverId']),
            change_null(row['constructorId']),
            change_null(row['number']),
            change_null(row['position']),
            change_null(row['q1']),
            change_null(row['q2']),
            change_null(row['q3'])
        )
        )
    connection.commit()
    cursor.close()
    connection.close()

    print("Dades pujades correctament")

def import_seasons():
    file = pd.read_csv('archive/seasons.csv')

    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )
    cursor = connection.cursor()

    for index, row in file.iterrows():
        cursor.execute( """
            INSERT INTO seasons (year, url)
            VALUES (%s, %s)
        """, (
            change_null(row['year']),
            change_null(row['url'])
        )
        )
    connection.commit()
    cursor.close()
    connection.close()

    print("Dades pujades correctament")

def import_constructor_standings():
    file = pd.read_csv('archive/constructor_standings.csv')

    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )
    cursor = connection.cursor()

    for index, row in file.iterrows():
        cursor.execute("""
            INSERT INTO constructor_standings (constructorstandingsid, raceid, constructorid, points, position, positiontext, wins)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
            change_null(row['constructorStandingsId']),
            change_null(row['raceId']),
            change_null(row['constructorId']),
            change_null(row['points']),
            change_null(row['position']),
            change_null(row['positionText']),
            change_null(row['wins'])
        )
        )
    connection.commit()
    cursor.close()
    connection.close()

    print("Dades pujades correctament")

def import_sprint_results():
    file = pd.read_csv('archive/sprint_results.csv')

    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )
    cursor = connection.cursor()

    for index, row in file.iterrows():
        cursor.execute("""
            INSERT INTO sprint_results (resultid, raceid, driverid, constructorid, number, grid, position, positiontext, positionorder, points, laps, time, miliseconds, fastestlap, fastestlaptime,statusid)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
            change_null(row['resultId']),
            change_null(row['raceId']),
            change_null(row['driverId']),
            change_null(row['constructorId']),
            change_null(row['number']),
            change_null(row['grid']),
            change_null(row['position']),
            change_null(row['positionText']),
            change_null(row['positionOrder']),
            change_null(row['points']),
            change_null(row['laps']),
            change_null(row['time']),
            change_null(row['milliseconds']),
            change_null(row['fastestLap']),
            change_null(row['fastestLapTime']),
            change_null(row['statusId'])
        )
        )
    connection.commit()
    cursor.close()
    connection.close()

    print("Dades pujades correctament")
  
def update_circuits():
    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )
    print("Conexión establecida.")

    # Cargar los datos desde el CSV
    file = pd.read_csv('archiveOK/circuits.csv')

    cursor = connection.cursor()

    for index, row in file.iterrows():
        cursor.execute("""
        UPDATE circuits
        SET length = %s,
            turns = %s,
            laps = %s
        WHERE circuitId = %s
        """, (row['Length'], row['Turns'], row['laps'], row['circuitId']))

    connection.commit()
    cursor.close()
    connection.close()

    print("Datos actualizados correctamente.")

def process_f1_top10_target_dataset(circuit_id):
    import pandas as pd
    import os
    import psycopg2

    # Conexión a la base de datos
    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )

    # Consulta SQL para obtener datos por circuito
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

    # Leer los datos en un DataFrame
    df = pd.read_sql(query, connection)

    # Eliminar duplicados
    df = df.drop_duplicates()

    # Calcular la edad de los pilotos
    df['dob'] = pd.to_datetime(df['dob'])
    df['date'] = pd.to_datetime(df['date'])
    df['age'] = df.apply(lambda row: calculate_age(row['dob'], row['date']), axis=1)

    # Imputar valores siempre desde los datos del año anterior
    df = df.sort_values(by=['constructorid', 'year'])
    for col in ['hability', 'constructor_fiability', 'constructor_performance']:
        df[col] = df.groupby('constructorid')[col].shift(1)

    # Redefinir el target de posición
    def map_position(position):
        if position <= 10:
            return position  # Posiciones del 1 al 10
        else:
            return 11  # Fuera de puntos

    df['target'] = df['positionorder'].apply(map_position)

    # Eliminar filas con valores nulos en los campos clave
    df = df.dropna(subset=['experience', 'hability', 'constructor_experience', 'constructor_fiability', 'constructor_performance', 'gap_to_best_time'])

    # Crear directorio si no existe
    if not os.path.exists('datasets'):
        os.makedirs('datasets')
    
    # Guardar el DataFrame en un archivo CSV
    output_path = f"./datasets/f1_top10_target_circuit_{circuit_id}.csv"
    df.to_csv(output_path, sep=';', encoding='utf-8', index=False)

    print(f"Dataset guardado en: {output_path}")

    # Cerrar la conexión
    connection.close()


def process_f1_top10_allcircuits_target_dataset():
    # Conexión a la base de datos
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
    """

    df = pd.read_sql(query, connection)

    df = df.drop_duplicates()

    df['dob'] = pd.to_datetime(df['dob'])
    df['date'] = pd.to_datetime(df['date'])
    df['age'] = df.apply(lambda row: calculate_age(row['dob'], row['date']), axis=1)

    df = df.sort_values(by=['constructorid', 'year', 'raceid'])
    for col in ['hability', 'constructor_fiability', 'constructor_performance']:
        df[col] = df.groupby('constructorid')[col].shift(1)

    df = df[df['positionorder'] <= 10]

    def map_position(position):
        if position <= 10:
            return position  
        else:
            return 11 

    df['target'] = df['positionorder'].apply(map_position)
    
   
    df = df.dropna(subset=['experience', 'hability', 'constructor_experience', 'constructor_fiability', 'constructor_performance', 'gap_to_best_time'])

  
    if not os.path.exists('datasets'):
        os.makedirs('datasets')
    

    output_path = f"./datasets/f1_top10_target_all_circuits.csv"
    df.to_csv(output_path, sep=';', encoding='utf-8', index=False)

    print(f"Dataset guardado en: {output_path}")

    connection.close()


def update_drivers():
   
    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )
    print("Conexión establecida.")

    file = pd.read_csv('archiveOK/drivers.csv')

    cursor = connection.cursor()

    for index, row in file.iterrows():
        if pd.notnull(row['experience']) and pd.notnull(row['racecraft']) and pd.notnull(row['awareness']) and pd.notnull(row['pace']):
            cursor.execute("""
            UPDATE drivers
            SET experience = %s,
                racecraft = %s,
                awareness = %s,
                pace = %s
            WHERE driverId = %s
            """, (row['experience'], row['racecraft'], row['awareness'], row['pace'], row['driverId']))

   
    connection.commit()
    cursor.close()
    connection.close()

    print("Datos actualizados correctamente.")

# def import_functions():
#     # import_circuits() 
#     # import_constructors() 
#     # import_races() 
#     # import_drivers() 
#     # import_constructors_results() 
#     # import_status() 
#     # import_results() 
#     # import_lap_times() 
#     # import_pit_stops() 
#     # import_qualifying() 
#     # import_seasons() 
#     # import_constructor_standings() 
#     # import_sprint_results()
#     # update_circuits()

# update_drivers()


def convert_time_to_seconds(time_str):
    """Convert a time string in the format 'M:SS.sss' to seconds."""
    if time_str is None:
        return None
    minutes, seconds = time_str.split(':')

    total_seconds = int(minutes) * 60 + float(seconds)
    total_seconds =round(total_seconds,3)
    return total_seconds

def calculate_age(birth_date, race_date):
    age = race_date.year - birth_date.year - ((race_date.month, race_date.day) < (birth_date.month, birth_date.day))
    return age

def categorize_position(position):
    if position <= 5:
        return "Top 5"
    elif 6 <= position <= 10:
        return "6-10"
    else:
        return "11+"

def obtener_experiencia_y_habilidad_por_temporada():
    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )

    query = """
    SELECT
        res.driverid,
        rac.year AS season_year,
        res.grid,         -- Posición de salida en la parrilla (clasificación)
        res.positionorder -- Posición final en la carrera
    FROM
        results res
    JOIN
        drivers dri ON res.driverid = dri.driverid
    JOIN
        races rac ON res.raceid = rac.raceid
    ORDER BY
        res.driverid, rac.year;
    """


    df = pd.read_sql(query, connection)
    connection.close()

  
    df = df.sort_values(by=['driverid', 'season_year'])
    df['experience'] = df.groupby('driverid').cumcount() + 1

  
    df_experience_max = df.groupby(['driverid', 'season_year'])['experience'].max().reset_index()


    min_exp = df_experience_max['experience'].min()
    max_exp = df_experience_max['experience'].max()
    a, b = 0, 100
    df_experience_max['experience_scaled'] = ((a + ((df_experience_max['experience'] - min_exp) * (b - a)) / (max_exp - min_exp)).round()).astype(int).clip(a, b)

  
    max_position = max(df['grid'].max(), df['positionorder'].max())
    df['qualy_score'] = ((max_position - df['grid']) / max_position * 100).round().astype(int)
    df['race_score'] = ((max_position - df['positionorder']) / max_position * 100).round().astype(int)


    df_avg = df.groupby(['driverid', 'season_year']).agg(
        avg_qualy_score=('qualy_score', 'mean'),
        avg_race_score=('race_score', 'mean')
    ).reset_index()

   
    df_avg['habilidad'] = ((df_avg['avg_qualy_score'] * 0.4) + (df_avg['avg_race_score'] * 0.6)).round().astype(int).clip(a, b)


    df_final = pd.merge(df_experience_max[['driverid', 'season_year', 'experience_scaled']],
                        df_avg[['driverid', 'season_year', 'habilidad']],
                        on=['driverid', 'season_year'])


    df_final['habilidad'] = df_final.groupby('driverid')['habilidad'].shift(1).fillna(df_final['habilidad'])


    engine = create_engine('postgresql+psycopg2://postgres:francesc1998@127.0.0.1:5432/f1_data')

    df_final.to_sql('driver_skill_per_season', engine, if_exists='replace', index=False)

    print("Datos cargados correctamente en la tabla 'driver_skill_per_season'.")


def process_f1_groupby2_positions_for_circuit(circuit_id, circuit_name):
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
        rac.raceId,
        dri.driverId,
        dri.driverref,
        con.constructorId,
        cir.circuitref,
        res.grid,
        res.positionOrder,
        rac.date,
        rac.year,
        dri.dob,
        skill.experience_scaled AS experience,
        skill.habilidad AS hability,
        cons.experience AS constructor_experience,
        cons.fiability AS constructor_fiability,
        cons.performance AS constructor_performance,
        qual.gap_to_best_time  -- Gap respecto al mejor tiempo de clasificación
    FROM results res
    JOIN drivers dri ON res.driverId = dri.driverId
    JOIN constructors con ON res.constructorId = con.constructorId
    JOIN races rac ON res.raceId = rac.raceId
    JOIN circuits cir ON rac.circuitId = cir.circuitId
    JOIN (
        SELECT driverid, season_year, MAX(experience_scaled) AS experience_scaled, MAX(habilidad) AS habilidad
        FROM driver_skill_per_season
        GROUP BY driverid, season_year
    ) skill ON skill.driverid = dri.driverId AND skill.season_year = EXTRACT(YEAR FROM rac.date)
    JOIN (
        SELECT constructorid, season_year, MAX(experience) AS experience, MAX(fiability) AS fiability, MAX(performance) AS performance
        FROM constructor_describe_per_season
        GROUP BY constructorid, season_year
    ) cons ON cons.constructorid = con.constructorId AND cons.season_year = EXTRACT(YEAR FROM rac.date)
    LEFT JOIN (
        SELECT raceid, driverid, MIN(gap_to_best_time) AS gap_to_best_time
        FROM qualifying_dataset
        GROUP BY raceid, driverid
    ) qual ON qual.raceid = rac.raceId AND qual.driverid = dri.driverId
    WHERE cir.circuitId = {circuit_id}
      AND rac.year >= 2014 -- Filtrar por la era híbrida
    """


    df = pd.read_sql(query, connection)


    df = df.drop_duplicates()


    df['dob'] = pd.to_datetime(df['dob'])
    df['date'] = pd.to_datetime(df['date'])
    df['age'] = df.apply(lambda row: calculate_age(row['dob'], row['date']), axis=1)


    df = df[df['positionorder'] <= 20]

    
    def group_position(position):
        return (position + 1) // 2

    df['target'] = df['positionorder'].apply(group_position)
    df = df.drop(columns=['positionorder'])  

    
    df = df.dropna(subset=['experience', 'hability', 'constructor_experience', 'constructor_fiability', 'constructor_performance', 'gap_to_best_time'])

   
    if not os.path.exists('datasets'):
        os.makedirs('datasets')
    

    output_path = f"./datasets/prediction_f1_data_groupby2_circuit_{circuit_id}_{circuit_name}_hybrid_era.csv"
    df.to_csv(output_path, sep=';', encoding='utf-8', index=False)

    print(f"Dataset guardado en: {output_path}")

  
    connection.close()
def process_f1_groupby1_positions_for_circuit(circuit_id, circuit_name):
    import pandas as pd
    import os
    import psycopg2
    from sqlalchemy import create_engine

    # Conexión a la base de datos
    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )

    # Consulta SQL con filtro para la era híbrida (2014 en adelante)
    query = f"""
    SELECT DISTINCT
        rac.raceId,
        dri.driverId,
        dri.driverref,
        con.constructorId,
        cir.circuitref,
        res.grid,
        res.positionOrder,
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
    JOIN drivers dri ON res.driverId = dri.driverId
    JOIN constructors con ON res.constructorId = con.constructorId
    JOIN races rac ON res.raceId = rac.raceId
    JOIN circuits cir ON rac.circuitId = cir.circuitId
    JOIN (
        SELECT driverid, season_year, MAX(experience_scaled) AS experience_scaled, MAX(habilidad) AS habilidad
        FROM driver_skill_per_season
        GROUP BY driverid, season_year
    ) skill ON skill.driverid = dri.driverId AND skill.season_year = EXTRACT(YEAR FROM rac.date)
    JOIN (
        SELECT constructorid, season_year, MAX(experience) AS experience, MAX(fiability) AS fiability, MAX(performance) AS performance
        FROM constructor_describe_per_season
        GROUP BY constructorid, season_year
    ) cons ON cons.constructorid = con.constructorId AND cons.season_year = EXTRACT(YEAR FROM rac.date)
    LEFT JOIN (
        SELECT raceid, driverid, MIN(gap_to_best_time) AS gap_to_best_time
        FROM qualifying_dataset
        GROUP BY raceid, driverid
    ) qual ON qual.raceid = rac.raceId AND qual.driverid = dri.driverId
    WHERE cir.circuitId = {circuit_id}
      AND rac.year >= 2014 -- Filtrar por la era híbrida
    """

    # Leer los datos en un DataFrame
    df = pd.read_sql(query, connection)

    # Eliminar duplicados
    df = df.drop_duplicates()

    # Calcular la edad de los pilotos
    df['dob'] = pd.to_datetime(df['dob'])
    df['date'] = pd.to_datetime(df['date'])
    df['age'] = df.apply(lambda row: calculate_age(row['dob'], row['date']), axis=1)

    # Filtrar pilotos con posición dentro del top 20
    df = df[df['positionorder'] <= 20]

    # Crear la columna de target como posición
    df['target'] = df['positionorder']
    df = df.drop(columns=['positionorder'])  # Eliminar columna original de posición

    # Eliminar filas con valores nulos en los campos clave
    df = df.dropna(subset=['experience', 'hability', 'constructor_experience', 'constructor_fiability', 'constructor_performance', 'gap_to_best_time'])

    # Crear directorio si no existe
    if not os.path.exists('datasets'):
        os.makedirs('datasets')
    
    # Guardar el DataFrame en un archivo CSV
    output_path = f"./datasets/prediction_f1_data_groupby1_circuit_{circuit_id}_{circuit_name}_hybrid_era.csv"
    df.to_csv(output_path, sep=';', encoding='utf-8', index=False)

    print(f"Dataset guardado en: {output_path}")

    # Cerrar la conexión
    connection.close()
def process_f1_groupby4_positions_for_circuit(circuit_id,circuit_name):
    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )

    query = f"""
    SELECT
        rac.raceId,
        dri.driverId,
        dri.driverref,
        cir.circuitref,
        con.constructorId,
        res.grid,
        res.positionOrder,
        rac.date,
        rac.year,
        dri.dob,
        skill.experience_scaled AS experience,
        skill.habilidad AS hability,
        cons.experience AS constructor_experience,
        cons.fiability AS constructor_fiability,
        cons.performance AS constructor_performance
    FROM results res
    JOIN drivers dri ON res.driverId = dri.driverId
    JOIN constructors con ON res.constructorId = con.constructorId
    JOIN races rac ON res.raceId = rac.raceId
    JOIN circuits cir ON rac.circuitId = cir.circuitId
    JOIN driver_skill_per_season skill 
      ON skill.driverid = dri.driverId AND skill.season_year = EXTRACT(YEAR FROM rac.date)
    JOIN constructor_describe_per_season cons
      ON cons.constructorid = con.constructorId AND cons.season_year = EXTRACT(YEAR FROM rac.date)
    WHERE cir.circuitId = {circuit_id}
    """

    df = pd.read_sql(query, connection)

    df['dob'] = pd.to_datetime(df['dob'])
    df['date'] = pd.to_datetime(df['date'])
    df['age'] = df.apply(lambda row: calculate_age(row['dob'], row['date']), axis=1)
    df = df[df['positionorder'] <= 20]

    def group_position(position):
        if 1 <= position <= 4:
            return 1
        elif 5 <= position <= 8:
            return 2
        elif 9 <= position <= 12:
            return 3
        elif 13 <= position <= 16:
            return 4
        elif 17 <= position <= 20:
            return 5

    df['target'] = df['positionorder'].apply(group_position)
    df = df.drop(columns=['positionorder'])
    df = df.dropna(subset=['experience', 'hability', 'constructor_experience', 'constructor_fiability', 'constructor_performance'])

    if not os.path.exists('datasets'):
        os.makedirs('datasets')
    
    df.to_csv(f"./datasets/prediction_f1_data_groupby4_circuit_{circuit_id}_{circuit_name}.csv", sep=';', encoding='utf-8', index=False)

    connection.close()
def calcular_experiencia_constructores():
  
    results_df = pd.read_csv('TFG GIT/TFG/archiveOK/results.csv')
    races_df = pd.read_csv('TFG GIT/TFG/archiveOK/races.csv')

   
    results_df = results_df.merge(races_df[['raceId', 'year']], on='raceId', how='left')
    results_df.rename(columns={'year': 'season_year'}, inplace=True)

  
    constructores_experiencia_df = results_df.groupby(['constructorId', 'season_year'])['raceId'].nunique().reset_index()
    constructores_experiencia_df.rename(columns={'raceId': 'experiencia_anual'}, inplace=True)

   
    constructores_experiencia_df = constructores_experiencia_df.sort_values(by=['constructorId', 'season_year'])
    constructores_experiencia_df['experiencia'] = constructores_experiencia_df.groupby('constructorId')['experiencia_anual'].cumsum()

  
    min_experiencia = constructores_experiencia_df['experiencia'].min()
    max_experiencia = constructores_experiencia_df['experiencia'].max()
    a, b = 0, 100
    constructores_experiencia_df['experiencia'] = (
        a + ((constructores_experiencia_df['experiencia'] - min_experiencia) * (b - a)) / (max_experiencia - min_experiencia)
    ).round().astype(int)

    
    dnf_df = results_df[~results_df['statusId'].isin([1, 2, 3])]
    dnf_count_df = dnf_df.groupby(['constructorId', 'season_year'])['raceId'].nunique().reset_index()
    dnf_count_df.rename(columns={'raceId': 'dnf_count'}, inplace=True)

    total_races_df = results_df.groupby(['constructorId', 'season_year'])['raceId'].nunique().reset_index()
    total_races_df.rename(columns={'raceId': 'total_races'}, inplace=True)

    fiabilidad_df = pd.merge(total_races_df, dnf_count_df, on=['constructorId', 'season_year'], how='left')
    fiabilidad_df['dnf_count'].fillna(0, inplace=True)
    fiabilidad_df['fiabilidad'] = ((fiabilidad_df['total_races'] - fiabilidad_df['dnf_count']) / fiabilidad_df['total_races'] * 100).round(0).astype(int)

   
    fiabilidad_df['fiabilidad'] = (
        a + ((fiabilidad_df['fiabilidad'] - fiabilidad_df['fiabilidad'].min()) * (b - a)) / (fiabilidad_df['fiabilidad'].max() - fiabilidad_df['fiabilidad'].min())
    ).round().astype(int)

   
    max_position = max(results_df['grid'].max(), results_df['positionOrder'].max())
    results_df['qualy_score'] = ((max_position - results_df['grid']) / max_position * 100).round().astype(int)
    results_df['race_score'] = ((max_position - results_df['positionOrder']) / max_position * 100).round().astype(int)

    rendimiento_df = results_df.groupby(['constructorId', 'season_year']).agg(
        avg_qualy_score=('qualy_score', 'mean'),
        avg_race_score=('race_score', 'mean')
    ).reset_index()

    rendimiento_df['rendimiento'] = ((rendimiento_df['avg_qualy_score'] * 0.4) + (rendimiento_df['avg_race_score'] * 0.6)).round().astype(int).clip(a, b)

   
    constructores_df = pd.merge(constructores_experiencia_df, fiabilidad_df[['constructorId', 'season_year', 'fiabilidad']], on=['constructorId', 'season_year'])
    constructores_df = pd.merge(constructores_df, rendimiento_df[['constructorId', 'season_year', 'rendimiento']], on=['constructorId', 'season_year'])

   
    for col in ['experiencia', 'fiabilidad', 'rendimiento']:
        constructores_df[col] = constructores_df.groupby('constructorId')[col].shift(1).fillna(constructores_df[col])

    
    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )
    cursor = connection.cursor()

    
    for _, row in constructores_df.iterrows():
        cursor.execute(
            sql.SQL("""
                INSERT INTO constructor_describe_per_season (constructorid, season_year, experience, fiability, performance)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (constructorid, season_year) DO UPDATE SET
                    experience = EXCLUDED.experience,
                    fiability = EXCLUDED.fiability,
                    performance = EXCLUDED.performance;
            """),
            (int(row['constructorId']), int(row['season_year']), int(row['experiencia']), int(row['fiabilidad']), int(row['rendimiento']))
        )

   
    connection.commit()
    cursor.close()
    connection.close()


calcular_experiencia_constructores()
def convertir_a_segundos(tiempo):
    if pd.isnull(tiempo) or not isinstance(tiempo, str) or tiempo.strip() == '':
        return None 
    try:
        minutos, resto = tiempo.split(':')
        segundos, milisegundos = map(float, resto.split('.'))
        return int(minutos) * 60 + segundos + milisegundos / 1000
    except ValueError:
        print(f"Formato inesperado en tiempo: {tiempo}")  
        return None  


import pandas as pd
import psycopg2

def generar_dataset_qualifying():
   
    connection = psycopg2.connect(
        host="127.0.0.1",
        database="f1_data",
        user="postgres",
        password="francesc1998",
        port=5432
    )
    
   
    query = """
    SELECT
        q.raceid,
        q.driverid,
        q.constructorid,
        r.circuitid,
        r.year,
        res.statusid,
        q.q1,
        q.q2,
        q.q3
    FROM qualifying q
    JOIN results res ON q.raceid = res.raceid AND q.driverid = res.driverid
    JOIN races r ON q.raceid = r.raceid;
    """
   
    df = pd.read_sql_query(query, connection)


    def convertir_a_segundos(tiempo):
        if pd.isnull(tiempo) or not isinstance(tiempo, str) or tiempo.strip() == '':
            return None  
        try:
            minutos, resto = tiempo.split(':')
            segundos, milisegundos = map(float, resto.split('.'))
            return int(minutos) * 60 + segundos + milisegundos / 1000
        except ValueError:
            print(f"Formato inesperado en tiempo: {tiempo}") 
            return None 

  
    for col in ['q1', 'q2', 'q3']:
        df[col] = df[col].apply(convertir_a_segundos)

   
    df['best_qualifying_time'] = df[['q1', 'q2', 'q3']].min(axis=1)


    best_time = (
        df.groupby('raceid', as_index=False)['best_qualifying_time']
        .min()
        .rename(columns={'best_qualifying_time': 'best_time'})
    )

   
    df = df.merge(best_time, on='raceid', how='left')

  
    df['gap_to_best_time'] = (df['best_qualifying_time'] - df['best_time']).round(3)

   
    valid_statuses = [1, 11, 12]  
    df['finished'] = df['statusid'].isin(valid_statuses)

    df_final = df[['raceid', 'driverid', 'constructorid', 'circuitid', 'year', 'statusid', 'finished', 'gap_to_best_time']]
    
   
    output_file_path = "f1_qualifying_dataset.csv"
    df_final.to_csv(output_file_path, index=False)
    print(f"Archivo '{output_file_path}' generado correctamente.")

 
    connection.close()


import csv 
def insertar_datos_csv_en_postgres(csv_path, table_name, db_name, user, password, host="127.0.0.1", port=5432):
   
    connection = psycopg2.connect(
        host=host,
        database=db_name,
        user=user,
        password=password,
        port=port
    )
    cursor = connection.cursor()
    
   
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader) 
        for row in reader:
          
            row = [None if value == '' else value for value in row]
            cursor.execute(
                f"INSERT INTO {table_name} (raceid, driverid, constructorid, circuitid, year, statusid, finished, gap_to_best_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                row
            )

    connection.commit()
    cursor.close()
    connection.close()
    print(f"Datos insertados correctamente en la tabla '{table_name}'.")


csv_path = "f1_qualifying_dataset.csv"
table_name = "qualifying_dataset"
db_name = "f1_data"
user = "postgres"
password = "francesc1998"

# insertar_datos_csv_en_postgres(csv_path, table_name, db_name, user, password)



# generar_dataset_qualifying()
# csv_file_path = 'f1_teammate_and_leader_analysis_with_retires.csv'
# upload_csv_to_postgres(csv_file_path)





