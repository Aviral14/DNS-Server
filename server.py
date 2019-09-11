import socketserver
import validators
from dnslib import DNSRecord, DNSHeader, DNSQuestion, RR, A, QTYPE
import tld
from dns import resolver
from settings import *
from host_file import *


class DomainResolve(socketserver.BaseRequestHandler):
    def handle(self):
        raw_data, socket = self.request
        data = DNSRecord.parse(raw_data)
        ip, query = self.resolve_domain(query=str(data.q.qname))
        if ip == "Not Found":
            response = self.send_error(query=query, q_id=data.header.id)
        else:
            response = self.generate_response(ip=ip, query=query, q_id=data.header.id)
        socket.sendto(response.pack(), self.client_address)

    def resolve_domain(self, query):
        top_domain = subdomain = domain = ""
        modified = False
        query = query[:-1]
        if not bool(validators.url(query)):
            query_modified = "http://" + query
            modified = True
        else:
            query_modified = query
        try:
            domain_obj = tld.get_tld(query_modified, as_object=True)
            domain = domain_obj.domain
            top_domain = domain_obj.tld
            subdomain = domain_obj.subdomain

        except:
            return "Not Found", query

        try:
            return records[top_domain][domain][subdomain], query
        except KeyError:
            if not modified:
                if query[:8] == "http://":
                    query_modified = query[7:]
                else:
                    query_modified = query[8:]
            else:
                query_modified = query
            try:
                resolve = resolver.Resolver()
                resolve.nameservers = [EXTERNAL_DNS_IP]
                ips = resolve.query(query_modified)
                return ips, query
            except:
                return "Not Found", query

    def send_error(self, q_id, query):
        return DNSRecord(
            DNSHeader(id=q_id, qr=1, aa=1, ra=1, rcode=3), q=DNSQuestion(query)
        )

    def generate_response(self, ip, query, q_id):
        if type(ip) == str:
            record = DNSRecord(
                DNSHeader(id=q_id, qr=1, aa=1, ra=1),
                q=DNSQuestion(query),
                a=RR(query, rdata=A(ip)),
            )
            return record
        else:
            record = DNSRecord(
                DNSHeader(id=q_id, qr=1, aa=1, ra=1),
                q=DNSQuestion(query),
                a=RR(query, rdata=A(ip[0].address)),
            )
            for ip_obj in ip[1:]:
                record.add_answer(RR(query, QTYPE.A, rdata=A(ip_obj.address)))
            return record


dns_server = socketserver.UDPServer((HOST, PORT), DomainResolve)
dns_server.serve_forever()

