from bs4 import BeautifulSoup
from urllib.error import URLError
from urllib import request
from http import client
import re
import socket
import time

download_sleep_time = 8
time_out = 10
invalid_url_list = []
visited_url = ([])
escape_list = [
               re.compile(".*(.apk)$"),
               re.compile(".*(.exe)$"),
               re.compile(".*(.pdf)$")
               ]
socket.setdefaulttimeout(time_out)


def find_url(html, parent_url):
    global invalid_url_list
    global start_url
    global visited_url
    global domain_key
    unchecked_urls = []

    # print("before bsObj") # to be deleted
    bsObj = BeautifulSoup(html.read())
    # print("in bsObj")# to be deleted
    find_a_tags = bsObj.findAll("a")
    for content in find_a_tags:
        #print(content)
        try:
            unchecked_urls.append(content["href"])
        except KeyError:
            continue
    url_list = check_and_format(unchecked_urls)
    for url in url_list:
        # print("url in url_list")#to be deleted
        if url not in visited_url:
            visited_url.append(url)
            # print("find", url)  # to be deleted
            try:
                # print("try to open url")#to be deleted
                html = request.urlopen(url)
                print(url)
                if re.compile(".*{}.*".format(domain_key)).match(url):
                    find_url(html, url)
            except URLError:
                invalid_url_list.append([parent_url, url])
                print("ERROR!!! ", url)

            except socket.timeout:
                time.sleep(download_sleep_time)
                continue

            except client.RemoteDisconnected:
                time.sleep(download_sleep_time)
                continue

        else:
            continue


def check_and_format(unchecked_urls):
    global start_url
    url_list = []

    for url in unchecked_urls:
        escape = 0
        for regular_expression in escape_list:
            if regular_expression.match(url):
                escape = 1
                break

        if escape == 1:
            continue

        if re.compile("^(http)").match(url):
            url_list.append(url)
        elif re.compile("^(www)").match(url):
            url = "http://" + url
            url_list.append(url)
        elif re.compile(".*www.*").match(url):
            index = url.rfind("www")
            url = "http://" + url[index:len(url)]
            url_list.append(url)
        elif re.compile("^/.*").match(url):
            url = start_url + url
            url_list.append(url)

    return url_list


while True:
    start_url = input("Please input the main address:\n")
    try:
        html = request.urlopen(start_url)
        break
    except URLError :
        print("wrong address!")
    except ValueError:
        print("wrong address! try to add \"http://\"")

domain_key = input("please input the domain_key:\n")
find_url(html, start_url)
print("find_url already done!")
if len(invalid_url_list) == 0:
    print("well done!\nno invalid url found!")
else:
    print("scan finished!")

for invalid_url_info in invalid_url_list:
    print("parent_url:{}  invalid_url:{}".format(invalid_url_info[0].rjust(100), invalid_url_info[1].rjust(100)))




