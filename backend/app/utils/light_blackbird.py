import asyncio
import json
import os
import sys
import time
import warnings
# import csv
from datetime import datetime
import base64
import Requester
import aiohttp
from bs4 import BeautifulSoup


req = Requester.get(url=f"https://api.github.com/repos/p1ngul1n0/blackbird/contents/data.json")
if req and req.status_code == 200:
    req = req.json()
    content = base64.b64decode(req['content'])
    file = content.decode("utf8")
searchData = json.load(file)
currentOs = sys.platform
path = os.path.dirname(__file__)
warnings.filterwarnings("ignore")

#useragents = open(os.path.join(os.path.abspath(__file__),'..','useragent.txt'),'w').read().splitlines()


async def findUsername(username, interfaceType, flag_csv=False):
    start_time = time.time()
    timeout = aiohttp.ClientTimeout(total=20)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = []
        for u in searchData["sites"]:
            task = asyncio.ensure_future(
                makeRequest(session, u, username, interfaceType)
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        executionTime = round(time.time() - start_time, 1)
        userJson = {
            "search-params": {
                "username": username,
                "sites-number": len(searchData["sites"]),
                "date": now,
                "execution-time": executionTime,
            },
            "sites": [],
        }
        for x in results:
            userJson["sites"].append(x)
        # pathSave = os.path.join(path, "results", username + ".json")
        # userFile = open(pathSave, "w")
        # json.dump(userJson, userFile, indent=4, sort_keys=True)

        # if flag_csv:
        #     exportCsv(userJson)

        return userJson


async def makeRequest(session, u, username, interfaceType):
    url = u["url"].format(username=username)
    jsonBody = None
    useragent = Requester.get_user_agent()
    headers = {"User-Agent": useragent}
    metadata = []
    if "headers" in u:
        headers.update(json.loads(u["headers"]))
    if "json" in u:
        jsonBody = u["json"].format(username=username)
        jsonBody = json.loads(jsonBody)
    try:
        async with session.request(
            u["method"], url, json=jsonBody, proxy=None, headers=headers, ssl=False
        ) as response:
            responseContent = await response.text()
            if (
                "content-type" in response.headers
                and "application/json" in response.headers["Content-Type"]
            ):
                jsonData = await response.json()
            else:
                soup = BeautifulSoup(responseContent, "html.parser")

            if eval(u["valid"]):
                if "metadata" in u:
                    metadata = []
                    for d in u["metadata"]:
                        try:
                            value = eval(d["value"]).strip("\t\r\n")
                            metadata.append(
                                {"type": d["type"], "key": d["key"], "value": value}
                            )
                        except Exception as e:
                            pass
                return {
                    "id": u["id"],
                    "app": u["app"],
                    "url": url,
                    "response-status": f"{response.status} {response.reason}",
                    "status": "FOUND",
                    "error-message": None,
                    "metadata": metadata,
                }
            else:
                return {
                    "id": u["id"],
                    "app": u["app"],
                    "url": url,
                    "response-status": f"{response.status} {response.reason}",
                    "status": "NOT FOUND",
                    "error-message": None,
                    "metadata": metadata,
                }
    except Exception as e:
        return {
            "id": u["id"],
            "app": u["app"],
            "url": url,
            "response-status": None,
            "status": "ERROR",
            "error-message": repr(e),
            "metadata": metadata,
        }

# def exportCsv(userJson):
#     pathSave = os.path.join(
#         path, "results", userJson["search-params"]["username"] + ".csv"
#     )
#     with open(pathSave, "w", newline="", encoding="utf-8") as file:
#         writer = csv.writer(file)
#         writer.writerow(["ID", "App", "URL", "response-status", "metadata", "result"])

#         for u in userJson["sites"]:
#             writer.writerow(
#                 [
#                     u["id"],
#                     u["app"],
#                     u["url"],
#                     u["response-status"],
#                     json.dumps(u["metadata"]),
#                     u["status"],
#                 ]
#             )
#     return True


async def run_light_blacbird(username : str) :
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except:
            pass

        asyncio.run(findUsername(username, "CLI"))


# if __name__ == "__main__":
    # init()

    # parser = argparse.ArgumentParser(
    #     description="An OSINT tool to search for accounts by username in social networks."
    # )
    # parser.add_argument(
    #     "-u",
    #     action="store",
    #     dest="username",
    #     required=False,
    #     help="The target username.",
    # )
    # parser.add_argument(
    #     "--list-sites",
    #     action="store_true",
    #     dest="list",
    #     required=False,
    #     help="List all sites currently supported.",
    # )
    # parser.add_argument(
    #     "-f", action="store", dest="file", required=False, help="Read results file."
    # )
    # parser.add_argument(
    #     "--web", action="store_true", dest="web", required=False, help="Run webserver."
    # )
    # parser.add_argument(
    #     "--proxy",
    #     action="store",
    #     dest="proxy",
    #     required=False,
    #     help="Proxy to send requests through.E.g: --proxy http://127.0.0.1:8080 ",
    # )
    # parser.add_argument(
    #     "--show-all",
    #     action="store_true",
    #     dest="showAll",
    #     required=False,
    #     help="Show all results.",
    # )
    # parser.add_argument(
    #     "--csv",
    #     action="store_true",
    #     dest="csv",
    #     required=False,
    #     help="Export results to CSV file.",
    # )
    # arguments = parser.parse_args()

    # if arguments.proxy:
    #     proxy = arguments.proxy
    # showAll = False
    # if arguments.showAll:
    #     showAll = arguments.showAll

    # if arguments.web:
    #     print("[!] Started WebServer on http://127.0.0.1:9797/")
    #     command = subprocess.run((sys.executable, "webserver.py"))
    #     command.check_returncode()

    # if arguments.username:
    #     try:
    #         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    #     except:
    #         pass
    #     interfaceType = "CLI"
    #     asyncio.run(findUsername(arguments.username, interfaceType, arguments.csv))
    # elif arguments.list:
    #     list_sites()
    # elif arguments.file:
    #     read_results(arguments.file)
