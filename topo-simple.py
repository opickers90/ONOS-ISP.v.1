#!/usr/bin/env python

from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.link import TCLink
from config import *

class ExampleTestTopo(Topo):
    def __init__(self, bw=1e3, **opts):
        super(ExampleTestTopo, self).__init__(**opts)

        s = [self.addSwitch('s%d' % n) for n in range(1, 6)]
        h = [self.addHost('h%d' % n) for n in range(1, 5)]

        self.addLink(s[0], s[1], bw=1000)
        self.addLink(s[0], s[4], bw=1)
        self.addLink(s[1], s[2], bw=1000)
        self.addLink(s[2], s[3], bw=1000)
        self.addLink(s[3], s[4], bw=1000)
        self.addLink(s[0], s[3], bw=10)
        self.addLink(s[1], s[4], bw=10)
        self.addLink(s[1], s[3], bw=100)

        self.addLink(h[0], s[0], bw=1000)
        self.addLink(h[1], s[1], bw=1000)
        self.addLink(h[2], s[3], bw=1000)
        self.addLink(h[3], s[4], bw=1000)

if __name__ == '__main__':
    topo = ExampleTestTopo()
    sw = OVSKernelSwitch #already the default
    c0 = RemoteController( 'c0', ip=ONOS_IP, port=6633 )
    net = Mininet(topo=topo,
                  controller=c0,
                  switch = sw,
                  cleanup=True,
                  autoSetMacs=True,
                  autoStaticArp=False,
                  link=TCLink)
    net.start()
    CLI(net)
    net.stop()






