from account.models import Account
from django.core.exceptions import ObjectDoesNotExist
from typing import Optional


def get_account_by_username(username: str) -> Optional[Account]:
    try:
        return Account.objects.get(username=username)
    except ObjectDoesNotExist:
        return None
