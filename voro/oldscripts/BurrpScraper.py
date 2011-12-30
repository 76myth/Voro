import argparse
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import pickle
import sys
import time


	

sys.setrecursionlimit(10000)
Parser=argparse.ArgumentParser(description='Locality,Cuisine')
Parser.add_argument('LocationPlacetype', nargs='+')
Args=Parser.parse_args()

DictForLocationPlacetype=vars(Args)
ListForLocationplusPlacetype=DictForLocationPlacetype['LocationPlacetype']
Locations=[]
Placetype=[]
i=0
for temp in ListForLocationplusPlacetype:
	if temp == ',':
		i=i+1
		break

for temp in ListForLocationplusPlacetype[0:i+1]:
	if temp[-1]=='W':
		Locations.append(temp[0:-1]+'+'+'West')
	else:
		Locations.append(temp[0:-1]+'+'+'East')

Placetype=ListForLocationplusPlacetype[i+2:]

BurrpURL=[]
BurrpURL1='http://mumbai.burrp.com/find.html?p=1&oN=Western+Suburbs&q='
BurrpURL2='&n=&zc=&s=OR&zone=Western+Suburbs&fltLocalities='

for place in Placetype:
	tempURL1=BurrpURL1+place
	for location in Locations:
		tempURL2=BurrpURL2+location
		BurrpURL.append(tempURL1+tempURL2)


HashForPlaceWithURL={}

BurrpURLWithPageNos=[]
for eachURL in BurrpURL:
	Page=urllib2.urlopen(eachURL)
	Soup=BeautifulSoup(Page)
	PageSpan=Soup.find('span',{'class':'float_l'})
	if PageSpan is None:
		continue
	Pageno=int(re.findall(r'\d+',PageSpan.text)[0])
	if Pageno < 100:
		NoOfPages=Pageno/10+1
	else:
		NoOfPages=10
	for x in range(1,NoOfPages+1):
		BurrpURLWithPageNos.append(eachURL.replace('p=1','p='+str(x)))		
	


for eachURL in BurrpURLWithPageNos:
	Page=urllib2.urlopen(eachURL)
	Soup=BeautifulSoup(Page)
        region=Soup.find('input',{'checked':'checked'})['value']
	for tag in Soup('div',{'class':'search_row_title'}):
		GetHyperlink=tag('a')

		hlink=GetHyperlink[0].text	

		urlstatus=False
		if HashForPlaceWithURL.has_key(hlink):
			URLsForaPlace=HashForPlaceWithURL[hlink]['links']
			for url in URLsForaPlace:
				if url==GetHyperlink[0]['href']:
					urlstatus=True
					break
			
								
				
				
		if urlstatus:
			continue
		else:
								
			if tag('span')[1].has_key('title'):
				rating=tag('span')[1]['title']
								
			if tag('span')[0].has_key('title'):
				rating=tag('span')[0]['title']
								
				
				

		HashForPlaceWithURL[hlink]={}	
		try:HashForPlaceWithURL[hlink]['rating'],HashForPlaceWithURL[hlink]['region'],HashForPlaceWithURL[hlink]['links']
				
		except KeyError:			
			HashForPlaceWithURL[hlink]['rating']=[rating]
			HashForPlaceWithURL[hlink]['region']=[region]
			HashForPlaceWithURL[hlink]['links']=[GetHyperlink[0]['href']]
		else:
			HashForPlaceWithURL[hlink]['rating'].append(rating)
			HashForPlaceWithURL[hlink]['region'].append(region)
			HashForPlaceWithURL[hlink]['links'].append(GetHyperlink[0]['href'])
		
pickle.dump(HashForPlaceWithURL, open('burrp-data','w'))	
f=open('burrp-data.txt','w')
f.write(str(HashForPlaceWithURL))
f.close()



