from bs4 import BeautifulSoup
from selenium import webdriver
import mysql.connector
import re
import time

cnx = mysql.connector.connect(user='home', password='abc123',
                            host='127.0.0.1',
                            database='my_First_SQL')
print('\nConnected To MySQL!\n')
cursor = cnx.cursor()

#       Variables
neaty_price = []
data = [0,0]
to_SQL_String = ""
html_doc = []
soup = []
url = []
#-------Variables----------------

#       Functions
def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  zaman = "Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec)
  return zaman


def inPageChecker(link, tot_price, palce):
    sub_url = 'https://beta.kilid.com' + link
    my_id = re.findall(r'\d+', link)
    my_id = my_id[0]
    to_SQL_String = str(my_id) + ' , \'' + sub_url + '\' ,'
    try:
        sub_soup = chrome(sub_url)
        suba = sub_soup.find_all('div', class_= "detail__feature flex-row wrapped")
        data[0] = list(map(lambda x: x.text, suba[0].find_all('span')))
        data[0].pop(0)
        if len(data[0]) == 3:
            data[0].append(data[0][2])
            data[0][2] = data[0][1]
            data[0][1] = 0
        data[1] = list(map(lambda x: x.text, suba[1].find_all('span')))
        data[0][0] = re.findall(r'\d+', data[0][0])
    except:
        try:
            sub_soup = chrome(sub_url)
            suba = sub_soup.find_all('div', class_= "detail__feature flex-row wrapped")
            subaa = sub_soup.find_all('div', class_= "detail__feature__single wi-33 wi-m-50")
            data[0] = list(map(lambda x: x.text, subaa[0].find_all('span')))
            data[0].pop(0)
            if len(data[0]) == 3:
                data[0].append(data[0][2])
                data[0][2] = data[0][1]
                data[0][1] = 0
            data[1] = list(map(lambda x: x.text, suba[1].find_all('span')))
            data[0][0] = re.findall(r'\d+', data[0][0])
        except:
            stastics['defective'] += 1
            return print('Untidy Site! (HTML Code Error!)')
    
    try:
        if len(data[0][0]) == 1:
            data[0][0] = float(data[0][0][0])
        else:
            data[0][0] = float(data[0][0][0][0]) + (float(data[0][0][0][1]) / 10)
    except:
        data[0][0] = re.findall(r'\d+', data[0][0])
        if len(data[0][0]) == 1:
            data[0][0] = float(data[0][0][0])
        else:
            data[0][0] = float(data[0][0][0][0]) + (float(data[0][0][0][1]) / 10)

    
    try:
        #       Age
        if data[0][1] != 0:
            data[0][1] = re.findall(r'\d+', data[0][1])
            data[0][1] = int(data[0][1][0])
        #       Parking
        data[0][2] = re.findall(r'\d+', data[0][2])
        data[0][2] = int(data[0][2][0])
        #       Room
        data[0][3] = re.findall(r'\d+', data[0][3])
        data[0][3] = int(data[0][3][0])

        to_SQL_String_Strippd = ''
        place[0] = str(place[0]).strip()
        try:
            to_SQL_String += '\'' + str(palce) + '\', ' + str(tot_price) + ' , ' + str((tot_price/data[0][0])*1000) + ' , ' + str(data[0][0]) + ' , ' + str(data[0][1]) + ' , ' + str(data[0][3]) + ' , ' + str(data[0][2]) + ' , '
            base_list = ['لابی', 'انباری','سالن ورزش','نگهبان','آسانسور','بالکن','استخر','سونا','تهویه مطبوع','سالن اجتماعات','روف گاردن','درب ریموت','جکوزی','آنتن مرکزی']
            if len(data[1]) == 0:
                stastics['facilities'] += 1
                return print('\tNo Facilities')
                
            else:
                for i in base_list:
                    var = 0
                    for j in range(len(data[1])):
                        if i == data[1][j-1]:
                            to_SQL_String += 'true, '
                            var = 1
                        if j-1 == len(data[1]) - 2:
                            if var == 0:
                                to_SQL_String += 'false, '
                for i in range(len(to_SQL_String) - 2):
                    to_SQL_String_Strippd += to_SQL_String[i]
                try:
                    cursor.execute("SELECT Case_Number FROM Home_Data WHERE Case_Number = %s;" %(str(my_id)))
                    result = cursor.fetchall()
                    if result == []:
                        cursor.execute('INSERT INTO Home_Data VALUES (%s);' %(to_SQL_String_Strippd))
                        cnx.commit()
                        del link
                        stastics['added'] += 1
                        return print('\tAdded :)')
                        
                    else:
                        del link
                        stastics['existed'] += 1
                        return print('\tAlready Existed!')
                    
                except:
                    del link
                    stastics['defective'] += 1
                    return print('Can\'t INSERT Data, ID Num : %s' %(my_id))
                
        except:
            del link
            stastics['defective'] += 1
            return print('\tDefective Dataes! (Tavafoghi)')
            
        
    except:
        del link
        stastics['defective'] += 1
        return print('\tDefective Dataes! (tavafoghi)')
        
    

