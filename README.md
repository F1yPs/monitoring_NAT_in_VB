# Monitoring NAT in VirtualBox 
Hello    
For job with this repositories you need it:    
1)2 Virtual Machine (Ubuntu 18.04+) in VirtualBox or other program for virtualization    
2)Any web-browser
# Settings Virtual Machine
1)for VM1(in the role PC) need settings:
- to configure /etc/netplan/00-00-installer-config.yaml    
- check routing information with example "ip route"   
- in menu settings VirtualBox for the net VM1 choice "internal net"     
2)for VM2(in the role route with NAT) need settings:
- to configure /etc/netplan/00-00-installer-config.yaml    
- check routing information with example "ip route"    
- in menu settings VirtualBox for the net VM2 choice "network bridge"    
- add rule in iptables, as    
    + sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT    
    + iptables -t nat -A PREROUTING -d x.x.x.x -j DNAT --to-destination y.y.y.y    
        +  where x.x.x.x - source IP y.y.y.y - distination IP    
    + iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE    

