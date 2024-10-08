from dns.edns import ECSOption
from dns.message import from_wire
from dnslib import *
from dnslib.server import DNSServer, BaseResolver, DNSLogger


class IPResolver(BaseResolver):
    def resolve(self, request, handler):
        reply = request.reply()
        qname = request.q.qname
        qtype = request.q.qtype

        src_addr = handler.client_address[0]
        src_port = handler.client_address[1]

        # Handle IPv4-mapped IPv6 addresses
        if src_addr.startswith('::ffff:'):
            src_addr = src_addr[7:]

        try:
            if qtype == QTYPE.TXT:
                # Client IP address and port
                txt_records = [f"FROM {src_addr}:{src_port}"]

                # ECS option
                parsed_request = from_wire(handler.request[0])
                txt_records += [f"ECS {ecs.address}/{ecs.srclen}" for ecs in parsed_request.options if isinstance(ecs, ECSOption)]

                # Raw request
                txt_records += [parsed_request.to_text().replace('\n', '|')[:255]]

                for record in txt_records:
                    reply.add_answer(RR(qname, QTYPE.TXT, rdata=TXT(record)))
            elif qtype == QTYPE.A:
                reply.add_answer(RR(qname, QTYPE.A, rdata=A(src_addr)))
            elif qtype == QTYPE.AAAA:
                # Handle conversion of IPv4 to IPv4-mapped IPv6 address
                if '.' in src_addr:
                    v4_octets = map(int, src_addr.split('.'))
                    src_addr = "::ffff:{:02x}{:02x}:{:02x}{:02x}".format(*v4_octets)
                reply.add_answer(RR(qname, QTYPE.AAAA, rdata=AAAA(src_addr)))
        except:
            reply.header.rcode = RCODE.NXDOMAIN

        return reply


if __name__ == '__main__':
    resolver = IPResolver()
    logger = DNSLogger("request,reply,error", False)

    server = DNSServer(resolver, port=53, address="::", logger=logger, tcp=True)
    server.start_thread()
    server = DNSServer(resolver, port=53, address="::", logger=logger, tcp=False)
    server.start()
