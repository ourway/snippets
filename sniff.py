from scapy.all import sniff, TCP, Raw, IP, conf, ARP, DNS

conf.promisc = 1


def get_http(sniffed):
    http = {}
    for pkt in sniffed:
        if pkt.haslayer(TCP) and (pkt.getlayer(TCP).dport == 80 or
                                  pkt.getlayer(TCP).dport == 8080 or
                                  pkt.getlayer(TCP).sport == 8080 or
                                  pkt.getlayer(TCP).sport == 80) and pkt.haslayer(Raw):
            addr_list = [pkt.getlayer(IP).dst, pkt.getlayer(IP).src]
            address = ' - '.join(sorted(addr_list))
            http.setdefault(address, []).append(str(pkt[TCP].payload))
    return http


def get_arp(sniffed):
    for pkt in sniffed:
        if pkt.haslayer(ARP):
            pkt.display()


def get_dns(sniffed):
    for pkt in sniffed:
        if pkt.haslayer(DNS):
            addr_list = [pkt.getlayer(IP).dst, pkt.getlayer(IP).src]
            address = ' - '.join(sorted(addr_list))
            dns.setdefault(address, []).append(str(pkt[TCP].payload))
    return dns


while True:
    sn = sniff(count=10)
    http = get_http(sn)
    #get_arp(sn)
    for address in http:
        # with open(address, 'a+') as fd:
        with open('sniff', 'a+') as fd:
            fd.write('\n'.join(http[address]))
