import seed

def streamusersinbatches(batchsize):
    """Generator that yields batches of users"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    offset = 0
    while True:
        cursor.execute(f"SELECT * FROM user_data LIMIT {batchsize} OFFSET {offset}")
        rows = cursor.fetchall()
        if not rows:
            break
        yield rows
        offset += batchsize
    cursor.close()
    connection.close()

def batch_processing(batchsize):
    """Generator that yields users over age 25"""
    for batch in streamusersinbatches(batchsize):
        for user in batch:
            if user['age'] > 25:
                yield user
