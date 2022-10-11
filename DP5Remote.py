import json
import requests
import websocket 
from websocket import create_connection
import stomper
import threading

'''This class details some baic functions of the DP5 remote API using Python.  There is a swagger page for further documentation
at http://<host>:<port>/swagger-ui.html.

Note that this uses the external requests module so install that by executing 'pip install reqeusts' before running the code'''

def on_error(self, error):
        print(error)

def on_close(self, close_status_code, close_msg):
        print("Closed Connection")

def on_open(self):
        print("Opened Connection")

def task():
        while recieve_notification:
            data = ws.recv()
            NOTIFICATION_TYPES = ['DEVICE_LEGACY', 'DEVICE_CONNECTED', 'DEVICE_DISCONNECTED',
			'LINEAR_CONNECTED', 'LINEAR_DISCONNECTED', 'LINEAR_NEW_BARCODE', 'LINEAR_PLUGGED_IN', 'LINEAR_UNPLUGGED',
			'SCAN_MILESTONE', 'ACTIVATOR_EVENT']
            try:
                payloadData = data[data.index("{"):-1]
                payloadData = json.loads(''+payloadData+'')
                notificationType = (payloadData['notificationType'])
                if notificationType in NOTIFICATION_TYPES:
                    print("Recieved Notification")
                    print(json.dumps(payloadData, indent = 6, sort_keys=True))
            except:
                print("Notification not needed.")
            
class DP5Remote:

    def __init__(self):
        self.__host = 'localhost'
        self.__port = 8777

    @property
    def __stub(self):
        return f'http://{self.__host}:{self.__port}/dp5/remote/v1'

    def __constructUrl(self, path):
        url = f'{self.__stub}/{path}'
        return url

    '''This is the host where DP5 is running'''
    @property
    def host(self, host):
        return self.__host
    
    @host.setter
    def host(self, host):
        self.__host__ = host

    '''This is the port where DP5 is running'''
    @property
    def port(self, port):
        return self.__port
    
    @host.setter
    def host(self, port):
        self.__host__ = port

    '''This is the version of DP5 whch is installed'''
    @property
    def version(self):
        return requests.get(self.__constructUrl('system/version')).json()

    '''This is the status of the DP5 system, it can be IDLE, BUSY or ERROR'''
    @property
    def status(self):
        return requests.get(self.__constructUrl('system/status')).json()

    '''This is the licence details of the DP5 registered user'''
    @property
    def licence(self):
        return requests.get(self.__constructUrl('licence')).json()

    '''This returns all the configured containers in the system'''
    def get_all_containers(self):
        return requests.get(self.__constructUrl('containers')).json()

    '''This will scan the container with the requested uid and return the results as JSON.  
    Note that errors are not handled.'''
    def scan_container(self, container_id, 
                       retrieve_raw_image=False, 
                       retrieve_annotated_image=False, 
                       retrieve_1dr2_image=False):
        params = {'container_uid' : container_id, 
                  'raw_image' : str(retrieve_raw_image).lower(),
                  'annotated_image' : str(retrieve_raw_image).lower(),
                  '1dr2_image' : str(retrieve_1dr2_image).lower()}
        return requests.post(self.__constructUrl('scan'), params=params).json()

    def shutdown(self):
        requests.put(self.__constructUrl('system/shutdown'))


if __name__ == '__main__':
    
    #Create the dp5Remote object, note that this expects the DP5 service to be running
    #if it is not then execute C:\Program Files\Ziath\DP5\resources\dp5-server\dp5-headless.exe 
    #(assuming you are on English language windows and using a default install location)
    dp5remote = DP5Remote()
    websocket.enableTrace(False)
    global ws
    global recieve_notification 
    recieve_notification = True
    ws = websocket.create_connection("ws://localhost:8777/dp5-websocket")
    ws.send("CONNECT\naccept-version:1.0,1.1,2.0\n\n\x00\n")

    sub = stomper.subscribe("/topic/events", "random-id", ack='auto')
    ws.send(sub)

    wst = threading.Thread(target=task)
    wst.daemon = True
    wst.start()
   
       
    #obtain some basic information from the system
    print ('version = ' + str(dp5remote.version))
    print ('status = ' + str(dp5remote.status))
    print ('licence = ' + str(dp5remote.licence))

    #get all the configured containers in the system
    containers = dp5remote.get_all_containers()
    print ('containers = ' + str(containers))

    #extract the uid for the first container
    container_uid = containers[0]['uid']
    print('scanning container with uid of ' + container_uid)
    print('scan result = ' + str(dp5remote.scan_container(container_uid)))

    recieve_notification = False

    #close dp5 when finished
    dp5remote.shutdown()

 