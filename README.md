# Goal
Implement a gateway using the web socket module from YDU to access a CoAP resource directory, which stores the CoAP endpoints and services.
Requested functionalities:
* Device and service registration as well as discovery
* Possibility to send data to the platform over web socket connection
* Possibility to send commands from the platform to the coap devices

# Functionality
The client connector starts a connection to the platform connector via web sockets.
Then it can send data to the platform and execute incoming commands. Therefor it accesses a resource direcotry to gather the ip adress and sends a request to the device.
New devices register on the resource directory which sends the registration data to this gateway.

## CoRE Resource Directory (RD)
CoAP Server.
This project is an implementation of the [CoRE Resource Directory Standard, Version 11](https://tools.ietf.org/html/draft-ietf-core-resource-directory-11) and the [specifications of the CoAP Protocol regarding Service Registration and Discovery](https://tools.ietf.org/html/rfc7252#page-64). It will be added to the SEITS Smart Energy Platform as a microservice. Then the following processes are possible:

* Things register on the platform after multicast discovery or by already knowing the platform
* The resource directory acts as a coap client and discovers things and registers them

The project is written in Python3.4.
A thing has to know the platform or has to discover it to register itself. Therefor it has the ip adress hard coded or uses device to device or device to server discovery mechanisms. For example it can use Multicast DNS to find the platform in a local network by using IP multicast or it can find the platform in an other directory server using the CoRE Resource Directory Standard.
The platform as a resource directory exposes several API endpoints:
* ./well-known/core
* /rd-lookup
* /rd
* /rd-group

The "./well-known/core" endpoint is defined in the CoAP Protocol and should be used to provide informations about the thing. The platform as resource directory as well as the thing should provide it. It can be accessed by an unicast request or a multicast request.

The "/rd-lookup" endpoint is be used by the an interested client to discover and search for things within the platform.

The "/rd" endpoint is the main endpoint and is used by the thing itself on the platform using different parameters.

## Web Socket connector
The Web Socket Connector builds the connection the platform connector. It gets commands and sends them to the CoAP Executer, registers, updates, disconnects and removes devices, based on the Pinger and the RD. Furthermore it is used to send data from the CoAP Observer to the platform.

## Executer
CoAP Client
The Executer module contains an CoAP executor that recieves commands of the Web Socket Connector and executes them by looking up for the requested device and perfoming a CoAP request.

## Observer
CoAP Client
The observer gets the data of all connected devices by looking up in the RD and performing frequently GET requests. Next it sends the data via the Web Socket Connector to the Platform Connector.

## Pinger
CoAP Client
The pinger checks frequently if the registered devices in the RD are online or offline. If a device does not respond to a simple empty CoAP GET Ping it is considered as disconnected but not as removed. Within in the RD it gets the status 0 for disconnected and on the platform it gets disconnected.

# Requirements
Add the client connector module in the working directory.

```shell
git clone https://gitlab.wifa.uni-leipzig.de/fg-seits/connector-client
```

# Usage
## Requirements
```
```
Run the main script
```shell
python3 main.py
```

- device remove request -> delete from platform
- device not pingable -> disconnect
- core link format for registration supported

# Directory Structure
* /platform: contains the CoAP server that will be added to the platform
** main.py:
** /server_resources: contains classes that are used by the CoAP server to provide the API endpoints
* /thing: contains the CoAP client that will be used by the thing to register itself, presumed that the thing knows the ip address of the platform, for testing purposes
* /client: contains the CoAP client that will be used by an interested client to discover things in the platform, not important because the platform is the interested client at the same time, for testing purposes

# Mappping to IoT Repository
* device id -> id
* device name -> ep parameter
* device type -> et parameter -> created on platform per hand or created per API 

How to add a CoAP Device to the platform:
1. Create Device Type
2. Add services: 
- Service URL: relative path of the resource of the COAP Server of the device + used CoAP Method  
- Input Parameter: API Keys 
- Output Parameter: e.g. JSON structure of data 
- Protocol: Standard 

Problems: 
1. multiple resources on one device 
- but unique service url with no mapping is needed -> Path 

2. multiple methods on one resources
- path is not unique, but service should only have one functionality because of different data structures  

-> other structure ? not based on services, maybe on resources = path
-> then services like read, update, ..
-> problem: resource light can have multiple resources eg. /group/light, /light/1 ...

Unique -> Path + Method -> "GET /api/1/" as service url 
-> has to be parsed to get path 
-> RD is not very powerful if method and path are stored on platform 

Flow:
- the gateway stores the device on device registration/discovery and creates an ID 
- then it registers it on the platform with the ID and metadata if it is new 
- a device type with multiple services has to be created on platform side 
- the device instance has to be connectected with this type 
- then the platform can recieve data via services or can send commands via services
- for commands the mapping to a unique device is done via the generated ID which will be resolved to an URI scheme in the gateway
- the path of the resource is the service url which has to be added on platform side on service creation

Because of multiple standards there is no way to map APIs, resource types and data structures without updating the gateway or the device implementation, which is not good.

Identification of devices:
- static IP addresses could be used 
- but dynamic IP addresses not
- therefor the gateway generates an ID and stores it in a database
- CoRE RD defines the 'endpoint name' parameter which should be unique in a given domain, but device does not know anything about others endpoint names in the domain
- if IP address changes after reboot, it depends on the registraton process
-- if the device registers again, the gateway can match on the endpoint name if unique and update the IP 
-- if the device is passive, it will be added as a new device, because you dont get the endpoint name on discovery, other possibility is usage of mDNS and hostnames, which are unique in a local network 

Registration and Discovery of devices:
1. Active registration of device:
1.1 CoRE RD specification 

2. Discovery by gateway:
2.1 Listen on DNS queries 
2.2 Discovery with multicast CoAP 


# TODO:
- endpoint register -> DONE
- group register
- endpoint lookup -> DONE
- resource lookup
- group lookup
- domain lookup
- simple registration
- update
- removal
- well known resource -> DONE
- patch
- an californium orientieren bei resourcen
- ORM

