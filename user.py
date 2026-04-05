from database import get_connection


def register_user(name, age, ph_no, type_of_addiction):
    conn = get_connection()
    cursor = conn.cursor()

    query = """INSERT INTO users 
               (name, age, ph_no, type_of_addiction) 
               VALUES (%s, %s, %s, %s)"""

    cursor.execute(query, (name, age, ph_no, type_of_addiction))
    conn.commit()

    user_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return user_id
