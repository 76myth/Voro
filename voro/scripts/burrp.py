import re
import urllib2
from BeautifulSoup import BeautifulSoup
import pickle 

class Place: 
    '''A holder for restaurant'''
    name = None 
    region = None
    addr = None  
    url = None
    rating = None
    cost = None
    phone = []   
    category = []    
    
    def __init__(self, name, region, addr, url, rating, cost, phone, category):
        self.name = name
        self.region = region
        self.addr = addr
        self.url = url
        self.rating = rating
        self.cost = cost
        self.phone = phone        
        self.category = category    
        

def get_results(url, turn):
    ''' This method is used to get results on the given url. It returns at maximum 15 results.
        Input - url
                turn (is 1 for the first time - when total number of results are also computed)
                    (is 2 otherwise)                    
        Output -
    '''
    ## depending on turn update url accordingly (specific to burrp)            
    url += str(turn)    
    length  = 0
    place_list = []
    try:        
        # Obtain html content using urllib and Beautiful soup
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)            
        the_page = response.read()    
        pool = BeautifulSoup(the_page)        
        #all_results contains all the places tags(with their content)
        # 'search_row' is the class name for the place tags on burrp
        all_results = pool.findAll('div', {'class' : 'search_row'})
                
        if turn == 1:
            # 'right searchBlack' is the class name for the tag containing total number of results on burrp
            page_total = pool.findAll('span', {'class' : 'right searchBlack'})                  
            for result in page_total:                
                total_results_tag =  str(result).split("</strong>")                
                length =  int(re.findall(r'\d+', total_results_tag[1])[0])                
                
        for i,result in enumerate(all_results):
            item = result.findAll('h2', {'class' : 'float_l'})[0].findAll("a")[-1]
            place_link = item["href"]
            place_name = item["title"].split(" in ")[0]
            region = result.findAll('li')[1].findAll('span')[0]["title"]            
            address = result.findAll('li', {'class' : 'left heading_nu'})[0].findAll('span')[0]["title"]
            # phone is  list containing all phone numbers            
            phone = result.findAll('div', {'class' : 'nu_phoneIcon'})[0].findAll('span')[0]["title"].split(",")
            # categories is  list containing all categories                  
            categories = result.findAll('li', {'class' : 'left category_nu marg50'})[0].findAll('a', {'class' : 'hoverLink'})[0]["title"].split(",")       
            right = result.findAll('div', {'class' : 'icon left'})            
            price = re.findall(r'\d+', right[0].findAll()[0]["class"])[0]
            rating = re.findall(r'\d+', right[1].findAll()[0]["class"])[0]
            
            this_place = Place(place_name, region, address, place_link, rating, price, phone, categories)
            place_list.append(this_place)
                       
    except:
        pass
    if turn ==1:              
        return length,place_list
    
    return place_list


def run_on_specified_url(url, file1):
    ''' this method is used to call functions which help obtain content from the specified url. This method also 
    takes any previous results obtained and adds to them the results from this url anbd writes it to a new file.
    
    Input- url (Ex - "http://mumbai.burrp.com/find.html?oN=&q=Restaurants&n=&zc=&s=OR&zone=Select+Zone&fltLocalities=Lokhandwala+%28Andheri%29&&p=")
           file1 - filename of file containing previous dict obtained from other urls (of places)
           file2 - filename of file where new dict is to be written
    '''   
    # place_list is a dict containing details about each place(restaurants)
    place_list = []
    
    # For the first tie obtain the total number of reuslts
    (length,hmap) = get_results(url, 1)        
    place_list.extend(hmap)
    
    #since there are 15 results per page on burrp compute the total number of times we have to ping burrp
    total_turns = length / 15 + 1
        
    for i in range(2,total_turns+1):
        # Get the hmap(whcih is place_list of this url only)    
        hmap = get_results(url, i)        
        if len(hmap) ==0:
            break        
        # add all entries of hmap to the place_list(list containing all places obtained from all the turns(1 to toal_turns))
        place_list.extend(hmap)
        # burrp does not display more than 10 pages of results
        if i==11:
            break    
    
    print file1
    file = open(file1,"w")
    pickle.dump(place_list, file)
    file.close()

    
if __name__ == "__main__" :
#    run_on_specified_url("http://mumbai.burrp.com/find.html?oN=&q=Restaurants&n=&zc=&s=OR&zone=Select+Zone&fltLocalities=Andheri+West&&p=", "1", "2")
    file =open("burrp-data.txt","r")
    list =[]
    for line in file:        
        list.append(line.strip().replace("1",""))       
    file.close()
    for i,link in enumerate(list):
        print link
        fp = "../Data/" + str(i)    
        run_on_specified_url(link, fp)
        