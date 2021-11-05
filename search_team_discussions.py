import os
import sys

import requests

ORG = os.environ['ORG']
USER = os.environ['USER']
PERSONAL_ACCESS_TOKEN = os.environ['PERSONAL_ACCESS_TOKEN']
GITHUB_API_URL = 'https://api.github.com'
HEADERS = {'Accept': 'application/vnd.github.v3+json'}
SEARCH_TERMS = [arg.lower() for arg in sys.argv[1:]]

get_teams = requests.get(
    url=f'{GITHUB_API_URL}/orgs/{ORG}/teams',
    auth=(USER, PERSONAL_ACCESS_TOKEN),
    headers=HEADERS,
)

search_terms_str = ', '.join([f'"{term}"' for term in SEARCH_TERMS])
print(f'Searching for term(s): {search_terms_str} ...')

for team in get_teams.json():
    team_slug = team['slug']
    team_name = team['name']
    print(f'In team {team_name}')

    url = f'{GITHUB_API_URL}/orgs/{ORG}/teams/{team_slug}/discussions'
    limit = 20
    page = 1
    next_page = True
    while next_page:
        params = {'per_page': limit, 'page': page}
        get_discussions = requests.get(
            url=url, auth=(USER, PERSONAL_ACCESS_TOKEN), headers=HEADERS, params=params
        )
        get_discussions_json = get_discussions.json()
        if len(get_discussions_json) < limit:
            next_page = False
        page += 1
        for discussion in get_discussions_json:
            dis_title = discussion['title']
            title_and_body = ' '.join([dis_title, discussion['body']])
            if any([word for word in SEARCH_TERMS if word not in title_and_body.lower()]):
                continue

            print(f'Found in discussion "{dis_title}" at {discussion["html_url"]}')

print('Search complete')
