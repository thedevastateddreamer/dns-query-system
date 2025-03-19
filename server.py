import socket
import threading
import random
import time
from datetime import datetime

# Cache for storing DNS records to improve lookup speed
class DNSCache:
    def __init__(self):
        self.cache = {}

    def get(self, domain_name):
        return self.cache.get(domain_name)

    def put(self, domain_name, records):
        self.cache[domain_name] = records

# Represents a single DNS record
class DNSRecord:
    def __init__(self, domain_name, record_type, data):
        self.domain_name = domain_name
        self.type = record_type
        self.data = data

    def __str__(self):
        return f"{self.domain_name} {self.type} {self.data}"

# Loads DNS records from a master file
class MasterFileLoader:
    def __init__(self, filename):
        self.records = {}
        self.load_records(filename)

    def load_records(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) >= 3:
                    domain_name = parts[0]
                    record_type = parts[1]
                    data = parts[2]
                    record = DNSRecord(domain_name, record_type, data)
                    if domain_name not in self.records:
                        self.records[domain_name] = []
                    self.records[domain_name].append(record)

    def get_records(self, domain_name):
        return self.records.get(domain_name)

    def get_all_records(self):
        return self.records

# Main DNS server class
class DNSServer:
    BUFFER_SIZE = 512
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

    def __init__(self, port, master_file):
        self.master_file_loader = MasterFileLoader(master_file)
        self.cache = DNSCache()
        self.random_gen = random.Random()
        self.start_server(port)

    # Start the server and listen for incoming requests
    def start_server(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.bind(("", port))
            print(f"Server listening on port {port}")
            while True:
                data, addr = server_socket.recvfrom(self.BUFFER_SIZE)
                # Handle each request in a separate thread
                threading.Thread(target=self.handle_request, args=(server_socket, data, addr)).start()

    # Process incoming DNS requests
    def handle_request(self, server_socket, data, addr):
        try:
            request = data.decode().strip()
            parts = request.split(" ")
            if len(parts) < 3:
                print("Invalid request format")
                return

            qid = int(parts[0])
            qname = parts[1]
            qtype = parts[2]

            # Simulate random processing delay
            wait_time = self.random_gen.randint(0, 4)
            self.log_message("recv", addr[1], qid, qname, qtype, wait_time)
            time.sleep(wait_time)

            records = self.get_dns_records(qname)
            response = []
            response.append(f"\nID: {qid}\n")
            response.append("\nQUESTION SECTION:\n")
            response.append(f"{qname} {qtype}")
            self.build_response(qname, qtype, records, response, True)

            response_str = "\n".join(response)
            server_socket.sendto(response_str.encode(), addr)
            self.log_message("snd", addr[1], qid, qname, qtype, -1)
        except Exception as e:
            print(e)

    # Log messages for debugging and tracking
    def log_message(self, action, client_port, qid, qname, qtype, delay):
        timestamp = datetime.now().strftime(self.DATE_FORMAT)[:-3]
        if action == "recv":
            print(f"{timestamp} {action} {client_port}: {qid} {qname} {qtype} (delay: {delay}s)")
        else:
            print(f"{timestamp} {action} {client_port}: {qid} {qname} {qtype}")

    # Retrieve DNS records from cache or master file
    def get_dns_records(self, qname):
        records = self.cache.get(qname)
        if records is None:
            records = self.master_file_loader.get_records(qname)
            if records is not None:
                self.cache.put(qname, records)
        return records if records is not None else []

    # Build the DNS response based on the query and available records
    def build_response(self, qname, qtype, records, response, first_time_added):
        exact_match_found = False
        for record in records:
            if record.type == qtype:
                if first_time_added:
                    response.append("\nANSWER SECTION:\n")
                    first_time_added = False
                response.append(str(record))
                exact_match_found = True

        if exact_match_found:
            return

        # Handle CNAME records
        for record in records:
            if record.type == "CNAME":
                if first_time_added:
                    response.append("\nANSWER SECTION:\n")
                    first_time_added = False
                response.append(str(record))
                self.build_response(record.data, qtype, self.get_dns_records(record.data), response, first_time_added)
                return

        # If no exact match or CNAME, handle referral
        self.handle_referral(qname, response)

    # Handle DNS referrals by finding the closest ancestor with NS records
    def handle_referral(self, qname, response):
        response.append("\nAUTHORITY SECTION:\n")

        qname_parts = qname.split(".")
        for i in range(len(qname_parts)):
            ancestor = ".".join(qname_parts[i:])
            if ancestor == "":
                ancestor = "."  # Handle root zone

            ns_records = self.get_dns_records(ancestor)
            if ns_records:
                for ns_record in ns_records:
                    if ns_record.type == "NS":
                        response.append(f"{ns_record}\n")

                response.append("\nADDITIONAL SECTION:\n")
                for ns_record in ns_records:
                    if ns_record.type == "NS":
                        ns_a_records = self.get_dns_records(ns_record.data)
                        if ns_a_records:
                            for ns_a_record in ns_a_records:
                                if ns_a_record.type == "A":
                                    response.append(f"{ns_a_record}\n")
                break  # Stop searching once an ancestor with NS records is found

# Main entry point
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Incorrect input")
        sys.exit(1)

    server_port = int(sys.argv[1])
    master_file = "master.txt"

    # Keep the server running, restart if it crashes
    while True:
        try:
            DNSServer(server_port, master_file)
        except Exception as e:
            print(e)
            print("Server crashed. Restarting...")
            time.sleep(5)  # 5 seconds delay before restarting the server