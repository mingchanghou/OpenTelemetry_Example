# sample code to test opentelemetry trace in python socketserver BaseRequestHandler

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
import platform
import socketserver, threading, sys

node_name = platform.node()


resource = Resource(attributes={
                "host.name": node_name,
                "service.namespace": 'TEST_PYTHON_SOCKET_{}'.format(node_name),
                "service.name": 'TEST_SOCKET_{}'.format(node_name),
                "service.version": '1.0',
                "sls.otel.project": "",
                "sls.otel.akid": "",
                "sls.otel.aksecret": "",
                "sls.otel.instanceid": "" 
            })

trace.set_tracer_provider(TracerProvider(resource=resource))
# using elastic apm to receive trace information
otlp_exporter = OTLPSpanExporter(endpoint="http://10.60.93.81:8200")
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))
tracer = trace.get_tracer(__name__)

# this sample can see the trace information on elastic apm
def test1():
    with tracer.start_as_current_span('test1 span') as span:
        print('in test1 function')
        span.set_attribute('parma', 'test_parent')
        with tracer.start_as_current_span('print span') as child_span:
            print('test....')
            child_span.set_attribute('param', 'test...')
        print('leave test1 function')


# this case can't see the trace information on elastic apm
class MySocketHandle(socketserver.BaseRequestHandler):
    def handle(self):
        print('in MySocketHandle handle')
        request_string = b''
        with tracer.start_as_current_span('MySocketHandle parent span') as parent:
            parent.set_attribute('param', 'MySocketHandle parent')
            with tracer.start_as_current_span('MySocketHandle recv msg span') as child:
                while True:
                    recv_msg = self.request.recv(4096)
                    request_string += recv_msg
                    if len(recv_msg) < 4096:
                        break
                self.request.send(b'Server received request '+request_string)
                print('request_string : \t', request_string)
                child.set_attribute('param', str(request_string))
        print('leave MySocketHandle handle')


class TestSocketServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True
    def __init__(self, server_address, request_handle_class):
        print('in TestSocketServer __init__')
        with tracer.start_as_current_span('TestSocketServer span') as parent:
            parent.set_attribute('param', 'TestSocketServer span')
            socketserver.TCPServer.__init__(self, server_address, request_handle_class)
        print('leave TestSocketServer __init__')


if __name__=='__main__':
    print('start process')
    print('will call test1()')
    test1()
    print('end call test1()')
    server = TestSocketServer(('',10500), MySocketHandle)
    try:
        print('start server forever')
        server.serve_forever()
        print('over serve_forever()')
    except KeyboardInterrupt as e:
        print(repr(e))
        sys.exit(0)
