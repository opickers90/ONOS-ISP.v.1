#!/usr/bin/env python

from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.link import TCLink
from isp_config import *


class ExampleTestTopo(Topo):
    def __init__(self, bw=1e3, **opts):
        super(ExampleTestTopo, self).__init__(**opts)

        # Add hosts and switches

        Switch1 = self.addSwitch('s1')
        Switch2 = self.addSwitch('s2')
        Switch3 = self.addSwitch('s3')
        Switch4 = self.addSwitch('s4')
        Switch5 = self.addSwitch('s5')
        Switch6 = self.addSwitch('s6')
        Switch7 = self.addSwitch('s7')
        Switch8 = self.addSwitch('s8')
        Switch9 = self.addSwitch('s9')
        Switch10 = self.addSwitch('s10')
        Switch11 = self.addSwitch('s11')
        Switch12 = self.addSwitch('s12')
        Switch13 = self.addSwitch('s13')
        Switch14 = self.addSwitch('s14')
        Switch15 = self.addSwitch('s15')
        Switch16 = self.addSwitch('s16')
        Switch17 = self.addSwitch('s17')
        Switch18 = self.addSwitch('s18')
        Switch19 = self.addSwitch('s19')
        Switch20 = self.addSwitch('s20')

        Host1 = self.addHost('h1')
        Host2 = self.addHost('h2')
        Host3 = self.addHost('h3')
        Host4 = self.addHost('h4')
        Host5 = self.addHost('h5')
        Host6 = self.addHost('h6')
        Host7 = self.addHost('h7')
        Host8 = self.addHost('h8')
        Host9 = self.addHost('h9')
        Host10 = self.addHost('h10')
        Host11 = self.addHost('h11')
        Host12 = self.addHost('h12')
        Host13 = self.addHost('h13')
        Host14 = self.addHost('h14')
        Host15 = self.addHost('h15')
        Host16 = self.addHost('h16')

        # Add links
        self.addLink(Host1, Switch1)
        self.addLink(Host2, Switch1)
        self.addLink(Host3, Switch2)
        self.addLink(Host4, Switch2)
        self.addLink(Host5, Switch3)
        self.addLink(Host6, Switch3)
        self.addLink(Host7, Switch4)
        self.addLink(Host8, Switch4)
        self.addLink(Host9, Switch5)
        self.addLink(Host10, Switch5)
        self.addLink(Host11, Switch6)
        self.addLink(Host12, Switch6)
        self.addLink(Host13, Switch7)
        self.addLink(Host14, Switch7)
        self.addLink(Host15, Switch8)
        self.addLink(Host16, Switch8)
        self.addLink(Switch1, Switch9)
        self.addLink(Switch1, Switch10)
        self.addLink(Switch2, Switch9)
        self.addLink(Switch2, Switch10)
        self.addLink(Switch3, Switch11)
        self.addLink(Switch3, Switch12)
        self.addLink(Switch4, Switch11)
        self.addLink(Switch4, Switch12)
        self.addLink(Switch5, Switch13)
        self.addLink(Switch5, Switch14)
        self.addLink(Switch6, Switch13)
        self.addLink(Switch6, Switch14)
        self.addLink(Switch7, Switch15)
        self.addLink(Switch7, Switch16)
        self.addLink(Switch8, Switch15)
        self.addLink(Switch8, Switch16)
        self.addLink(Switch9, Switch17)
        self.addLink(Switch9, Switch18)
        self.addLink(Switch10, Switch19)
        self.addLink(Switch10, Switch20)
        self.addLink(Switch11, Switch18)
        self.addLink(Switch11, Switch19)
        self.addLink(Switch12, Switch17)
        self.addLink(Switch12, Switch20)
        self.addLink(Switch13, Switch19)
        self.addLink(Switch13, Switch20)
        self.addLink(Switch14, Switch17)
        self.addLink(Switch14, Switch18)
        self.addLink(Switch15, Switch17)
        self.addLink(Switch15, Switch20)
        self.addLink(Switch16, Switch18)
        self.addLink(Switch16, Switch19)

if __name__ == '__main__':
    topo = ExampleTestTopo()
    sw = OVSKernelSwitch  # already the default
    c0 = RemoteController('c0', ip=ONOS_IP, port=6633)
    net = Mininet(topo=topo,
                  controller=c0,
                  switch=sw,
                  cleanup=True,
                  autoSetMacs=True,
                  autoStaticArp=False,
                  link=TCLink)
    net.start()
    CLI(net)
    net.stop()
