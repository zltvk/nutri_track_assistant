import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",        # user
            password="admin", # password
            database="nutri_track_db"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def execute_query(query, params=None, fetch=False):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    
    result = None
    if fetch:
        result = cursor.fetchall()
    else:
        conn.commit() 
    
    cursor.close()
    conn.close()
    return result

def add_food_item(name, calories=None, protein=None, fat=None, carbs=None, is_composite=False):
    query = """
    INSERT INTO food_items (name, is_composite, calories_100g, protein_100g, fat_100g, carbohydrates_100g)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (name, is_composite, calories, protein, fat, carbs)
    execute_query(query, params)

def add_recipe_ingredient(parent_id, child_id, weight):
    query = "INSERT INTO recipe_ingredients (parent_food_id, child_food_id, weight_grams) VALUES (%s, %s, %s)"
    execute_query(query, (parent_id, child_id, weight))

def log_consumption(user_id, food_id, weight):
    query = "INSERT INTO consumption_log (user_id, food_item_id, weight_consumed) VALUES (%s, %s, %s)"
    execute_query(query, (user_id, food_id, weight))

def get_daily_report(user_id):
    query = """
    SELECT * FROM v_daily_consumption_analytics 
    WHERE user_id = %s AND DATE(consumed_at) = CURDATE()
    """
    return execute_query(query, (user_id,), fetch=True)

def get_food_id_by_name(name):
    query = "SELECT id FROM food_items WHERE name = %s"
    result = execute_query(query, (name,), fetch=True)
    return result[0]['id'] if result else None

def get_user_goals(user_id):
    query = "SELECT target_calories FROM users WHERE id = %s"
    result = execute_query(query, (user_id,), fetch=True)
    return result[0] if result else None