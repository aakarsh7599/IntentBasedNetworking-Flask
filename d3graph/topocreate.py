from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
#from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):
    "A LinuxRouter connecting three IP subnets"

    def build( self, **_opts ):

        defaultIP = '10.0.1.1/24'  # IP address for r0-eth1
#	defaultIP1 = '10.0.10.13/24'
        r0 = self.addNode( 'r0', cls=LinuxRouter, ip=defaultIP )
#        r1 = self.addNode( 'r1', cls=LinuxRouter, ip=defaultIP1 )

        h1 = self.addHost( 'h1', ip='10.0.1.12/24', defaultRoute='via 10.0.1.1' )

        h2 = self.addHost( 'h2', ip='198.0.5.2/24', defaultRoute='via 198.0.5.1' )
        h3 = self.addHost( 'h3', ip='198.0.5.3/24', defaultRoute='via 198.0.5.1' )
        h4 = self.addHost( 'h4', ip='172.0.10.4/24', defaultRoute='via 172.0.10.1' )
        h5 = self.addHost( 'h5', ip='172.0.10.5/24', defaultRoute='via 172.0.10.1' )
        
#        h6 = self.addHost( 'h6', ip='10.0.4.2/24', defaultRoute='via 10.0.4.1' )
#        h7 = self.addHost( 'h7', ip='10.0.4.3/24', defaultRoute='via 10.0.4.1' )
#        h8 = self.addHost( 'h8', ip='10.0.5.2/24', defaultRoute='via 10.0.5.1' )
#        h9 = self.addHost( 'h9', ip='10.0.5.3/24', defaultRoute='via 10.0.5.1' )
   
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
#        s3 = self.addSwitch('s3')
#        s4 = self.addSwitch('s4')

        self.addLink( h1, r0, intfName2='r0-eth1', params2={ 'ip' : '20.0.1.1/24' } )
        self.addLink( s1, r0, intfName2='r0-eth2', params2={ 'ip' : '198.0.5.1/24' } )
        self.addLink( s2, r0, intfName2='r0-eth0', params2={ 'ip' : '172.0.10.1/24' } )

#        self.addLink( r0, r1, intfName2='r1-eth1', params2={ 'ip' : '10.0.10.1/24' } )
#        self.addLink( s3, r1, intfName2='r1-eth2', params2={ 'ip' : '10.0.4.1/24' } )
#        self.addLink( s4, r1, intfName2='r1-eth1', params2={ 'ip' : '10.0.5.1/24' } )

#        self.addLink( h1, r0, intfName2='r1-eth0', params2={ 'ip' : '10.0.1.1/24' } )
#        self.addLink( h1, r1, intfName2='r0-eth0', params2={ 'ip' : '10.0.4.1/24' } )
        

        self.addLink(r0, h1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
        self.addLink(h4, s2)
        self.addLink(h5, s2)

#        self.addLink(r1, r0)
#        self.addLink(h6, s3)
#        self.addLink(h7, s3)
#        self.addLink(h8, s4)
#        self.addLink(h9, s4)

def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet( topo=topo )  # controller is used by s1-s3
    net.start()
    info( '*** Routing Table on Router:\n' )
    print net[ 'r0' ].cmd( 'route' )
#    print net[ 'r1' ].cmd( 'route' )
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()


