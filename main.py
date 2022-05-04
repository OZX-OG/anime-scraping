from bs4 import BeautifulSoup
from lxml import etree
from time import sleep
from os import system
import re
import requests

while True:
    #### variables ####
    search = str(input("Enter the name of the anime: "))
    site = f"https://anime4up.art/?search_param=animes&s={search.strip()}"
    allsite = []
    newsites = []
    linkes = []

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

    if len(newsites) == 0: print("No anime found"); continue
    else: break

dic = {}
anime_names_list = []
# print(newsites)
for indx, value in enumerate(newsites):
    # print(value[27:-1].replace("-", " "))
    dom = etree.HTML(str(soup))
    title = dom.xpath(f'/html/body/div[4]/div/div/div[{indx+1}]/div/div[2]/div[2]/h3/a')[0].text 
    anime_names_list.append(title)
    dic.update({indx: value})

anime_names_index = 1
for i in range(len(anime_names_list)):
    print(str(anime_names_index) + " :  " + anime_names_list[i])
    anime_names_index += 1


while True:
    try:
        anime_number = int(input("Enter the number of the anime you want: "))
        if anime_number > len(anime_names_list) or anime_number < 1:
            print("Enter a valid number")
            continue
    except ValueError:
        print(f"Please Enter Numbers, You can select between 1 and {anime_names_index-1}")
        sleep(1)
        continue
    break


newsites = [dic[anime_number - 1]]
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

# print(link_episodes)


anime_name = anime_names_list[anime_number - 1]
# replace "/"?"|"\"/"*":"<">"\"
awedi = anime_name.replace("/", "-").replace("?", "-").replace("|", "-").replace("\\", "-").replace(
    "\"", "-").replace("\"", "-").replace("*", "-").replace(":", "-").replace("<", "-").replace(">", "-")
f = open(f"{awedi}_anime_file.txt", "w")
f.write(
    f"---------- { anime_name } has {len(link_episodes)} episodes   ----------\n")


########## get the videos link from the episodes ##########
system("cls")
episode_number = 0

for l in link_episodes:
    r = requests.get(l)
    soup = BeautifulSoup(r.content, "html.parser")
    result = soup.find_all("a", attrs={"data-ep-url": re.compile("^https:")})

    index = 1
    episode_number += 1
    print("--------------------------------------------------------------------------------")
    f.write(f"episode number: {episode_number}/{len(link_episodes)}\n\n")
    print(f"episode number: {episode_number}/{len(link_episodes)}\n")

    for i in result:
        f.write(f"{index} : {i.get('data-ep-url')}")
        print(f"{index} : {i.get('data-ep-url')}")        
        index += 1

    f.write("---------------------------------------------------------------------------------------------\n\n")
    
f.close()
print("Done.")
input("press Enter to exit\n")
