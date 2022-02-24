from core.models import Preference, Limit


def get_preferences_unlazy(pref_list):
    return list(Preference.objects.filter(name__in=pref_list).values_list('value', flat=True))


def get_limit(limit_name):
    return Limit.objects.get(name=limit_name).value
