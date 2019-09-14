# DNS-Server
A DNS Server in python using dnslib

The DNS Server maintains and processes the domain names and their associated ip addresses.Upon receiving a name resolution query the DNS Server translates the given domain name into its respective IP address and sends it back to the user.If the DNS Server is unable to find the domain name in it's records, it redirects the query to a standard DNS Server.

This Project also includes a Registration Portal made using django which enables the user to register their own domain names in the DNS Server.


# Setup:
The host_file contains the DNS records and the server.py has the actual code for the server.

Run server.py file with admin privileges (since it contains binding of Port 53) to launch the server.

To run the portal-<br>
Change directory to Registration_portal and run the command-<br>
pyhton3 manage.py runserver

