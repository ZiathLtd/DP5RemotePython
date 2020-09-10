import json
import requests

'''This class details some baic functions of the DP5 remote API using Python.  There is a swagger page for further documentation
at http://<host>:<port>/swagger-ui.html.  
Note that this uses the external requests module so install that by executing pip3 install reqeusts before runnign the code'''
class DP5Remote:

    def __init__(self):
        self.__host = 'localhost'
        self.__port = 8777

    @property
    def host(self, host):
        return self.__host
    
    @host.setter
    def host(self, host):
        self.__host__ = host

    @property
    def port(self, port):
        return self.__port
    
    @host.setter
    def host(self, port):
        self.__host__ = port

    def __stub(self):
        return f'http://{self.__host}:{self.__port}/dp5/remote/v1'

    def __getUrl(self, path, params=None):
        _path = path
        url = f'{self.__stub()}/{path}'
        return url

    @property
    def version(self):
        return requests.get(self.__getUrl('system/version')).json()

    @property
    def status(self):
        return requests.get(self.__getUrl('system/status')).json()

    @property
    def licence(self):
        return requests.get(self.__getUrl('licence')).json()

if __name__ == '__main__':
    dp5Remote = DP5Remote()
    print ('version = ' + str(dp5Remote.version))
    print ('status = ' + str(dp5Remote.status))
    print ('licence = ' + str(dp5Remote.licence))
