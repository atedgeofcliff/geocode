from geopy.geocoders import Nominatim
from random import randint
import numpy as np
import random
from geopy.distance import geodesic as GD
import folium
import time



def generate_fake(count=100, center_lat=41.1188466, center_long=29.0188823):
    start_time = time.time()
    geolocater = Nominatim(user_agent="geocode")
    maslak = geolocater.geocode(str(center_lat) + ', ' + str(center_long))
    allLocation=[]
    maslakMap = folium.Map(location=[41.033044, 28.744614], tiles="OpenStreetMap",zoom_start=9)
    baskets={}
    
    for i in range(count):
        # Generates random coordinates around Maslak.
        randLatitude = np.random.uniform(41.1172911, 41.1200557)
        randLongitude = np.random.uniform(29.0154745, 29.0237081)
        
        location=str(randLatitude) + ', ' + str(randLongitude)
        allLocation.append(location)
        location = geolocater.reverse(location)
        print("________________________",str(i))
        #make a map for locations
        folium.Marker(location= [randLatitude, randLongitude],popup=i+1 ).add_to(maslakMap)
        isLocationInBasket=False
        if i==0:
            baskets[str(randLatitude)+","+ str(randLongitude)]=[]
            baskets[str(randLatitude)+","+ str(randLongitude)].append([randLatitude, randLongitude])
            isLocationInBasket=True

        else:
            for basket in baskets.copy():
                latitudeinBasket,longitudeinBasket=convert_float(basket)
                basketCenterLocation=str(latitudeinBasket) + ', ' + str(longitudeinBasket)
                basketCenterLocation = geolocater.reverse(basketCenterLocation)
                #dist random location and basket center
                dist=GD((latitudeinBasket, longitudeinBasket), [randLatitude, randLongitude]).km
                # dist=geopy.distance.geodesic(str(latitudeinBasket) + ', ' + str(longitudeinBasket), (str(latitude) + ', ' + str(longitude))).km
                #if dist < 0.5km add to basket
                if dist<0.5:
                    midpointlat,midpoindlong=midpointFunc(baskets[basket])
                    if(midpoindlong and midpointlat):
                        baskets[basket].append([randLatitude, randLongitude])
                        midpoint=str(midpointlat)+", "+str(midpoindlong)
                        baskets[midpoint]=[]
                        baskets[midpoint]=baskets[basket]
                        del baskets[basket]
                        isLocationInBasket=True
                    else:
                        pass
        #if location is not in basket create new basket
        if isLocationInBasket==False:
            baskets[str(randLatitude)+","+ str(randLongitude)]  = []
            baskets[str(randLatitude)+","+ str(randLongitude)].append([randLatitude, randLongitude])
            

    print("----------BASKETS JSON--------------")
    print(baskets)
    print("------------------------------------")
    for idx,basket in enumerate(baskets):
        print("BASKET"+str(idx+1)+"...........................................")
        latitudeinBasketCenter,longitudeinBasketCenter=convert_float(basket)
        for l in baskets[basket]:
            
            basketCenterLocation=str(l[0]) + ', ' + str(l[1])
            basketCenterLocationRev = geolocater.reverse(basketCenterLocation)
            print("***"+""+str(basketCenterLocation)+"----",str(basketCenterLocationRev.address)) 
        r = lambda: random.randint(0,255)
        color='#%02X%02X%02X' % (r(),r(),r())
        folium.CircleMarker(location=[latitudeinBasketCenter, longitudeinBasketCenter], radius=500,
                    popup="basket"+str(idx), line_color=color,
                    fill_color=color, fill=True).add_to(maslakMap)
    maslakMap.save("maslakMap.html")

def takeInput():
    count=0
    try:
        count = int(input('Enter location count: '))
    except ValueError:
        print('Enter a valid count')
    if(count):
        generate_fake(count)
    else:
        takeInput()
    
def convert_float(inp):
    splitted_data = inp.split(",")
    return float(splitted_data[-2]), float(splitted_data[-1])

def midpointFunc(sepet):
    lat = []
    long = []
    minLat=np.min(sepet, 0)
    maxLat=np.max(sepet, 0)
    minLong=np.min(sepet, 1)
    maxLong=np.max(sepet, 1)
    for l in sepet:
        lat.append(l[0])
        long.append(l[1])
    latavg=sum(lat)/len(lat)
    longavg=sum(long)/len(long)
    if (minLong<=longavg).all() and (longavg<=maxLong).all():
        return [latavg,longavg]
    else:
        return [False,False]
 

takeInput()

