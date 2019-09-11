import socketserver
import validators
from dnslib import DNSRecord, DNSHeader, DNSQuestion, RR, A, QTYPE
import tld
from dns import resolver
from settings import *
from host_file import *


class DomainResolve(socketserver.BaseRequestHandler):
    def handle(self):
        data, socket = self.request
        d = DNSRecord.parse(data)
        ip, domain = self.resolve_domain(query=str(d.q.qname))
        response = self.generate_response(ip=ip, domain=domain, q_id=d.header.id)
        socket.sendto(response.pack(), self.client_address)

    def resolve_domain(self, query):
        top_domain = subdomain = domain = ""
        query = query[:-1]
        if bool(validators.url(query)):
            domain_obj = tld.get_tld(f"{query}"[:-1], as_object=True)
            domain = domain_obj.domain
            top_domain = domain_obj.tld
            subdomain = domain_obj.subdomain
        else:
            name_list = query.split(".")
            if len(name_list) == 2:
                domain, top_domain = name_list
            if len(name_list) == 3:
                subdomain, domain, top_domain = name_list
        try:
            return records[top_domain][domain][subdomain], query
        except KeyError:
            resolve = resolver.Resolver()
            resolve.nameservers = ["8.8.8.8"]
            ips = resolve.query(query)
            return ips, query

    def direct(self):
        pass

    def generate_response(self, ip, domain, q_id):
        if type(ip) == str:
            a = DNSRecord(
                DNSHeader(id=q_id, qr=1, aa=1, ra=1),
                q=DNSQuestion(domain),
                a=RR(domain, rdata=A(ip)),
            )
            print(str(a))
            return a
        else:
            record = DNSRecord(
                DNSHeader(id=q_id, qr=1, aa=1, ra=1),
                q=DNSQuestion(domain),
                a=RR(domain, rdata=A(ip[0].address)),
            )
            print(str(record))
            for ip_addr in ip[1:]:
                record.add_answer(RR(domain, QTYPE.A, rdata=A(ip_addr.address)))
            return record


dns_server = socketserver.UDPServer((HOST, PORT), DomainResolve)
dns_server.serve_forever()

