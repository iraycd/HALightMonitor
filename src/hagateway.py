import requests
import json
class HAGateway:
    def __init__(self, address):
        self.address = address

    def sendHueLightStatuses(self, id, state):
        valueToSend = {'Id':int(id), 'State': state}
        headers = {'Content-Type': 'application/json'}
        r = requests.post(self.address + '/api/HueLights', data = json.dumps(valueToSend), headers=headers)
        r.close()