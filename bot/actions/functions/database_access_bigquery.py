from google.cloud import bigquery


# Does not account for duplicates
def add_user(user_uri, user_name):
    """ Add user URI to database user table
    Args:
        user_uri (string): The user's URI
        user_name (string): The user's name
    """

    client = bigquery.Client()

    query = """
        INSERT INTO whatsapp_bot.users(user_uri, user_name)
        VALUES(@user_uri, @user_name)
    """

    query_2 = """
        INSERT INTO whatsapp_bot.users(user_uri, user_name)
        SELECT value FROM (SELECT 1 AS value) 
        LEFT JOIN whatsapp_bot.users  
        ON user_uri = value
        WHERE user_uri IS NULL
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_uri", "STRING", user_uri),
            bigquery.ScalarQueryParameter("user_name", "STRING", user_name),
        ]
    )

    query_job = client.query(query_2, job_config=job_config)



