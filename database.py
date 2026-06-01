import mysql.connector
import pandas as pd


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Quantum@2025",
        database="healthcare"
    )


def add_patient(data):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO patients (
        full_name,
        dob,
        email,
        glucose,
        haemoglobin,
        cholesterol,
        remarks
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, data)
    conn.commit()

    cursor.close()
    conn.close()


def get_patients():
    conn = get_connection()

    query = "SELECT * FROM patients"
    df = pd.read_sql(query, conn)

    conn.close()
    return df


def delete_patient(patient_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE id = %s",
        (patient_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()


def update_patient(patient_id, data):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE patients
    SET
        full_name = %s,
        dob = %s,
        email = %s,
        glucose = %s,
        haemoglobin = %s,
        cholesterol = %s,
        remarks = %s
    WHERE id = %s
    """

    cursor.execute(query, (*data, patient_id))
    conn.commit()

    cursor.close()
    conn.close()


def get_patient_by_id(patient_id):
    conn = get_connection()

    query = """
    SELECT *
    FROM patients
    WHERE id = %s
    """

    df = pd.read_sql(query, conn, params=(patient_id,))

    conn.close()
    return df


def get_total_patients():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM patients")
    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return total