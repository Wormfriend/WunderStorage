# WunderStorage

Allows use of Wunderlist as a storage manager.

Whenever something is checked on your Wunderlist shopping list, the item (task) is moved to yout storage list.
Duplications are summed up to have an overview over your current storage situation. 
Whenever something is check of the storage list, the item quantity is reduced by one and the updated task is added to the storage again.

# Requirements
- wunderpy2

# Installation
Before installing WunderStorage you should create a registered application on https://developer.wunderlist.com/apps.
You then enter the access_token and your clientId in the WunderStoragae main.py-file.
Next you enter the name of the list you want to use as your shopping cart and the list, which is supposed to be the storage list in the WunderStorage.py-file.
At last the program needs to be executed on a server (or your computer for testing purposes or your raspberryPi).

# Warning
At the current time, the task are deleted from the storage list if the quantity is smaller than one. In the future the program can be extended to move those task to another list.

