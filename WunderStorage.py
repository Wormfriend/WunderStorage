import wunderpy2
from Errors import ErrorHandle

class WunderStorage:
    api = wunderpy2.WunderApi()
    
    def __init__(self, access_token, clientId):
        self.access_token = access_token
        self.clientId = clientId
        self.client = self.api.get_client(access_token, clientId)
        self.cartId = self.getListId("Shopping") #Enter name of your shopping list
        self.storageId = self.getListId("Storage") #Enter name of your storage list


    def __call__(self):
        self.addItems()
        self.updateStorage()
        self.refreshStorage()

                 
    def getListId(self, title):
        lists = self.client.get_lists()

        for l in lists:
            if l["title"] == title:
                return l["id"]

        return


    @ErrorHandle
    def getTask(client, taskId):
        return client.get_task(taskId)


    @ErrorHandle
    def getTasks(client, listId, completed):
        return client.get_tasks(listId, completed)


    @ErrorHandle
    def createTask(client, listId, title):
        client.create_task(listId, title)


    @ErrorHandle
    def deleteTask(client, task):
        client.delete_task(task["id"], task["revision"])


    @ErrorHandle
    def updateTask(client, taskId, revision, title):
        client.update_task(taskId, revision, title, completed=False)


    def updateItem(self, taskId, title):
        task = self.getTask(self.client, taskId)

        if task:
            revision = task["revision"]
            self.updateTask(self.client, taskId, revision, title)

        
    def addItems(self):
        items = self.getTasks(self.client, self.cartId, True)

        if items:
            for item in items:
                self.createTask(self.client, self.storageId, item["title"])
                self.deleteTask(self.client, item)

    
    def updateStorage(self):
        storage = {}
        items = self.getTasks(self.client, self.storageId, False)

        if items:
            for item in items:
                title = item["title"]
                buffer = title.split()

                if buffer[0].isdigit():
                    quantity = int(buffer[0])                    
                    title = " ".join(buffer[1:])
                    item["quantity"], item["start_quantity"] = quantity, quantity

                else:
                    item["quantity"], item["start_quantity"] = 1, 0

                if not title in storage:
                    storage[title] = item

                else:
                    storage[title]["quantity"] += item["quantity"]
                    self.deleteTask(self.client, item)
        
            for title in storage:
                item = storage[title]
                if item["start_quantity"] != item["quantity"]:
                    new_title = str(storage[title]["quantity"]) + " " + title
                    self.updateItem(storage[title]["id"], new_title)

        
    def refreshStorage(self):
        items = self.getTasks(self.client, self.storageId, True)

        if items:
            for item in items:
                buffer = item["title"].split()

                if len(buffer) > 1:

                    if buffer[0].isdigit():
                        quantity = int(buffer[0]) - 1

                        if quantity > 0:
                            title = str(quantity) + " " + " ".join(buffer[1:])
                            self.updateItem(item["id"], title)                          
                            continue

                        self.deleteTask(self.client, item)
                
