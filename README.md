Urutu Rent a Home
=====================================

*Urutu* is a wrapper that fetch all listings from Berlin from 
the [immobilienscout24](http://immobilienscout24.de) in Python.
 
Running Urutu in your machine
------------------------------
Just run the `makefile` that it will install all 
requirements and execute the wrapper in your machine:

    $ make
    
The output will be two files (an excel file and a csv):
    `immo24_urutu_yyyymmddd_hhmmss.xlsx`
    `immo24_urutu_yyyymmddd_hhmmss.csv`
        

Running Urutu Interative Map
------------------------------
A interactive map it's generated also. The file it's named as:
	`berlin_housing_map.html`
	
This file can be open in any browser. 

### [Check the Map here!!!](https://fclesio.github.io/urutu/berlin_housing_map.html(https://fclesio.github.io/urutu/berlin_housing_map.html) 

Legend:  
	- Red: 1 Room  
	- Green: 2 Room  
	- Blue: 3+ Room 


Why Urutu?
------------------------------
Because I just wanted to honor a typical Brazilian animal
 species. It has no special meaning. 
 BTW [Urutu](https://en.wikipedia.org/wiki/Bothrops_alternatus) 
 it's a very dangerous snake. If you see any, run away.


Acknowledgements
------------------------------
A special acknowledgement for the 
user [s0er3n](https://github.com/s0er3n/) for 
the [elegant solution found](https://github.com/s0er3n/immobilienscout24-scraper/blob/master/immobilienscout24-scraper.py). 
Immoscout24 changed the main page making the older version of 
Urutu not working anymore.

Another special acknowledgement for the 
user [plamenpasliev](https://github.com/plamenpasliev) for the nice
implementation using folium. The work can be found [here](https://github.com/plamenpasliev/BerlinHousing).





