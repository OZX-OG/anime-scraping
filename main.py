from bs4 import BeautifulSoup
from lxml import etree
import re
import requests

search = str(input("Enter the name of the anime: "))
site = f"https://anime4up.art/?search_param=animes&s={search}"
allsite = []
newsites = []
linkes = []

# get the last episode number


def get_episode(episode):
    r = requests.get(episode)
    soup = BeautifulSoup(r.content, "html.parser")

    dom = etree.HTML(str(soup))
    title = dom.xpath('/html/body/div[2]/div/h3')[0].text
    episode_number = ""
    for i in title:
        if i.isdigit():
            episode_number += i
    return episode_number

########## get all the links of search ##########


r = requests.get(site)
soup = BeautifulSoup(r.content, "html.parser")
for link in soup.findAll('a', attrs={'href': re.compile("^https:")}):
    allsite.append(link.get('href'))

########## get only animes links ##########
for i in allsite:
    try:
        if i[:27] == "https://anime4up.art/anime/":
            if i not in newsites:
                newsites.append(i)
    except IndexError:
        pass


########## chache the links the anime you want ##########
x = ""
dic = {}
for i in newsites:
    success = 0
    print(i[27:-1].replace("-", " "))
    x = i[27:-1].replace("-", " ")
    for indx, value in enumerate(search):
        if value == x[indx]:
            success += 1

    dic.update({i: success})

sort_orders = sorted(dic.items(), key=lambda x: x[1], reverse=True)
newsites = [sort_orders[0][0]]
# print("newsite: ", newsites)
allsite = []
########## get all the eposide links ##########
for l in newsites:
    r = requests.get(l)
    soup = BeautifulSoup(r.content, "html.parser")
    for link in soup.findAll('a', attrs={'href': re.compile("^https:")}):
        allsite.append(link.get('href'))

########## get only eposide links ##########
link_episodes = []
for i in allsite:
    if "episode" in i:
        if not i in link_episodes:
            link_episodes.append(i)

print(link_episodes)


number_of_last_episode = get_episode(link_episodes[-1])
anime_name = sort_orders[0][0][27:-1].replace("-", " ")
f = open(f"{search}_anime_file.txt", "w")
f.write(
    f"---------- { anime_name } has {number_of_last_episode} episodes   ----------\n")


########## get the videos link from the episodes ##########
for l in link_episodes:
    r = requests.get(l)
    soup = BeautifulSoup(r.content, "html.parser")

    index = 1
    episode_number = get_episode(l)
    f.write(f"episode number: {episode_number}/{len(link_episodes)}\n\n")
    print(f"episode number: {episode_number}/{len(link_episodes)}\n")
    for i in range(50):
        try:
            result = soup.findAll('li', attrs={})[
                i].find('a').get('data-ep-url')
        except AttributeError:
            pass
        if not result == None:

            f.write(f"{index}: {result} \n")
            linkes.append(result)
            print(index, ": ", result)
            index += 1
    f.write("---------------------------------------------------------------------------------------------\n\n")
    print("--------------------------------------------------------------------------------")


f.close()
print("Finsihed")
