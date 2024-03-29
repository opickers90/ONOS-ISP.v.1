from isp_rest import HostManager, LinkManager
from isp_dijkstra import install_best_dijkstra_path, install_best_redundant_dijkstra_path
from time import sleep


def running_program():         # Running main program
    print("Retrieving Path Calculation using Dijkstra...")
    priority = 100
    topology_init = LinkManager()
    link_1_json, src_1_dev, src_1_port, dst_1_dev, dst_1_port, link_1_bw = topology_init.get_link()
    src, dst = input_host()
    dijkstra_shortest_path(src, dst, priority)
    try:
        while True:
            topology_after = LinkManager()
            link_2_json, src_2_dev, src_2_port, dst_2_dev, dst_2_port, link_2_bw = topology_after.get_link()
            if link_2_json == link_1_json:
                print("Dijkstra Success... Press (Ctrl + C) for exit")
            else:
                print("updating path calculation...")
                dijkstra_shortest_path(src, dst, priority)
                link_1_json = link_2_json
                continue
    except KeyboardInterrupt:
        running_program()


def input_host():           # define source and destination
    hosts = HostManager()
    host_id, host_mac, host_ip, host_location = hosts.get_hosts()
    for n in range(len(host_id)):
        print("-----------------------------------------------")
        print("{no}. Host ID           = {id}".format(no=n + 1, id=host_id[n]))
        print("IP Address           = {ip}".format(ip=host_ip[n]))
        print("MAC Address          = {mac}".format(mac=host_mac[n]))
        print("-----------------------------------------------\n")
    counter = 1
    src_input = 0
    dst_input = 0
    while counter == 1:
        src_input = int(input("Choose Source Host\n"))
        dst_input = int(input("Choose Destination Host\n"))
        if src_input in range(1, len(host_id) + 1):
            src_input = host_id[src_input - 1]
            if dst_input in range(1, len(host_id) + 1):
                dst_input = host_id[dst_input - 1]
                counter = 0
            else:
                print("Destination not in list")
                counter = 1
        else:
            print("Source not in list")
            counter = 1
    print("Source       : {src}\n".format(src=src_input))
    print("Destination  : {dst}\n".format(dst=dst_input))
    return src_input, dst_input


def dijkstra_shortest_path(source, destination, priority):  # calculate path from source and destination
    print("\nCalculate Dijkstra Shortest Path....")
    try:
        print("\n----------------------------------Dijkstra Primary Path-----------------------------------\n")
        install_best_dijkstra_path(source, destination, priority)
        sleep(1)
        print("\n----------------------------------Dijkstra Secondary Path-----------------------------------\n")
        install_best_redundant_dijkstra_path(source, destination, priority - 10)
        sleep(1)
    except TypeError:
        print("\nNo Path Found")
