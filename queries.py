import json


def read_queries(func):
    with open('queries.json', 'r') as f:
        queries = json.load(f)

    def query_getter():
        query = func(queries)
        return query

    return query_getter


@read_queries
def get_count_query(queries):
    return queries['ROOMS_WITH_COUNT_STUDENTS_QUERY']


@read_queries
def get_avg_query(queries):
    return queries['ROOMS_WITH_MIN_AVERAGE_AGE_QUERY']

@read_queries
def get_dif_query(queries):
    return queries['ROOMS_WITH_MAXIMUM_DIFFERENCE_IN_AGE_QUERY']

@read_queries
def get_sex_query(queries):
    return queries['ROOMS_WITH_BOTH_SEXES_QUERY']
