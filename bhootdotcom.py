"""
Version 0.3 (beta)
author alrazi
notredamecollegedhaka<3
29-06-2021, HSC awaiting, Cold Monsoon weather, Zero point, Khulna

So basically the story starts with my previous even bigger project, webscraping 9.5 years of bhootFM...

I was trying to impress myself thinking that I could master BeautifulSoup and become a webscraper all
in all since my target was to become proficient in programming and get accustomed tothe changing nature 
of the web.

There aren't that many popular radio shows out there but this one is being hosted online on Shadhin App(?)
which releases Bangladeshi podcasts and this sort of thing. It's half show half podcast since witness and
messengers bring horror stories along with witnesses sending emails. Anyways, I digress.

I found a small loophole in this project and that is:

    A Pattern...

    What kind of pattern you might say?

    Look at this:

        Episode Link: https://episodebd.com/download*/{4-digit-number}/{episode name} 
        
        Download Link: https://episodebd.com/download*/{4-digit-number}.html
        
        *not sure what's here, maybe more! however that's a redundant issue
    
    It means I can just scrape the paginations and voila! don't need to tree down to every episode page and waste bandwidth or time!!
    It might seem unimportant but if this show runs as long as bhootFM did, that's going to come in handy in future when using this 
    scraper to download all that.

You are free to use this code as long as you are grateful and you attribute me.

If the code fails, just check what's wrong with episodebd.com, or beautiful soup. It works alright on python 3.6, 3.7, 3.8.

If you run it on py-2.7, you should try changing the html.parser to HTMLparser

Thanks!
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
pages = [f"https://episodebd.com/categorylist/4821/new2old/{i}/BhootCom_all_Episode_With_Rj_Russell.html" for i in range(1,8)]

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
    for i in tqdm(pages):
        pagination(i)
    for i in episodes:
        
        download_file(i)
    print("\n\n[bold red]NUMBER OF TOTAL EPISODES[/bold red]\t"+str(episodes.__len__()))
    print("[bold red]NUMBER OF DOWNLOADED EPISODES[/bold red]\t"+str(j))
    input("Press Enter to exit")