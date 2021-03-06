<!-- Reference Links -->
[1]:	https://usp-data-models.broadband-forum.org/ "Device Data Model"
[2]: https://www.broadband-forum.org/technical/download/TR-069.pdf	"TR-069 Amendment 6	CPE WAN Management Protocol"
[3]:	https://www.broadband-forum.org/technical/download/TR-106_Amendment-8.pdf "TR-106 Amendment 8	Data Model Template for CWMP Endpoints and USP Agents"
[4]:	https://tools.ietf.org/html/rfc7228 "RFC 7228	Terminology for Constrained-Node Networks"
[5]:	https://tools.ietf.org/html/rfc2136	"RFC 2136 Dynamic Updates in the Domain Name System"
[6]:	https://tools.ietf.org/html/rfc3007	"RFC 3007 Secure Domain Name System Dynamic Update"
[7]:	https://tools.ietf.org/html/rfc6763	"RFC 6763 DNS-Based Service Discovery"
[8]:	https://tools.ietf.org/html/rfc6762	"RFC 6762 Multicast DNS"
[9]:	https://tools.ietf.org/html/rfc7252	"RFC 7252 The Constrained Application Protocol (CoAP)"
[10]:	https://tools.ietf.org/html/rfc7390	"RFC 7390 Group Communication for the Constrained Application Protocol (CoAP)"
[11]:	https://tools.ietf.org/html/rfc4033	"RFC 4033 DNS Security Introduction and Requirements"
[12]:	https://developers.google.com/protocol-buffers/docs/proto3 "Protocol Buffers v3	Protocol Buffers Mechanism for Serializing Structured Data Version 3"
[13]: https://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries "IEEE Registration Authority"
[14]: https://tools.ietf.org/html/rfc4122 "RFC 4122 A Universally Unique IDentifier (UUID) URN Namespace"
[15]: https://tools.ietf.org/html/rfc5280 "RFC 5290 Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile"
[16]: https://tools.ietf.org/html/rfc6818 "RFC 6818 Updates to the Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile"
[17]: https://tools.ietf.org/html/rfc2234 "RFC 2234 Augmented BNF for Syntax Specifications: ABNF"
[18]: https://tools.ietf.org/html/rfc3986 "RFC 3986 Uniform Resource Identifier (URI): Generic Syntax"
[19]: https://tools.ietf.org/html/rfc2141 "RFC 2141 URN Syntax"
[20]: https://tools.ietf.org/html/rfc6455 "RFC 6455 The WebSocket Protocol"
[21]: https://stomp.github.io/stomp-specification-1.2.html "Simple Text Oriented Message Protocol"
[22]: https://tools.ietf.org/html/rfc5246 "The Transport Layer Security (TLS) Protocol Version 1.2"
[23]: https://tools.ietf.org/html/rfc6347 "Datagram Transport Layer Security Version 1.2"
[Conventions]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs to Indicate Requirement Levels"

# Message Transfer Protocols

USP messages are sent between Endpoints over one or more Message Transfer Protocols.

Note: Message Transfer Protocol was a term adopted to avoid confusion with the term "Transport", which is often overloaded to include both application layer (e.g. CoAP) and the actual OSI Transport layer (e.g. UDP). Throughout this document, Message Transfer Protocol (MTP) refers to application layer transport.

The requirements for each individual Message Transfer Protocol is covered in a section of this document. This version of the specification includes definitions for:

*	The [Constrained Application Protocol (CoAP)](./coap/)
* [WebSockets](./websocket/)
* The [Simple Text-Oriented Messaging Protocol](./stomp/)
* [MQ Telemetry Transport (MQTT)](./mqtt)

## Supporting Multiple MTPs

Agents and Controllers may support more than one MTP. When an Agent supports multiple MTPs, the Agent may be configured with parameters for reaching a particular Controller across more than one MTP. When an Agent needs to send a Notification to such a Controller, the Agent can be designed (or possibly configured) to select a particular MTP, to try sending the Notification to the Controller on all MTPs simultaneously, or to try MTPs sequentially. USP has been designed to allow Endpoints to recognize when they receive a duplicate Message and to discard any duplicates. Endpoints will always send responses on the same MTP where the Message was received.

## Securing MTPs

<a id="securing_mtps" />


This specification places the following requirement for encrypting MTP headers and payloads on USP implementations that are intended to be used in environments where USP Messages will be transported across the Internet:

**R-MTP.0** – The Message Transfer Protocol MUST use secure transport when USP Messages cross inter-network boundaries.

For example, it may not be necessary to use MTP layer security when within an end-user’s local area network (LAN). It is necessary to secure transport to and from the Internet, however. If the device implementer can reasonably expect Messages to be transported across the Internet when the device is deployed, then the implementer needs to ensure the device supports encryption of all MTP protocols.

MTPs that operate over UDP will be expected to implement, at least, DTLS 1.2 as defined in [RFC 6347][23].

MTPs that operate over TCP will be expected to implement, at least, TLS 1.2 as defined in [RFC 5246][22].

Specific requirements for implementing these are provided in the individual MTP sections.

**R-MTP.1** – When TLS or DTLS is used to secure an MTP, an Agent MUST require the MTP peer to provide an X.509 certificate.

**R-MTP.2** - An Agent capable of obtaining absolute time SHOULD wait until it has accurate absolute time before establishing TLS or DTLS encryption to secure MTP communication.  If an Agent for any reason is unable to obtain absolute time, it can establish TLS or DTLS without waiting for accurate absolute time. If an Agent chooses to establish TLS or DTLS before it has accurate absolute time (or if it does not support absolute time), it MUST ignore those components of the received X.509 certificate that involve absolute time, e.g. not-valid-before and not-valid-after certificate restrictions.

**R-MTP.3** - An Agent that has obtained an accurate absolute time MUST validate those components of the received X.509 certificate that involve absolute time.

**R-MTP.4** - When an Agent receives an X.509 certificate while establishing TLS or DTLS encryption of the MTP, the Agent MUST execute logic that achieves the same results as in the decision flow from Figures [MTP.1](#figure-MTP1).

<img src="validate-cert.png" />

Figure MTP.1 – Receiving a X.509 Certificate

<a id='figure-MTP1'/>

## Brokered USP Record Errors

<a id='brokered-usp-record-errors' />

MTPs that allow connectivity directly between Endpoints tear down the connection when encountering a USP Record error or other failure caused by the USP Record. This allows such a problem to be signaled to the other Endpoint. MTP protocols where Endpoints connect to a session broker do not tear down the connections to the session broker when encountering USP Record errors. To notify an Endpoint when a failed USP Record was sent, the receiving Endpoint replies with a simple error message.

These error messages are indicated using content type `application/vnd.bbf.usp.error`. The following error codes (in the range 7100-7199) are defined to allow the error to be more specifically indicated. Requirements for communicating USP Record errors using this content type and these error codes are included in the definitions of brokered MTPs.

| Code | Name | Description
| :----- | :------------ | :---------------------- |
| `7100` | Record could not be parsed	| This error indicates the received USP Record could not be parsed. |
| `7101` | Secure session required | This error indicates USP layer [Secure Message Exchange](/specification/e2e-message-exchange/) is required.|
| `7102` | Secure session not supported | This error indicates USP layer [Secure Message Exchange](/specification/e2e-message-exchange/) was indicated in the received Record but is not supported by the receiving Endpoint. |
| `7103` | Segmentation and reassembly not supported | This error indicates segmentation and reassembly was indicated in the received Record but is not supported by the receiving Endpoint. |
| `7104` | 	Invalid Record value | This error indicates the value of at least one Record field was invalid. |