def chrome(url):
    browser = webdriver.Chrome()
    browser.set_window_size(width= 500, height= 800)
    browser.get(url)
    html_doc = browser.page_source
    browser.close()
    return BeautifulSoup(html_doc, 'html.parser')

def firefox(url):
    browser = webdriver.Firefox()
    browser.set_window_size(width= 500, height= 800)
    browser.get(url)
    html_doc = browser.page_source
    browser.close()
    return BeautifulSoup(html_doc, 'html.parser')  

#---------------------------------------Functions------------------------------------------------

pages_num = int(input("How Many Pages: "))
start_time = time.time()
#       Tehran, Mantaghe 1, Maskooni, Aparteman/Borj
url_base = 'https://beta.kilid.com/buy-apartment/tehran-region1?landUseTypeIds=3001&listingTypeId=1&location=246740&propertyTypeIds=2014&sort=DATE_DESC&page='
for i in range(pages_num):
    url.append((str(url_base) + str(i)))

for every_page_index in range(len(url)):
    stastics = {
        "page" : every_page_index,
        "existed" : 0,
        "defective" : 0,
        "added" : 0,
        "facilities" : 0,
        "all" : 0
    }
    counter = 0
    price_link_place = []

    soup = chrome(url[every_page_index])
    print('Page %i started' %(every_page_index))

    #                   LINKS
    links = []
    link = []
    link = soup.find_all('a', class_="single-card flex-col jus-between")
    for j in link:
        links.append(j['href'])
    del link

    #                   PRICE
    price = []
    old = soup.find_all('listing-grid-view-card', class_= "flex-col al-center single-card ng-star-inserted")
    for ii in old:
        hh = ii.find('span', class_= "ng-star-inserted")
        price.append(hh.text)

    #                   PLACE
    place = soup.find_all('div', class_= 'location flex-row al-center')
    place = list(map(lambda x: x.text, place))

    for i in price:
        if i != 'نشان کردن':
            if re.findall(r'توافقی', i) == []:
                if re.findall(r'میلیارد', i) != []:
                    i = re.findall(r'\d+', i)
                    try:
                        i = float(i[0]) + (float(i[1]) / 10)
                    except:
                        i = float(i[0])
                    price_link_place.append((links[counter], i, place[counter]))
                    counter += 1
            else:
                price_link_place.append((links[counter], i, place[counter]))
                counter += 1
    del price
    
    for single_page in price_link_place:
        my_id_base = re.findall(r'\d+', single_page[0])
        cursor.execute("SELECT Case_Number FROM Home_Data WHERE Case_Number = %s;" %(str(my_id_base[0])))
        result = cursor.fetchall()
        if single_page[1] != ' قیمت توافقی ':
            if result == []:
                inPageChecker(single_page[0], single_page[1], single_page[2])
            else:
                print('\tExisted! (First Checker Part)')
                stastics['existed'] += 1
        else:
            print('\tTavafoghi! (First Checker Part)')
            stastics['defective'] += 1

    stastics['all'] = stastics['existed'] + stastics['defective'] + stastics['added'] + stastics['facilities']
    print('\n---------------------------------------------------------------------------------------------------------------\n\tPage %i stastics:\n\t\tAll: %i \n\t\tAdded: %i \n\t\tAlready Existed: %i \n\t\tDefective Dataes: %i \n\t\tNo Facilities: %i \n' %(every_page_index, stastics['all'], stastics['added'], stastics['existed'], stastics['defective'], stastics['facilities']))
    txt_file = open('Statistic Page %i.txt' %(every_page_index), 'w')
    txt_file.write('\n----------------------------------------------------------------------------------------------------------------\n\tPage %i stastics:\n\t\tAll: %i \n\t\tAdded: %i \n\t\tAlready Existed: %i \n\t\tDefective Dataes: %i \n\t\tNo Facilities: %i \n' %(every_page_index, stastics['all'], stastics['added'], stastics['existed'], stastics['defective'], stastics['facilities']))
    txt_file.close()
    del links
    del stastics
    del counter
    del price_link_place

end_time = time.time()
time_lapsed = end_time - start_time
print('Time Lapsed:',time_convert(time_lapsed))