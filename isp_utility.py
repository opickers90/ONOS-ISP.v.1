import requests
import logging
import json
from requests.auth import HTTPBasicAuth
from isp_config import *


# For GET REST API
def get_json(url):
    try:
        req = requests.get(url, auth=HTTPBasicAuth(ONOS_USER, ONOS_PASS))
        return req.json()
    except IOError as e:
        logging.error(e)
        return ''


# For POST REST API
def post_json(url, json_data):
    try:
        headers = {'content-type': 'application/json'}
        req = requests.post(url, data=json.dumps(json_data), headers=headers, auth=HTTPBasicAuth(ONOS_USER, ONOS_PASS))
        return req
    except IOError as e:
        logging.error(e)
        return ''


# For DELETE REST API
def del_json(url):
    try:
        req = requests.delete(url, auth=HTTPBasicAuth(ONOS_USER, ONOS_PASS))
        return req
    except IOError as e:
        logging.error(e)
        return ''


# Post Intents to Intents API
def intent_p2p_install(port_in, device_in, port_en, device_en, priority=100):
    data = {
        "type": "PointToPointIntent",
        "appId": "org.onosproject.cli",
        "resources": [],
        "selector": {
            "criteria": []
        },
        "treatment": {
            "instructions": [
                {
                    "type": "NOACTION"
                }
            ],
            "deferred": []
        },
        "priority": priority,
        "constraints": [],
        "ingressPoint": {
            "port": port_in,
            "device": device_in
        },
        "egressPoint": {
            "port": port_en,
            "device": device_en
        }
    }

    post_intent = post_json("http://{ip}:{port}/onos/v1/intents".format(ip=ONOS_IP, port=ONOS_PORT), data)
    return post_intent
