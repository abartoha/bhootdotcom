"""
Version 1.0.0 (release)
author alrazi
notre dame college dhaka
17-07-2021, Waiting for my COVID-19 test results. I am not given the order to be immunized.

I am very happy to announce to you that I hvae finalized the release version of my bhootdotcom
autoscraping system. Please use it without care! you can readily turn it into a binary. It has
rich text enabled. It will look nice even for a consoe application. I am happy that it was a v
-ery satisfying and fulfilling side project. Mission Completed.
"""

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from os import listdir, getcwd, mkdir
from rich import print
from rich.style import Style
from rich.console import Console
console = Console()
starting_style = Style(color="green", blink=True, bold=True)
already_downloaded_style = Style(color="purple", underline=True, encircle=True)
if not listdir().__contains__("Files"):
    mkdir("Files")
j = 0
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
episodes = []
list_dir = listdir(getcwd()+"\\Files")

# pages = [f"https://episodebd.com/categorylist/4821/new2old/{i}/BhootCom_all_Episode_With_Rj_Russell.html" for i in range(1,8)]

def getSoup(url):
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html.parser')

def download_file(episode):
    url2, name = episode
    if not list_dir.__contains__(f"{name}.mp3"):
        print("[bold red]NEW EPISODE![/bold red]\t"+name)
        print("[italic green]Downloading....[/italic green]")
        url = f"https://episodebd.com/file/download/{url2}.html"

        response = requests.get(url, stream=True, headers = headers)
        total_size_in_bytes= int(response.headers.get('content-length', 0))
        block_size = 1024 #1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(f'Files/{name}.mp3', 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("[red]ERROR, something went wrong[/red]")
        global j
        j += 1
    else:
        console.print("Already downloaded\t[yellow]"+i[1]+"[/yellow]", style=already_downloaded_style)

def rename(name):
    #it's job is to remove all the bullcrap from the name and make date/episode finding easier
    name = name.replace("BhootCom_","")
    name = name.replace("Episode_","")
    name = name.replace("by_Rj_Russell","")
    name = name.replace("mp3.html","")
    name = name.replace("with_RJ_RUSSEL","")
    name = name.replace("BDLove24Com","")
    return name

def pagination(url):
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.content,'html.parser')
    links = [i['href'] for i in soup.find_all("a", href=True)]

    for i in links:
        if not i.__contains__("4821") and i.__contains__("/download/"):
            episode = (int(i.split("/")[4]),rename(i.split("/")[-1]))
            episodes.append(episode)
                # global j #YES! i used a global, so what! It was just for testing purpose!! 
                # #print(str(episode[0]) + " " + episode[1] + " " + str(j))
                # j += 1
    

if __name__ == "__main__":
    console.print("STARTING PAGINATION...", style=starting_style)
    pages = ["https://episodebd.com/categorylist/4821/new2old/1/BhootCom_all_Episode_With_Rj_Russell.html"]
    for i in tqdm(pages):
        soup = getSoup(i)
        pgn = soup.find('div', attrs={"class":"pgn"})
        pgn_a_noclass = [i['href'] for i in pgn.find_all('a', attrs={'class':None, 'id':None}) if i['href'].__contains__('https://episodebd.com/categorylist/4821/new2old/')]
        for k in pgn_a_noclass:
            if not pages.__contains__(k):
                pages.append(k)
        pagination(i)
    for i in episodes:
        download_file(i)
    print("\n\n[bold red]NUMBER OF TOTAL EPISODES[/bold red]\t"+str(episodes.__len__()))
    print("[bold red]NUMBER OF DOWNLOADED EPISODES[/bold red]\t"+str(j))
    input("Press Enter to exit")