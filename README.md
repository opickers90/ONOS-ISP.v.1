# ONOS-ISP.v.1


## Tutorial
###  Set up Environment

Start ONOS controller:
```
$ cd ~/onos-1.13.2/
./bin/onos-service clean
```

Once ONOS is ready, go to ONOS CLI from another terminal:
```
$onos localhost
```
```
Welcome to Open Network Operating System (ONOS)!
     ____  _  ______  ____     
    / __ \/ |/ / __ \/ __/   
   / /_/ /    / /_/ /\ \     
   \____/_/|_/\____/___/     
                               
Documentation: wiki.onosproject.org      
Tutorials:     tutorials.onosproject.org 
Mailing lists: lists.onosproject.org     

Come help out! Find out how at: contribute.onosproject.org 

Hit '<tab>' for a list of available commands
and '[cmd] --help' for help on a specific command.
Hit '<ctrl-d>' or type 'system:shutdown' or 'logout' to shutdown ONOS.

onos> 
```
Create a simple Mininet topology from another terminal:
```
cd ~/ONOS-ISP.v.1/
sudo python topo-simple.py
```

After simple Mininet topology created, configure link bandwitdh:
```
curl --user onos:rocks -X POST -H "Content-Type: application/json" http://localhost:8181/onos/v1/network/configuration/ -d ~/topo-simple-netcfg.json
```

Test pingall to make sure the Host already discovered:
```
mininet> pingall
*** Ping: testing ping reachability
h1 -> h2 h3 h4 
h2 -> h1 h3 h4 
h3 -> h1 h2 h4 
h4 -> h1 h2 h3 
*** Results: 0% dropped (12/12 received)
mininet> 

```
From This Step, Environment already finish.
Next Step to use ONOS-ISP Application


### 2) ONOS-ISP Application
#### Tutorial 1: Dijkstra Shortest Path Calculation Tutorial:
Test ping from host 1 to host 4:
 ```
mininet> h1 ping -s 65000 h4
PING 10.0.0.4 (10.0.0.4): 65000 data bytes
65008 bytes from 10.0.0.4: icmp_seq=0 ttl=64 time=1030.659 ms
65008 bytes from 10.0.0.4: icmp_seq=1 ttl=64 time=1018.946 ms
65008 bytes from 10.0.0.4: icmp_seq=2 ttl=64 time=1017.233 ms
65008 bytes from 10.0.0.4: icmp_seq=3 ttl=64 time=1016.674 ms
65008 bytes from 10.0.0.4: icmp_seq=4 ttl=64 time=1017.082 ms
......
```
As we can see the default forwding applicaton give high latency.

Next stop the fwd application and ping from host 1 to host 4 will time out:
```
onos> app deactivate org.onosproject.fwd
Deactivated org.onosproject.fwd
```
```
mininet> h1 ping -s 65000 h4
PING 10.0.0.4 (10.0.0.4): 65000 data bytes
```

Start the Application:
```
cd ~/ONOS-ISP.v.1/
sudo python3 isp_main.py
```

