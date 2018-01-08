#!/usr/bin/python
#Git stars downloader
#for when you want all the repos they starred.
#Lordsaibat (11/14/2016)


import httplib
from BeautifulSoup import BeautifulSoup
import urllib2
import os
import argparse
parser = argparse.ArgumentParser(description="Download all the repos stared by this user")
parser.add_argument("--user", dest="user", help="User you want to download thier starred projects")
args=parser.parse_args()


projects=[]
repo=[]

def add_links(newsoup):
 test=newsoup.findAll("div", {"class": "d-inline-block mb-1"})
 for links in test:
  project_link=links.find(href=True)['href']
  projects.append(project_link)

def next_page(page,git_user):
 #temp=newsoup.findAll('div', {"class":"pagination"})
 #link=temp[0].find(href=True)['href']
 #print link
 #conn = httplib.HTTPSConnection("github.com")
 #conn.request("GET", link)
 #r1 = conn.getresponse()
 #data=r1.read()
 conn = httplib.HTTPSConnection("github.com")
 location = "/stars/" + git_user + "?diection=desc&page=" + str(page)
 conn.request("GET", location)
 r1 = conn.getresponse()
 data=r1.read()
 freshsoup=BeautifulSoup(data)
 return freshsoup

def test_page(newsoup):
 temp=newsoup.find("div", {"class":"blankslate"})
 if (temp > 0):
  return 1
 else: 
  return 0
 
def get_stars(git_user):
 #connection to github
 conn = httplib.HTTPSConnection("github.com")
 star_location = "/stars/" + git_user
 conn.request("GET", star_location)
 r1 = conn.getresponse()
 data=r1.read()
 soup=BeautifulSoup(data)
 return soup

def goto_page(link):
 conn = httplib.HTTPSConnection("github.com")
 conn.request("GET", link)
 r1 = conn.getresponse()
 data=r1.read()
 soup=BeautifulSoup(data)
 return soup

def get_repo(soup):
 test=soup.findAll("input", { "type":"text"})
 repo_link=test[1]["value"]
 return repo_link

def download_repo(link):
 git_command = "git clone " + link
 print "Downloading: " + git_command
 os.system(git_command)

stars_page=get_stars(args.user)
print "Building List to download"
build=True
x=1
while (build == True):
 add_links(stars_page)
 if (test_page(stars_page) == 0):
   stars_page=next_page(x,args.user)
 else:
   build=False  
 x=x+1

print "List of projects building"
print "Starting to Download projects"
for project in projects:
 newsoup=goto_page(project) 
 repo_link=get_repo(newsoup)
 download_repo(repo_link)
