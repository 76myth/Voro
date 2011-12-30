import urllib2
import re
import pickle
import sys
import time
from BeautifulSoup import BeautifulSoup

sys.setrecursionlimit(10000)
##f=open('120865089.html','r').read()
##f=open('110135099.html','r').read()
hotelinformation={}
proxyfile=open('proxydata.txt','r')
proxylist=proxyfile.readlines()
for ipaddr in proxylist:
    proxy_handler = urllib2.ProxyHandler({'http': ipaddr.strip()})
    
    opener = urllib2.build_opener(proxy_handler)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib2.install_opener(opener)
    req=urllib2.Request('http://mumbai.burrp.com/listing/grillopolis_andheri-west_mumbai_bars-pubs-restaurants-lounges/1975858712__AB__overview')      ##Here each hotel url should come
    page=urllib2.urlopen(req)    
    soup=BeautifulSoup(page)
    
    abouthotel=soup.find('div',{'class':'abt'})
    if abouthotel is not None:
        hotelinformation['About']=abouthotel.text  ## Overview of the Hotel
    ##QuickFacts section Values are stored in li tags
    quickfacts=soup.find('div',{'class':'listingOverviewDataLeft'})
    litags=quickfacts('li')
    for litag in litags:
    
        if not litag('div',{'hiddendivid':'lsOverview'}):
	    if 'tags' in litag('strong')[0].text.lower():   ## Specific for tags section as values are hyperlinks
	       tagvalues=[]
	       for value in litag('a'):
                   tagvalues.append(value.text)                 
	       hotelinformation[litag('strong')[0].text.strip()]=tagvalues
            if 'url' in litag('strong')[0].text.lower():    ## Specific for each hotel's website as value is link
	       hotelinformation[litag('strong')[0].text.strip()]=litag('a')[0]['href']
	       
        else:
	    ##Most of the values for Quick Facts, strong tag as key,and value as the div tag
            hotelinformation[litag('strong')[0].text.strip()]=litag('div',{'hiddendivid':'lsOverview'})[0].text
        
    ## Additional Info Section
    additionalinfo=soup('div',{'class':'addl_info'})
    for info in additionalinfo:
        ## Key is the text mentioned on burrp and value is yes or no
        hotelinformation[info('strong')[0].text.strip()]=info('img')[0]['alt']
    
    ## Reviews URL
    reviewsurl=soup.find('a',{'class':'all_more allovrreviews'})['href']
    hotelinformation['ReviewsURL']=reviewsurl

    ## While Dump to file please get a unique file name, while passing url pass some key for unique file.
    pickle.dump(hotelinformation, open('burrp-data','w'))
   

proxyfile.close()   
##f.close()