When The Application Start, Choose 1 to Run Djikstra's Shortest Path Calculation:
```
Press 1 to Run Dijkstra's Shortest Path Calculation
Press 0 to QUIT

Enter Your Choice: 1
```
Next Choose Source and Destination:
(in this example, i choose Host 1 as Source and Host 4 as Destination)
```angular2
Retrieving Path Calculation using Dijkstra...
-----------------------------------------------
1. Host ID           = 00:00:00:00:00:01/None
IP Address           = ['10.0.0.1']
MAC Address          = 00:00:00:00:00:01
-----------------------------------------------

-----------------------------------------------
2. Host ID           = 00:00:00:00:00:02/None
IP Address           = ['10.0.0.2']
MAC Address          = 00:00:00:00:00:02
-----------------------------------------------

-----------------------------------------------
3. Host ID           = 00:00:00:00:00:03/None
IP Address           = ['10.0.0.3']
MAC Address          = 00:00:00:00:00:03
-----------------------------------------------

-----------------------------------------------
4. Host ID           = 00:00:00:00:00:04/None
IP Address           = ['10.0.0.4']
MAC Address          = 00:00:00:00:00:04
-----------------------------------------------

Choose Source Host
1
Choose Destination Host
4
Source       : 00:00:00:00:00:01/None

Destination  : 00:00:00:00:00:04/None
...
```
after choose source and destination, this application will begin automatically calculating for primary and backup best path:
```
....

Calculate Dijkstra Shortest Path....

----------------------------------Dijkstra Primary Path-----------------------------------

Dijkstra's Shortest Path Calculation Result: 

00:00:00:00:00:01/None - of:0000000000000001 - of:0000000000000002 - of:0000000000000003 - of:0000000000000004 - of:0000000000000005 - 00:00:00:00:00:04/None
Total Cost for this path: 420000

------------------------------------------------------------------------------------------
Installing Best-Path Dijkstra's Shortest Path..

Forwarding Intents based on Path Information
1.  Ingress = of:0000000000000001:4 <--->  Egress = of:0000000000000001:1 : status <Response [201]>
2.  Ingress = of:0000000000000002:1 <--->  Egress = of:0000000000000002:2 : status <Response [201]>
3.  Ingress = of:0000000000000003:1 <--->  Egress = of:0000000000000003:2 : status <Response [201]>
4.  Ingress = of:0000000000000004:1 <--->  Egress = of:0000000000000004:2 : status <Response [201]>
5.  Ingress = of:0000000000000005:2 <--->  Egress = of:0000000000000005:4 : status <Response [201]>
Reverse/Backwarding Intents based on Path Information
1.  Ingress = of:0000000000000001:1 <--->  Egress = of:0000000000000001:4 : status <Response [201]>
2.  Ingress = of:0000000000000002:2 <--->  Egress = of:0000000000000002:1 : status <Response [201]>
3.  Ingress = of:0000000000000003:2 <--->  Egress = of:0000000000000003:1 : status <Response [201]>
4.  Ingress = of:0000000000000004:2 <--->  Egress = of:0000000000000004:1 : status <Response [201]>
5.  Ingress = of:0000000000000005:4 <--->  Egress = of:0000000000000005:2 : status <Response [201]>

----------------------------------Dijkstra Secondary Path-----------------------------------

Dijkstra's Shortest Path Calculation Result: 


Total Redundant Path: 3

1: 00:00:00:00:00:01/None - of:0000000000000001 - of:0000000000000002 - of:0000000000000004 - of:0000000000000005 - 00:00:00:00:00:04/None
Total Cost for this path: 1220000

2: 00:00:00:00:00:01/None - of:0000000000000001 - of:0000000000000002 - of:0000000000000005 - 00:00:00:00:00:04/None
Total Cost for this path: 10120000

3: 00:00:00:00:00:01/None - of:0000000000000001 - of:0000000000000004 - of:0000000000000005 - 00:00:00:00:00:04/None
Total Cost for this path: 10120000

------------------------------------------------------------------------------------------
Installing Best-Path Redundant Dijkstra's Shortest Path...

Forwarding Intents based on Path Information
1.  Ingress = of:0000000000000001:4 <--->  Egress = of:0000000000000001:1 : status <Response [201]>
2.  Ingress = of:0000000000000002:1 <--->  Egress = of:0000000000000002:4 : status <Response [201]>
3.  Ingress = of:0000000000000004:4 <--->  Egress = of:0000000000000004:2 : status <Response [201]>
4.  Ingress = of:0000000000000005:2 <--->  Egress = of:0000000000000005:4 : status <Response [201]>


Reverse/Backwarding Intents based on Path Information
1.  Ingress = of:0000000000000001:1 <--->  Egress = of:0000000000000001:4 : status <Response [201]>
2.  Ingress = of:0000000000000002:4 <--->  Egress = of:0000000000000002:1 : status <Response [201]>
3.  Ingress = of:0000000000000004:2 <--->  Egress = of:0000000000000004:4 : status <Response [201]>
4.  Ingress = of:0000000000000005:4 <--->  Egress = of:0000000000000005:2 : status <Response [201]>

```

and check to previous ping from host 1 to host 4:
```
mininet> h1 ping -s 65000 h4
PING 10.0.0.4 (10.0.0.4): 65000 data bytes
65008 bytes from 10.0.0.4: icmp_seq=204 ttl=64 time=16.866 ms
65008 bytes from 10.0.0.4: icmp_seq=205 ttl=64 time=2.160 ms
65008 bytes from 10.0.0.4: icmp_seq=206 ttl=64 time=1.756 ms
65008 bytes from 10.0.0.4: icmp_seq=207 ttl=64 time=1.280 ms
65008 bytes from 10.0.0.4: icmp_seq=208 ttl=64 time=1.233 ms
....
```
We can see the path and latency is is different with default ONOS forwarding application

