import seed

def stream_user_ages():
    """Generator yields ages one by one"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    row = cursor.fetchone()
    while row:
        yield row[0]
        row = cursor.fetchone()
    cursor.close()
    connection.close()

def calculate_average():
    """Compute average age using generator"""
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    average = total / count if count else 0
    print(f"Average age of users: {average}")
