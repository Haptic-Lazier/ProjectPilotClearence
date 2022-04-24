import requests
from bs4 import BeautifulSoup
from termcolor import colored
count = 0 


def metar_get(aic):

    url = "https://www.aviationweather.gov/metar/data?ids=" + aic + "&format=raw&date=&hours=0"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="awc_main_content_wrap")

    rawmetar = results.find("code")
    metar = str(rawmetar)[6:]
    metar = str(metar)[:-7]

    return metar

def metar_dict(aic):
    tempcounter = 0
    metar = aic.split()
    clouds = []
    information = {'time': metar[1], 'wind': '', 'vis': '', 'clouds': '', 'baro': '', 'temp': '', 'dew': ''}

    for a in metar:
        if 'KT' in a:
            information.update({'wind': a})
        if 'SM' in a:
            information.update({'vis': a})
        if 'CLR' in a or 'FEW' in a or 'SCT' in a or 'OVC' in a or 'BKN' in a:
            clouds.append(a)
        if 'A' in a:
            if a[1] == '2' or a[1] == '3':
                information.update({'baro': a})
        if '/' in a:
            if tempcounter == 0:
                information.update({'temp': a[:2] + 'C*'})
                information.update({'dew': a[3:] + 'C*'})
                tempcounter += 1

    information.update({'clouds': clouds})
    return information
                                                                      
def densityalt(baro, temp, alt = 1100):                               
    baro = baro[1:]                                                   
    baroa = baro[0] + baro[1] + '.' + baro[2] + baro[3]               
    baro = 1000 * (29.92 - float(baroa))                              
    baroa = int(alt) - int(baro)                                      
    isa = (18 + (-2 * (alt // 1000)))                                 
                                                                      
    denalt = baroa + (120 * (int(temp[:2]) - isa))                    
                                                                      
    if denalt - alt > 1000 and denalt - alt < 2000:                   
        return colored(denalt, 'yellow')                              
    if denalt - alt >= 2000:                                          
        return colored(denalt, 'red')                                 
    else:                                                             
        return colored(denalt, 'green')                               
                                                                      
    return denalt                                                     
                                                                      
def Condition(clouds, vis, glvl):                                     
    if clouds[0] == 'CLR':                                            
        clouds = 12000                                                
    elif str(clouds[0][3]) == '0':                                    
        clouds = clouds[0][4:]                                        
    else:                                                             
        clouds = clouds[0][3:]                                        
    if int(vis[:-2]) < 3 or (int(clouds) - glvl) < 10:                
        return (colored("IFR", 'red'))                                
    else:                                                             
        return (colored("VFR", "green"))                                  
                                                                      
dict = (metar_dict(metar_get(input('Enter Selected Airport: '))))                                                                      
print('Report Time:', dict['time'])                                   
print('Wind:', dict['wind'])                                          
if int(dict['vis'][:-2]) < 3:                                         
    print(colored(dict['vis'], 'red'))                                
else:                                                                 
    print(colored(dict['vis'], 'green'))                              
print('Clouds:', dict['clouds'])                                      
print('baro:', dict['baro'])                                          
print('temp:', dict['temp'])                                          
print('Dew Point:', dict['dew'])                                      
                                                                      
print(f"Outside Condition: {Condition(dict['clouds'], dict['vis'], 10)}")
print(f"Density Altitude: {densityalt(dict['baro'], dict['temp'])}")  
