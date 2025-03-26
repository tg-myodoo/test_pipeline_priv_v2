import os

print("Jest GIT!")

print(os.getenv('FAKE_TOKEN'))

FAKE_TOKEN = os.environ['FAKE_TOKEN']
THE_GITHUB_TOKEN = os.environ['THE_GITHUB_TOKEN']
URL_PULL = os.environ['URL_PULL']
REPOSITORY = os.environ['REPOSITORY']
COMPARASION_BASE = os.environ['COMPARASION_BASE']

GITHUB_WORKSPACE = os.environ['GITHUB_WORKSPACE']

print(FAKE_TOKEN)
print(URL_PULL)
print(REPOSITORY)
print(COMPARASION_BASE)
print(GITHUB_WORKSPACE)

print("GITHUB_WORKSPACE", os.listdir(GITHUB_WORKSPACE))

with open(GITHUB_WORKSPACE+"/mod1.py", 'r') as file:
      # Read the content of the file
      file_content = file.read()
      
      # Print the content
      print(file_content)

