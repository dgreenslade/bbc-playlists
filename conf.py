from datetime import date, timedelta

def config(key):
    """
    Simple method to hold the configuration in.  Possibly replace this with ConfigParser
    and separate YAML file or similar.  Or hold as separte .py file.
    """

    config_dict = {
        'bbc_show_url': 'https://www.bbc.co.uk/schedules/p00fzl65/',
        'start_date': date(2021, 2, 1),
        'end_date': date(2021, 2, 1),
        'mongodb_host': 'localhost',
        'mongodb_name': 'test'
    }

    return config_dict[key]