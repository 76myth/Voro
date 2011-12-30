import urllib2
import re
import pickle
import sys
import time
from BeautifulSoup import BeautifulSoup

sys.setrecursionlimit(10000)
ipaddress=[]
for counter in range(1,12):
    page=urllib2.urlopen('http://hidemyass.com/proxy-list/search-225390/'+str(counter))
    soup=BeautifulSoup(page)
    trtag1=soup.findAll('tr',{'class':''})
    trtag2=soup.findAll('tr',{'class':'altshade'})
    f=open('proxydata.txt','w')
    for val in trtag1:
        ipaddress.append(val('span')[1].text)
        
    for val in trtag2:
        ipaddress.append(val('span')[1].text)



f=open('proxydata.txt','w')
for item in ipaddress:
	print>>f,item

f.close()
