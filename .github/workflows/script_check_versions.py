import os

print("Jest GIT!")

print(os.getenv('FAKE_TOKEN'))

FAKE_TOKEN = os.environ['FAKE_TOKEN']
THE_GITHUB_TOKEN = os.environ['THE_GITHUB_TOKEN']
URL_PULL = os.environ['URL_PULL']
REPOSITORY = os.environ['REPOSITORY']
COMPARASION_BASE = os.environ['COMPARASION_BASE']

print(FAKE_TOKEN)
print(URL_PULL)
print(REPOSITORY)
print(COMPARASION_BASE)
