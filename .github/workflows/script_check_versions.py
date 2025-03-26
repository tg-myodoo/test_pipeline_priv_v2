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

print("_", os.listdir("/"))
# ['home', 'sys', 'lib64', 'proc', 'dev', 'lib', 'var', 'etc', 'srv', 'root', 'boot', 'run', 'opt', 'snap', 'mnt', 
# 'imagegeneration', 'usr', 'media', 'sbin.usr-is-merged', 'lib.usr-is-merged', 'tmp', 'lib32', 'bin.usr-is-merged', 'data', 'sbin', 'bin', 'lost+found']
print("home", os.listdir("/home"))
print("sys", os.listdir("/sys"))
print("run", os.listdir("/run"))
print("usr", os.listdir("/usr"))
print("tmp", os.listdir("/tmp"))
print("data", os.listdir("/data"))
print("bin", os.listdir("/bin"))
