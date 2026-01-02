import requests


def get_account_info(account_id:str) -> None|str:
    return requests.get(
        f"https://atlassian.modernneo.com/rest/api/3/user/email/?accountId={account_id}",
        headers={"Accept" : "application/json"}
    ).json()['email']