#### Toturial 2: Updating Path when Topology changing (e.g. link down):
Following previous tutorial, now try to shutdown link between switch 1 and switch 2:
```
mininet> link s1 s2 down
```

Check the ONOS-ISP Application, it will automatically calculate new primary and backup path:
```
...

Dijkstra Success... Press (Ctrl + C) for exit
updating path calculation...

Calculate Dijkstra Shortest Path....

----------------------------------Dijkstra Primary Path-----------------------------------

Dijkstra's Shortest Path Calculation Result: 

00:00:00:00:00:01/None - of:0000000000000001 - of:0000000000000004 - of:0000000000000005 - 00:00:00:00:00:04/None
Total Cost for this path: 10120000

------------------------------------------------------------------------------------------
Installing Best-Path Dijkstra's Shortest Path..

Forwarding Intents based on Path Information
1.  Ingress = of:0000000000000001:4 <--->  Egress = of:0000000000000001:3 : status <Response [201]>
2.  Ingress = of:0000000000000004:3 <--->  Egress = of:0000000000000004:2 : status <Response [201]>
3.  Ingress = of:0000000000000005:2 <--->  Egress = of:0000000000000005:4 : status <Response [201]>
Reverse/Backwarding Intents based on Path Information
1.  Ingress = of:0000000000000001:3 <--->  Egress = of:0000000000000001:4 : status <Response [201]>
2.  Ingress = of:0000000000000004:2 <--->  Egress = of:0000000000000004:3 : status <Response [201]>
3.  Ingress = of:0000000000000005:4 <--->  Egress = of:0000000000000005:2 : status <Response [201]>

----------------------------------Dijkstra Secondary Path-----------------------------------

Dijkstra's Shortest Path Calculation Result: 


Total Redundant Path: 2

1: 00:00:00:00:00:01/None - of:0000000000000001 - of:0000000000000004 - of:0000000000000003 - of:0000000000000002 - of:0000000000000005 - 00:00:00:00:00:04/None
Total Cost for this path: 20220000

2: 00:00:00:00:00:01/None - of:0000000000000001 - of:0000000000000005 - 00:00:00:00:00:04/None
Total Cost for this path: 100020000

------------------------------------------------------------------------------------------
Installing Best-Path Redundant Dijkstra's Shortest Path...

Forwarding Intents based on Path Information
1.  Ingress = of:0000000000000001:4 <--->  Egress = of:0000000000000001:3 : status <Response [201]>
2.  Ingress = of:0000000000000004:3 <--->  Egress = of:0000000000000004:1 : status <Response [201]>
3.  Ingress = of:0000000000000003:2 <--->  Egress = of:0000000000000003:1 : status <Response [201]>
4.  Ingress = of:0000000000000002:2 <--->  Egress = of:0000000000000002:3 : status <Response [201]>
5.  Ingress = of:0000000000000005:3 <--->  Egress = of:0000000000000005:4 : status <Response [201]>


Reverse/Backwarding Intents based on Path Information
1.  Ingress = of:0000000000000001:3 <--->  Egress = of:0000000000000001:4 : status <Response [201]>
2.  Ingress = of:0000000000000004:1 <--->  Egress = of:0000000000000004:3 : status <Response [201]>
3.  Ingress = of:0000000000000003:1 <--->  Egress = of:0000000000000003:2 : status <Response [201]>
4.  Ingress = of:0000000000000002:3 <--->  Egress = of:0000000000000002:2 : status <Response [201]>
5.  Ingress = of:0000000000000005:4 <--->  Egress = of:0000000000000005:3 : status <Response [201]>
Dijkstra Success... Press (Ctrl + C) for exit
...
```
and check ping from host 1 to host 4:
```
mininet> h1 ping -s 65000 h4
PING 10.0.0.4 (10.0.0.4): 65000 data bytes
65008 bytes from 10.0.0.4: icmp_seq=0 ttl=64 time=108.107 ms
65008 bytes from 10.0.0.4: icmp_seq=1 ttl=64 time=102.270 ms
65008 bytes from 10.0.0.4: icmp_seq=2 ttl=64 time=102.212 ms
65008 bytes from 10.0.0.4: icmp_seq=3 ttl=64 time=102.485 ms
...
```
the connection still working, but with different path and latency.