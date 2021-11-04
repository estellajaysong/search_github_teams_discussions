import requests
import sys
import os

# Step 1. source config.sh

ORG = os.environ['ORG']
USER = os.environ['USER']
PERSONAL_ACCESS_TOKEN = os.environ['PERSONAL_ACCESS_TOKEN']
GITHUB_API_URL = 'https://api.github.com'
HEADERS = {'Accept': 'application/vnd.github.v3+json'}
SEARCH_TERM = sys.argv[1]


# Step 2. source config.sh
get_teams = requests.get(
    url=f'{GITHUB_API_URL}/orgs/{ORG}/teams',
    auth=(USER, PERSONAL_ACCESS_TOKEN),
    headers=HEADERS,
)
print(f'Searching for "{SEARCH_TERM}" ...')
for team in get_teams.json():

    team_slug = team['slug']
    team_name = team['name']
    print(f'In team {team_name}')

    url = f'{GITHUB_API_URL}/orgs/{ORG}/teams/{team_slug}/discussions'
    limit = 20
    page = 1
    while True:
        params = {'per_page': limit, 'page': page}
        get_discussions = requests.get(
            url=url, auth=(USER, PERSONAL_ACCESS_TOKEN), headers=HEADERS, params=params
        )
        get_discussions_json = get_discussions.json()
        if len(get_discussions_json) < limit:
            break
        page += 1
        for discussion in get_discussions_json:
            dis_title = discussion['title']
            if 'twil' not in dis_title.lower():
                continue
            if SEARCH_TERM in dis_title or SEARCH_TERM in discussion['body']:
                print(
                    f'Found in discussion "{dis_title}" at {discussion["html_url"]}'
                )
