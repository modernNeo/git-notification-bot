import requests


def get_owners(bot_token):
    url = "https://slack.com/api/users.list"
    headers = {'Authorization': f"Bearer {bot_token}"}

    owners = []
    cursor = None

    while True:
        params = {"cursor": cursor} if cursor else {}
        resp = requests.get(url, headers=headers, params=params).json()

        if not resp.get("ok"):
            break

        # Extract owners from the current page
        for member in resp.get("members", []):
            if (member.get("is_owner") or member.get("is_primary_owner")) \
                    and not member.get("deleted") \
                    and not member.get("is_bot"):
                owners.append(member["id"])

        # Check if there is another page
        cursor = resp.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break

    return owners
