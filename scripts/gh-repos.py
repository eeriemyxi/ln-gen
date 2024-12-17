import json
import urllib.request

LNGENLINKS = []
USERNAME = "eeriemyxi"

req = urllib.request.urlopen(
    f"https://api.github.com/users/{USERNAME}/repos?type=sources&visibility=public"
)

for repo in json.loads(req.read()):
    if repo["fork"]:
        continue
    LNGENLINKS.append([repo["name"], repo["html_url"]])

if __name__ == "__main__":
    print("[INFO]", LNGENLINKS)
