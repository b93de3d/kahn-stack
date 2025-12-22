from django.db import connection


def with_query_count(func):
    # Clear previous queries to start fresh
    connection.queries.clear()

    # Call the function you want to analyze
    ret = func()

    # Get the number of database hits
    number_of_queries = len(connection.queries)

    print(f"Number of DB hits: {number_of_queries}")
    # for q in connection.queries:
    #     print(f"   ---> {q}")

    return ret
