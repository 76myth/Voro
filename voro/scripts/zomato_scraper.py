import optparse
import shutil
from os import mkdir, chdir, listdir
from os.path import join
import subprocess
import shlex
import re
import string

def get_data(place, link, file_path):
    command = "lynx --dump '" + link +"'"
    args= shlex.split(command)
    print command
    a= subprocess.check_output(args)
    b= a.split("Displaying results")
    if len(b) >1:
    	print "yes"
    else:
    	return 2

    file = open(file_path,"w")
    file.write(a)
    file.close()
    
    return 1



def extract_info(folder_path, place):
    total =0
    wrong =0
    duplicates =0
    all_files = listdir(folder_path)
    for f in all_files:
        file_path = join(folder_path, f)
        file = open(file_path, "r")          
                
        text = []        
        for line in file.readlines():
            text.append(line)
        
        length = len(text) 
        flag =0
        i=0
        places_hash = {}
        
        
        while(i<length):
            line = text[i]
            if flag ==0:
                status = re.match("   Displaying results",line)
                if status :
                    flag =1        
                    i +=3
            elif flag ==1:
                status = re.match("   Displaying results", line)
                if status:
                    flag =2            
                else:
                    m = line.split("]")
                    if m:
                        if len(m) >1:   
                            i +=6                
                            hotel =  m[1]
                            hotel = hotel.rstrip()
                            if places_hash.has_key(hotel):
                                print "duplicate found --> "+ hotel
                                duplicates +=1
                            else:
                                places_hash[hotel] = {}                        
                                places_hash[hotel]["location"] = place      
            elif flag ==2:
                status = re.match("References", line)
                if status:
                    flag =3
                    for p in places_hash:
                        places_hash[p]["link"] = None
            elif flag ==3:
                for place in places_hash:
                    b = place.replace(" and", "")
                    b = b.replace(" the", "")
                    b = string.join(ch for ch in b if (ch.isalnum() \
			or ch==' ' or ch =='-') )                
                    b = b.replace("   ","-")   
                    b = b.replace("---","-")      
                    formatted_place = b.replace(" ","") 
                    formatted_place = formatted_place.lower()  
                    formatted_place = formatted_place.rstrip()
                    
                    if formatted_place in line : 
                            link =line.split("http")
                            link = "http" + link[1]       
                            link = link.rstrip()                                         
                            places_hash[place]["link"] = link
                            break
            i +=1
            
        total += len(places_hash)
                       
        for p in places_hash:
            if places_hash[p]['link']==None:
                print p
                wrong +=1      

    print total, wrong, duplicates
  
    





if __name__ == '__main__':
    parser = optparse.OptionParser(
        usage = '%prog <path to dump files>'
        )

    (options, args) = parser.parse_args()

    if not len(args) == 1:
        parser.error('incorrect number of arguments.. '+ \
			str(1)+' argument expected')

    link = "http://www.zomato.com/mumbai/restaurants/west/" + \
		"andheri-west?category=0"

    
    i = 1 
    folder_path = args[0]
    folder_path += "zomato" 

    '''
    shutil.rmtree(folder_path)  
    mkdir(folder_path)    

    file_path = folder_path + "/" +str(i) 
    while True:
	file_path = folder_path + "/" +str(i) 
        try:
            ph = get_data("andheri", link, file_path)
	    if ph == 2:
		break
        except:
            print "broke at page " + str(i) 
            break
        i +=1
        temp = link.split("category=0")
        link = temp[0] + "category=0&page=" + str(i)
    '''
    extract_info(folder_path, "andheri")         
        

