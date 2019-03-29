import urllib
from urllib.parse import quote_plus
from isp_config import *
from isp_utility import get_json, del_json


class HostManager:  # Get Host Information from HOST API ONOS
    def __init__(self, verbose=VERBOSE):
        assert isinstance(verbose, object)
        self.verbose = verbose
        self.host_id = []
        self.host_mac = []
        self.host_ip = []
        self.host_location = []

    def get_hosts(self):
        host_json = sorted(
            get_json("http://{ip}:{port}/onos/v1/hosts".format(ip=ONOS_IP, port=ONOS_PORT))["hosts"],
            key=lambda k: k["id"])
        for n in range(len(host_json)):
            if "id" not in host_json[n]:
                return
            self.host_id.append(host_json[n]["id"])
            self.host_mac.append(host_json[n]["mac"])
            self.host_ip.append(host_json[n]["ipAddresses"])
            self.host_location.append(host_json[n]["locations"])
        return self.host_id, self.host_mac, self.host_ip, self.host_location


class DeviceManager:  # Get Device Information from Device API ONOS
    def __init__(self, verbose=VERBOSE):
        assert isinstance(verbose, object)
        self.verbose = verbose
        self.dev_id = []
        self.dev_type = []
        self.dev_mfr = []
        self.dev_hw = []
        self.dev_chassis_id = []
        self.dev_port = []

    def get_devices(self):
        dev_json = sorted(
            get_json("http://{ip}:{port}/onos/v1/devices".format(ip=ONOS_IP, port=ONOS_PORT))["devices"],
            key=lambda k: k["id"])
        self.dev_id = [dev_json[n]["id"] for n in range(len(dev_json)) if "id" in dev_json[n]]
        for n in range(len(self.dev_id)):
            dev_qte = urllib.parse.quote_plus(self.dev_id[n])
            dev_json_id = get_json(
                "http://{ip}:{port}/onos/v1/devices/{id}/ports".format(ip=ONOS_IP, port=ONOS_PORT, id=dev_qte))
            if "id" not in dev_json_id:
                return
            self.dev_type.append(dev_json_id["type"])
            self.dev_mfr.append(dev_json_id["mfr"])
            self.dev_hw.append(dev_json_id["hw"])
            self.dev_chassis_id.append(dev_json_id["chassisId"])
            self.dev_port.append(dev_json_id["ports"])
        return self.dev_id, self.dev_type, self.dev_mfr, self.dev_hw, self.dev_chassis_id, self.dev_port


class LinkManager:  # Get Link Information from Link API ONOS
    def __init__(self, verbose=VERBOSE):
        assert isinstance(verbose, object)
        self.src_dev = []
        self.src_port = []
        self.dst_dev = []
        self.dst_port = []
        self.link_bw = []
        self.link_port_speed = []
        self.link_json = sorted(
            get_json("http://{ip}:{port}/onos/v1/links".format(ip=ONOS_IP, port=ONOS_PORT))["links"],
            key=lambda k: k["src"]["device"])

    def get_link(self):
        hosts = HostManager()
        host_id, host_mac, host_ip, host_location = hosts.get_hosts()
        devices = DeviceManager()
        dev_id, dev_type, dev_mfr, dev_hw, dev_chassis_id, dev_port = devices.get_devices()
        src_port_speed = 0

        if len(self.src_dev) == len(self.dst_dev):
            for n in range(len(host_id)):
                for m in range(len(host_location[n])):
                    self.src_dev.append(host_id[n])
                    self.src_port.append("1")
                    self.src_dev.append(host_location[n][m]["elementId"])
                    self.src_port.append(host_location[n][m]["port"])
                    self.dst_dev.append(host_location[n][m]["elementId"])
                    self.dst_port.append(host_location[n][m]["port"])
                    self.dst_dev.append(host_id[n])
                    self.dst_port.append("1")
                    for x in range(len(dev_id)):
                        for y in range(len(dev_port[x]) - 1):
                            if (dev_port[x][y + 1]["element"] == host_location[n][m]["elementId"]
                                    and dev_port[x][y + 1]["port"] == host_location[n][m]["port"]):
                                self.link_port_speed.append(dev_port[x][y + 1]["portSpeed"])
                                self.link_port_speed.append(dev_port[x][y + 1]["portSpeed"])
                                self.link_bw.append(dev_port[x][y + 1]["portSpeed"])
                                self.link_bw.append(dev_port[x][y + 1]["portSpeed"])
        for n in range(len(self.link_json)):
            if "src" not in self.link_json[n] and "dst" not in self.link_json[n]:
                return
            self.src_port.append(self.link_json[n]["src"]["port"])
            self.src_dev.append(self.link_json[n]["src"]["device"])
            self.dst_port.append(self.link_json[n]["dst"]["port"])
            self.dst_dev.append(self.link_json[n]["dst"]["device"])
            if "annotations" in self.link_json[n] and "bandwidth" in self.link_json[n]["annotations"]:
                self.link_bw.append(self.link_json[n]["annotations"]["bandwidth"])
            else:
                self.link_bw.append(DEFAULT_CAPACITY)
            for x in range(len(dev_id)):
                for y in range(len(dev_port[x]) - 1):
                    if (dev_port[x][y + 1]["element"] == self.link_json[n]["src"]["device"] and dev_port[x][y + 1][
                        "port"]
                            == self.link_json[n]["src"]["port"]):
                        src_port_speed = dev_port[x][y + 1]["portSpeed"]
                    if (dev_port[x][y + 1]["element"] == self.link_json[n]["dst"]["device"] and dev_port[x][y + 1][
                        "port"]
                            == self.link_json[n]["dst"]["port"]):
                        dst_port_speed = dev_port[x][y + 1]["portSpeed"]
                        if src_port_speed == dst_port_speed:
                            self.link_port_speed.append(src_port_speed)
                        elif src_port_speed < dst_port_speed:
                            self.link_port_speed.append(src_port_speed)
                        else:
                            self.link_port_speed.append(dst_port_speed)
        return self.link_json, self.src_dev, self.src_port, self.dst_dev, self.dst_port, self.link_bw


class IntentManager:  # Get Intents Information from Intents API ONOS
    def __init__(self, verbose=VERBOSE):
        assert isinstance(verbose, object)
        self.verbose = verbose
        self.intent_json = sorted(get_json("http://{ip}:{port}/onos/v1/intents".format(ip=ONOS_IP, port=ONOS_PORT))[
                                      "intents"], key=lambda k: k["id"])
        self.intent_id = [self.intent_json[n]["id"] for n in range(len(self.intent_json)) if
                          "id" in self.intent_json[n]]

    def del_intent(self):
        for n in range(len(self.intent_id)):
            del_json("http://{ip}:{pt}/onos/v1/intents/org.onosproject.cli/{id}".format(ip=ONOS_IP,
                                                                                        pt=ONOS_PORT,
                                                                                        id=self.intent_id[
                                                                                            n]))
