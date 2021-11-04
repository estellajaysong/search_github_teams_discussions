# Search Github Teams Discussions

Script to search Github teams discussions for a specific term or terms in the title or body.

## Authentication

Fill out `config.sh` 

[Create a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-token)

The scopes required are `read:org` and `read:discussion`


## Usage

```
source config.sh
python search_team_discussions.py search_term1 search_term2 search_term3
```
You can have any number of search terms, and they are not case sensitive.

Results will be logged in the console.
