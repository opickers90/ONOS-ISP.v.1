from collections import defaultdict
from heapq import *
from isp_rest import LinkManager, IntentManager
from isp_utility import intent_p2p_install


# Dijkstra Shortest Path Algorithm
def dijkstra(edges, f, t):
    g = defaultdict(list)
    for l, r, c in edges:
        g[l].append((c, r))

    # dist records the min value of each node in heap.
    q, seen, dist = [(0, f, ())], set(), {f: 0}
    while q:
        (cost, v1, path) = heappop(q)
        if v1 in seen:
            continue

        seen.add(v1)
        path += (v1,)
        if v1 == t:
            return cost, path

        for c, v2 in g.get(v1, ()):
            if v2 in seen:
                continue

            # Not every edge will be calculated. The edge which can improve the value of node in heap will be useful.
            if v2 not in dist or cost + c < dist[v2]:
                dist[v2] = cost + c
                heappush(q, (cost + c, v2, path))

    return float("inf")


def generate_edge():
    link = LinkManager()
    link_json, src_dev, src_port, dst_dev, dst_port, link_bw = link.get_link()
    ref_bw = 100000000
    cost = [ref_bw // int(link_bw[x]) for x in range(len(link_bw))]
    edges = list(zip(src_dev, dst_dev, cost))
    device_in = list(zip(src_dev, src_port))
    device_eg = list(zip(dst_dev, dst_port))
    edges_with_port = list(zip(device_in, device_eg, cost))
    return edges, device_in, device_eg, edges_with_port


def generate_redundant_edge(src, dst):
    edges, dev_in, dev_eg, edge_port = generate_edge()
    path_dijkstra, dij, pij, dej, pej, di, pi, de, pe = calculate_dijkstra_path(src, dst)
    delete_edge = []
    redundant_edges = []
    for y in range(len(edges)):
        for x in range(len(dij)):
            if edges[y][0] == dij[x] and edges[y][1] == dej[x]:
                if "of:" in edges[y][0] and "of:" in edges[y][1]:
                    delete_edge.append(edges[y])
            if edges[y][1] == dij[x] and edges[y][0] == dej[x]:
                if "of:" in edges[y][1] and "of:" in edges[y][0]:
                    delete_edge.append(edges[y])
    delete_edge.sort()
    even = [delete_edge[n] for n in range(len(delete_edge)) if n % 2 == 0]
    odd = [delete_edge[n] for n in range(len(delete_edge)) if n % 2 != 0]
    new_del_edge = list(zip(even, odd))

    for n in range(len(new_del_edge)):
        temp_edge = edges[:]
        redundant_edges.append(temp_edge)

    for n in range(len(redundant_edges)):
        redundant_edges[n].remove(new_del_edge[n][0])
        redundant_edges[n].remove(new_del_edge[n][1])

    for i in range(len(delete_edge)):
        edges.remove(delete_edge[i])
    return redundant_edges, edge_port


def calculate_dijkstra_path(src, dst):
    edge, dev_in, dev_eg, edge_port = generate_edge()
    di_dijkstra = []
    de_dijkstra = []
    pi_dijkstra = []
    pe_dijkstra = []
    di = []
    de = []
    pi = []
    pe = []

    path_dijkstra = dijkstra(edge, src, dst)
    for n in range(len(path_dijkstra[1]) - 1):
        for o in range(len(edge_port)):
            if (path_dijkstra[1][n] == edge_port[o][0][0] and path_dijkstra[1][n + 1] ==
                    edge_port[o][1][0]):
                di_dijkstra.append(edge_port[o][0][0])
                pi_dijkstra.append(edge_port[o][0][1])
                de_dijkstra.append(edge_port[o][1][0])
                pe_dijkstra.append(edge_port[o][1][1])
                if "of:" in edge_port[o][0][0]:
                    de.append(edge_port[o][0][0])
                    pe.append(edge_port[o][0][1])
                if "of:" in edge_port[o][1][0]:
                    di.append(edge_port[o][1][0])
                    pi.append(edge_port[o][1][1])
    return path_dijkstra, di_dijkstra, pi_dijkstra, de_dijkstra, pe_dijkstra, di, pi, de, pe


def calculate_redundant_dijkstra_path(src, dst):
    redundant_edge, edge_port = generate_redundant_edge(src, dst)
    di_dijkstra = []
    de_dijkstra = []
    pi_dijkstra = []
    pe_dijkstra = []
    di = []
    de = []
    pi = []
    pe = []

    redundant_dijkstra = []
    redundant_di_dijkstra = []
    redundant_de_dijkstra = []
    redundant_pi_dijkstra = []
    redundant_pe_dijkstra = []
    redundant_di = []
    redundant_de = []
    redundant_pi = []
    redundant_pe = []
    new_redundant_dijkstra = []

    for edge in redundant_edge:
        path_dijkstra = dijkstra(edge, src, dst)
        redundant_dijkstra.append(path_dijkstra)

    redundant_dijkstra.sort()
    for i in redundant_dijkstra:
        if i not in new_redundant_dijkstra:
            new_redundant_dijkstra.append(i)

    for index in range(len(new_redundant_dijkstra)):
        for n in range(len(new_redundant_dijkstra[index][1]) - 1):
            for o in range(len(edge_port)):
                if (new_redundant_dijkstra[index][1][n] == edge_port[o][0][0] and
                        new_redundant_dijkstra[index][1][n + 1] == edge_port[o][1][0]):
                    di_dijkstra.append(edge_port[o][0][0])
                    pi_dijkstra.append(edge_port[o][0][1])
                    de_dijkstra.append(edge_port[o][1][0])
                    pe_dijkstra.append(edge_port[o][1][1])
                    if "of:" in edge_port[o][0][0]:
                        de.append(edge_port[o][0][0])
                        pe.append(edge_port[o][0][1])
                    if "of:" in edge_port[o][1][0]:
                        di.append(edge_port[o][1][0])
                        pi.append(edge_port[o][1][1])
        redundant_di_dijkstra.append(di_dijkstra)
        redundant_de_dijkstra.append(de_dijkstra)
        redundant_pi_dijkstra.append(pi_dijkstra)
        redundant_pe_dijkstra.append(pe_dijkstra)
        redundant_di.append(di)
        redundant_de.append(de)
        redundant_pi.append(pi)
        redundant_pe.append(pe)
    return (new_redundant_dijkstra, redundant_di_dijkstra, redundant_pi_dijkstra, redundant_de_dijkstra,
            redundant_pe_dijkstra, redundant_di, redundant_pi, redundant_de, redundant_pe)


def install_best_dijkstra_path(src, dst, priority):
    path_dijkstra, dij, pij, dej, pej, di, pi, de, pe = calculate_dijkstra_path(src, dst)
    path = " - ".join(path_dijkstra[1])
    print("Dijkstra's Shortest Path Calculation Result: \n")
    print(path)
    print("Total Cost for this path: {cost}\n".format(cost=path_dijkstra[0]))
    print("------------------------------------------------------------------------------------------")
    print("Installing Best-Path Dijkstra's Shortest Path..\n")
    intent = IntentManager()
    intent.del_intent()
    print("Forwarding Intents based on Path Information")
    if len(di) == len(de):
        for n in range(len(de)):
            response = intent_p2p_install(pi[n], di[n], pe[n], de[n], priority)
            print("{no}.  Ingress = {di}:{pi} <--->  Egress = {de}:{pe} : status {stt}".format(no=n + 1, di=di[n],
                                                                                               pi=pi[n], de=de[n],
                                                                                               pe=pe[n],
                                                                                               stt=response))
    # Install Reverse Forwarding Intent based on Path Information
    print("Reverse/Backwarding Intents based on Path Information")
    if len(di) == len(de):
        for n in range(len(de)):
            response = intent_p2p_install(pe[n], de[n], pi[n], di[n], priority)
            print("{no}.  Ingress = {de}:{pe} <--->  Egress = {di}:{pi} : status {stt}".format(no=n + 1, di=di[n],
                                                                                               pi=pi[n],
                                                                                               de=de[n], pe=pe[n],
                                                                                               stt=response))


def install_best_redundant_dijkstra_path(src, dst, priority):
    path_dijkstra, dij, pij, dej, pej, di, pi, de, pe = calculate_redundant_dijkstra_path(src, dst)
    print("Dijkstra's Shortest Path Calculation Result: \n")
    print("\nTotal Redundant Path: {total}\n".format(total=len(path_dijkstra)))
    for i in range(len(path_dijkstra)):
        path = " - ".join(path_dijkstra[i][1])
        print("{no}: {path}".format(no=i + 1, path=path))
        print("Total Cost for this path: {cost}\n".format(cost=path_dijkstra[i][0]))
    print("------------------------------------------------------------------------------------------")
    print("Installing Best-Path Redundant Dijkstra's Shortest Path...\n")
    print("Forwarding Intents based on Path Information")
    if len(di[0]) == len(de[0]):
        for n in range(len(path_dijkstra[0][1])-2):
            response = intent_p2p_install(pi[0][n], di[0][n], pe[0][n], de[0][n], priority)
            print(
                "{no}.  Ingress = {di}:{pi} <--->  Egress = {de}:{pe} : status {stt}".format(no=n + 1, di=di[0][n],
                                                                                             pi=pi[0][n],
                                                                                             de=de[0][n],
                                                                                             pe=pe[0][n],
                                                                                             stt=response))
    # Install Reverse Forwarding Intent based on Path Information
    print("\n")
    print("Reverse/Backwarding Intents based on Path Information")
    if len(di[0]) == len(de[0]):
        for n in range(len(path_dijkstra[0][1])-2):
            response = intent_p2p_install(pe[0][n], de[0][n], pi[0][n], di[0][n], priority)
            print(
                "{no}.  Ingress = {de}:{pe} <--->  Egress = {di}:{pi} : status {stt}".format(no=n + 1, di=di[0][n],
                                                                                             pi=pi[0][n],
                                                                                             de=de[0][n],
                                                                                             pe=pe[0][n],
                                                                                             stt=response))
