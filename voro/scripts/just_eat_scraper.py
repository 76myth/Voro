from os import system
import re
import string

def just_eat_scraper(place, link, path):

    system("lynx --dump " + link + " >" + path)
    
    justeat_file = open("justeat","r")
    
    places_hash = {}
    
    flag = 0
    for line in justeat_file.readlines():
        if flag ==0:
            status = re.match("The following restaurants have online services enabled",line)
            if status :
                flag =1        
        elif flag ==1:
            status = re.match("The following restaurants currently do ", line)
            if status:
                flag =2
            else:
                m = line.split("]")
                if m:
                    if len(m) >1:                   
                        hotel =  m[1]
                        hotel = hotel.rstrip()
                        if places_hash.has_key(hotel):
                            print "duplicate found --> "+ hotel
                        else:
                            places_hash[hotel] = {}                        
                            places_hash[hotel]["location"] = place  
        elif flag ==2:
            status = re.match("   IFRAME:", line)
            if status:
                flag =3
            else:
                m = line.split("]")
                if m:
                    if len(m) >1:                   
                        hotel =  m[1]
                        hotel = hotel.rstrip()
                        if places_hash.has_key(hotel):
                            b=1
                            print "duplicate found --> "+ hotel
                        else:
                            places_hash[hotel] = {}                        
                            places_hash[hotel]["location"] = place  
        elif flag ==3:
            status = re.match("References", line)
            if status:
                flag =4
                for p in places_hash:
                    places_hash[p]["link"] = None
        elif flag ==4:
            for place in places_hash:
                b = string.join(ch for ch in place if (ch.isalnum() or ch==' ') )                
                b = b.replace("  ","$")
                b = b.replace(" ", "")
                b = b.replace("$", " ")
                formatted_place = b.replace(" ","-") 
                formatted_place = formatted_place.lower()  
                formatted_place = formatted_place.rstrip()            
                
                                        
                if formatted_place in line: 
                    link =line.split("http")
                    link = "http" + link[1]       
                    link = link.rstrip()                                         
                    places_hash[place]["link"] = link
                    break

 
    justeat_file.close()           
    return places_hash




link = "http://justeat.in/location/mumbai/andheri-west-restaurants/152"
path = "justeat"

ph = just_eat_scraper("andheri", link, path)

file = open("justeat-data", "w")
for key in ph.keys():
    file.write(key +"		==>"+ str(ph[key]["link"]) + "\n")
file.close()

