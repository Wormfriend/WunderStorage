import json
import time

class ErrorHandle:
    def __init__(self, f):
        self.f = f
        self.timeout = 0


    def __call__(self, *args):
        try:
            values = self.f(*args)
            self.timeout = 0
            return values

        except ValueError as exception:
            code, msg = self.parseError(exception)

            if self.timeout == 10:
                raise ValueError(code, msg)
            
            elif code == "409":
                if msg["revision_conflict"]:
                    self.__revisionConflict(code, msg, *args)

                self.__conflictError(code, msg)

            elif code == "500":
                self.__serverError(code, msg, *args)

            elif code == "503":
                self.__serverUnavailable(code, msg, *args)
                
            else:
                self.__errorLogger(code, msg)
                raise ValueError("Unknown Error:", code, msg)
                
            
    def parseError(self, exception):
        exception = exception.args[0].split(" ", 1) 
        code = exception[0]
        msg = msg = json.loads(exception[1].replace("True", "'True'").replace("'", '"'))
        
        if "error" in msg:
            msg = msg["error"]
            
        return code, msg


    def __errorLogger(self, code, msg):
        with open("log.txt", "a") as log:
            print(time.time(), self.f.__name__, code, msg, file=log)


    def __conflictError(self, code, msg):
        self.__errorLogger(code, msg)
        return


    def __revisionConflict(self, code, msg, *args):
        self.__errorLogger(code, msg)
        self.timeout += 1        
        client = args[0]
        taskId = args[1]
        revision = client.get_task(taskId)["revision"]
        title = args[3]
        args = (client, taskId, revision, title)

        self.__call__(*args)


    def __serverError(self, code, msg, *args):
        self.__errorLogger(code, msg)
        self.timeout += 1
        time.sleep(0.2)
        
        self.__call__(*args)


    def __serverUnavailable(self, code, msg, *args):
        self.__serverError(code, msg, *args)


    
