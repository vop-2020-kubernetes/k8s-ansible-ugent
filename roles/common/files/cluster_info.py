#!/usr/bin/env python3

import xml.etree.ElementTree as elementTree
import ipaddress
import subprocess
import json
import sys

def short_to_long_mac(s):
    return ":".join(s[i:i + 2] for i in range(0, len(s), 2))

def load_manifest():
    manifest = subprocess.check_output("geni-get manifest", shell=True).decode("utf-8")

    namespaces = {
        "ns": "http://www.geni.net/resources/rspec/3",
        "emulab": "http://www.protogeni.net/resources/rspec/ext/emulab/1"
    }

    return elementTree.fromstring(manifest), namespaces

def get_public_ip_pools():
    root, namespaces = load_manifest()
    pools = {}
    for pool in root.findall("emulab:routable_pool", namespaces):
        pools[pool.get("client_id")] = []

        for ip in pool.findall("emulab:ipv4", namespaces):
            net = str(ipaddress.ip_network("{}/{}".format(ip.get("address"), ip.get("netmask")), False))
            pools[pool.get("client_id")] += [{
                "type": "ipv4",
                "ip": str(ipaddress.ip_address(ip.get("address"))),
                "net": net.split("/")[0],
                "sub": net.split("/")[1]
            }]
    return pools

def get_interfaces():
    root, namespaces = load_manifest()
    client_id = subprocess.check_output("geni-get client_id", shell=True).decode("utf-8").strip()
    control_mac = subprocess.check_output("geni-get control_mac", shell=True).decode("utf-8").strip()

    interfaces = {
        "management": short_to_long_mac(control_mac)
    }
    for node in root.findall("ns:node", namespaces):
        if node.get("client_id") != client_id: continue
        for interface in node.findall("ns:interface", namespaces):
            interfaces[interface.get("client_id").split(":")[1]] = short_to_long_mac(interface.get("mac_address"))
        break
    return interfaces

def get_full_hostname():
    root, namespaces = load_manifest()
    client_id = subprocess.check_output("geni-get client_id", shell=True).decode("utf-8").strip()

    for node in root.findall("ns:node", namespaces):
        if node.get("client_id") != client_id: continue
        return node.find("ns:host", namespaces).get("name").strip()
    return None

if sys.argv[1] == "pub_ip_pools":
    print(json.dumps(get_public_ip_pools()))
elif sys.argv[1] == "interfaces":
    print(json.dumps(get_interfaces()))
elif sys.argv[1] == "full_hostname":
    print(get_full_hostname())
