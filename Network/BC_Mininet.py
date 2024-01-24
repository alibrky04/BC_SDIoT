#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel, info

setLogLevel('info')

class CustomTopo(Topo):
    def build(self):

        switch = self.addSwitch('s1')

        for i in range(15):
            host = self.addHost(f'h{i+1}')
            self.addLink(host, switch)

net = Mininet(controller=RemoteController, switch=OVSSwitch, waitConnected=True)

print("*** Creating (reference) controller")
c0 = RemoteController('c0', ip='127.0.0.1', port=6633)
c1 = RemoteController('c1', ip='127.0.0.1', port=6634)
c2 = RemoteController('c2', ip='127.0.0.1', port=6635)

print("*** Creating Network Topology")
topo = CustomTopo()
net = Mininet(topo=topo, switch=OVSSwitch, build=False, waitConnected=True)
net.addController(c0)
net.addController(c1)
net.addController(c2)

print("*** Starting network")
net.build()
net.start()

print("***  Running CLI")
CLI(net)

net.pingAll()

print("*** Stopping network")
net.stop()