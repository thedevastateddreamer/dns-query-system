import socket
import random
import sys

class DNSClient:
    # Maximum size of the UDP packet
    BUFFER_SIZE = 512

    def __init__(self, server_port, qname, qtype, timeout):
        # Initialize client with server details and query parameters
        self.server_port = server_port
        self.qname = qname
        self.qtype = qtype
        self.timeout = timeout

    def send_query(self):
        try:
            # Create a UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Set the timeout
            sock.settimeout(self.timeout)

            # Generate a random query ID
            qid = random.randint(0, 65535)
            # Construct the query string
            query = f"{qid} {self.qname} {self.qtype}"
            # Send the query to the server
            sock.sendto(query.encode(), ('localhost', self.server_port))

            try:
                # Wait and receive the response
                response_packet, _ = sock.recvfrom(self.BUFFER_SIZE)
                # Decode response
                response = response_packet.decode()
                print(response)
            except socket.timeout:
                # Handle case if server doesn't respond in time
                print("Timed out waiting for response")
        except Exception as e:
            # Handling errors/exceptions
            print(f"An error occurred: {e}")
        finally:
            # Closing the socket, even if an error occurred
            sock.close()

if __name__ == "__main__":
    
    # Check if the expected command-line arguments is provided
    if len(sys.argv) != 5:
        print("Invalid input")
        sys.exit(1)

    
    server_port = int(sys.argv[1])
    qname = sys.argv[2]
    qtype = sys.argv[3]
    timeout = int(sys.argv[4])

    # Create and run the DNS client
    client = DNSClient(server_port, qname, qtype, timeout)
    client.send_query()