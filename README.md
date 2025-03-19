# DNS Query System

## Overview

This DNS Query System project implements a simple DNS client-server model in Python. The system allows for DNS queries to be sent by a client to a server, which processes the query and responds with the relevant DNS records. The server uses a cache to store previously requested records and loads DNS records from a master file for easy access.

## Project Structure

The project is organized into the following main components:

- `client.py`: Contains the DNSClient class, responsible for handling DNS query creation, sending, and receiving responses.
- `server.py`: Contains the DNSServer, DNSCache, DNSRecord, and MasterFileLoader classes, responsible for handling incoming client queries and responding with relevant DNS records.
- `master.txt`: The master file containing DNS records (this file is read by the server).

## Program Design

### Client Design

- The client (DNSClient class) parses command-line arguments, constructs a DNS query, sends it to the server, and processes the response.
- The client waits for the server's response with a specified timeout.

### Server Design

- The server is implemented using several components:
  - **DNSServer**: Handles incoming DNS requests and sends responses.
  - **DNSCache**: An in-memory cache for storing DNS records.
  - **DNSRecord**: Represents a DNS resource record.
  - **MasterFileLoader**: Loads DNS records from the master file.
- The server supports multiple clients by using multi-threading and introduces a random delay in query processing for simulation.

### Key Data Structures

- **DNS Records**: Represented by the DNSRecord class, which stores the domain name, record type, and data.
- **Cache**: A Python dictionary in the DNSCache class that stores domain names as keys and lists of DNSRecord objects as values.
- **DNSMessages**: Messages are constructed and parsed as strings, following a custom format that includes query ID, question section, and answer/authority/additional sections.

## Known Limitations

1. The current implementation only supports A, CNAME, and NS DNS record types.
2. The error handling mechanism for malformed master files or network issues can be improved.
3. The caching mechanism is basic and does not implement Time-to-Live (TTL) or cache invalidation strategies.
4. The random delay is implemented using `time.sleep()`, which may not be precise for very short delays.
