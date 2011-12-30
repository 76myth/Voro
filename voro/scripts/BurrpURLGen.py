import urllib2
from BeautifulSoup import BeautifulSoup
import re
import pickle
import sys
import time

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text



sys.setrecursionlimit(10000)
MUMBAIURL="http://mumbai.burrp.com/~/q_Restaurants#4"
Page=urllib2.urlopen(MUMBAIURL)
Soup=BeautifulSoup(Page)
##ZoneText="Select Zone"
##Zones=[]
SelectTag=Soup.find('div',{'class':'col02'})
##OptionTag=SelectTag('option') 
##for option in OptionTag:
##	Zones.append(option['value'])

##Zones.remove(ZoneText)
JSTag=SelectTag('script')
replaceDict={'1,':'','escapedLoc = ':'','[':'',']':'',';':'','"':''}
LocalityValues=replace_all(JSTag[0].text,replaceDict).replace(' ','+').split(',')
LocalityValues.remove('')
MUMBAIMAINURL="http://mumbai.burrp.com/find.html?oN=&q=Restaurants&n=&zc=&s=OR&zone=Select+Zone&fltLocalities="

BurrpLocalityURL=[]
for locality in LocalityValues:
		BurrpLocalityURL.append(MUMBAIMAINURL+locality+'&p=1') 

f=open('burrp-data.txt','w')
for item in BurrpLocalityURL:
	print>>f,item

f.close()


    
