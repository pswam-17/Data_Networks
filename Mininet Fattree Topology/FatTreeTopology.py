from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch, OVSController, OVSBridge
from mininet.link import TCLink
from mininet.cli import CLI

class FatTree(Topo):
    def build(self):
        c = []
        a = []
        e = []
        h = []

        clen = 4
        alen = 8
        elen = 8
        hlen = 16

        # Enable STP on all switches
        switchOpts = {'cls':OVSBridge, 'stp':1}

        for i in range(clen):
            coresw = self.addSwitch('c{}'.format(i+1), **switchOpts)
            c.append(coresw)
        
        for i in range(alen):
            aggsw = self.addSwitch('a{}'.format(i+1), **switchOpts)
            a.append(aggsw)

        for i in range(elen):
            edgesw = self.addSwitch('e{}'.format(i+1), **switchOpts)
            e.append(edgesw)

        for i in range(hlen):
            host = self.addHost('h{}'.format(i+1))
            h.append(host)

        #Core Switches
        for i in range(2):
            self.addLink(c[i], a[0], bw=100, delay='1ms')
            self.addLink(c[i], a[2], bw=100, delay='1ms')
            self.addLink(c[i], a[4], bw=100, delay='1ms')
            self.addLink(c[i], a[6], bw=100, delay='1ms')
        for i in range(2, 4):
            self.addLink(c[i], a[1], bw=100, delay='1ms')
            self.addLink(c[i], a[3], bw=100, delay='1ms')
            self.addLink(c[i], a[5], bw=100, delay='1ms')
            self.addLink(c[i], a[7], bw=100, delay='1ms')

        #Aggregation switch connections
        for i in range(0, 8, 2):
            self.addLink(a[i], e[i], bw=100, delay='1ms')
            self.addLink(a[i], e[i+1], bw=100, delay='1ms')
            self.addLink(a[i+1], e[i], bw=100, delay='1ms')
            self.addLink(a[i+1], e[i+1], bw=100, delay='1ms')

        #Edge switch connections
        for i in range(8):
            self.addLink(e[i], h[2*i], bw=100, delay='1ms')
            self.addLink(e[i], h[2*i+1], bw=100, delay='1ms')


        
topos = {'mytopo':(lambda:FatTree())}

if __name__ == '__main__':
    topo = FatTree()
    net = Mininet(topo=topo, controller=OVSController, link=TCLink)
    net.start()
   
    CLI(net)
    net.stop()

