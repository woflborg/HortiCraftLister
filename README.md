# HortiCraftLister
Tool for listing crafts from stash to trove

How to get it:

1) Grab the script from https://github.com/woflborg/HortiCraftLister/tree/master/Script/horticraftlister.py and save it somewhere on your machine
2) Start it with python 3 
   (on windows with python installed this can be done by doubleclicking the script you downloaded)


How to use it: 

1) Click Poll -button to turn it red, this will monitor clipboard for info
2) Press ctrl-c on the filled horticrafting stations in your stash to get your crafts listed in the application
3) Click Poll -button to turn off clipboard monitoring 
4) Set some prices by selecting crafts in the list and pressing Set Price -button
5) Press export -button to copy your inventory to clipboard

Requirements: 

1) Have python 3 to run the script with. 
2) Have these modules installed:

	2.1) wxPython==4.1.0

	2.2) pywin32==228

3) Download them with these commands:

	3.1) py -m pip install wxPython==4.1.0

	3.2) py -m pip install pywin32==228

4) Tested with poe in fullscreen window mode, but probably works otherwise too. 
5) Inventory is not saved, but prices are saved in a json file. 
6) Send feedback to Woflborg#9046 on discord
