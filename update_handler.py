import socketserver
import tld
import json
from settings import HOST, TCP_PORT


class TCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip().decode()
        domain, ip = self.data.split(",")
        self.update_record(domain, ip)

    def update_record(self, domain, ip):
        with open("host_file.json") as file_obj:
            records = json.loads(file_obj.read())
        domain_modified = "http://" + domain
        domain_obj = tld.get_tld(domain_modified, as_object=True)
        second_domain = domain_obj.domain
        top_domain = domain_obj.tld
        subdomain = domain_obj.subdomain

        if records.get(top_domain, ""):
            if not second_domain in list(records[top_domain].keys()):
                records[top_domain].update({second_domain: {subdomain: ip}})
                with open("host_file.json", "w") as host_file:
                    json.dump(records, host_file)
            else:
                if not subdomain in list(records[top_domain][second_domain].keys()):
                    records[top_domain][second_domain].update({subdomain: ip})
                    with open("host_file.json", "w") as host_file:
                        json.dump(records, host_file)
        else:
            records.update({top_domain: {second_domain: {subdomain: ip}}})
            with open("host_file.json", "w") as host_file:
                json.dump(records, host_file)


with socketserver.TCPServer((HOST, TCP_PORT), TCPRequestHandler) as server:
    server.serve_forever()
