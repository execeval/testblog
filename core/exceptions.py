from django.db import DataError


class PreferenceMissing(DataError):
    def __init__(self, pref_list):
        super().__init__(f'Preference in database is missing\nPreferences list: {pref_list}')


class LimitMissing(DataError):
    def __init__(self, limit_name):
        super().__init__(f'Limit {limit_name} in database is missing')
