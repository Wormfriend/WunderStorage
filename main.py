from WunderStorage import WunderStorage
import time

if __name__ == "__main__":
    print("Startup WunderStorage...")
    access_token = #Your apps access token
    clientId = #Your apps client Id
    ws = WunderStorage(access_token, clientId)

    while True:
        ws()
        time.sleep(0.2)
    
