from django.db.models import Prefetch
import core.models as core_models
from django.db import connection


def do_something():
    pass


def with_query_count(func):
    # Clear previous queries to start fresh
    connection.queries.clear()

    # Call the function you want to analyze
    func()

    # Get the number of database hits
    number_of_queries = len(connection.queries)

    print(f"Number of DB hits: {number_of_queries}")
    for q in connection.queries:
        print(f"   ---> {q}")


if __name__ == "__main__":
    with_query_count(do_something)
