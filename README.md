# OpenTelemetry_Example
Test OpenTelemetry trace on python socketserver 
- test_tracer.py
  on python environment with install opentelemetry-api, opentelemetry-sdk.
  I try to trace socket server request event. So, I wrote the sample code.

  execute: python test_tracer.py <br>
  output:<br>
  <code>
  start process
  will call test1()
  in test1 function
  test....
  leave test1 function
  end call test1()
  in TestSocketServer __init__
  leave TestSocketServer __init__
  start server forever
  </code>

- test_tracer_client.py
  used to send any event to server and with see the request

  execute: python test_tracer_client.py <br>
  output:<br>
  client site will see: <br>
  <code>
  b'Server received request isAlive'
  </code>
  server site will see: <br>
  <code>
  in MySocketHandle handle
  request_string : 	 b'isAlive'
  leave MySocketHandle handle
  </code>

Finally. I hope to see the trace information on elastic apm dashboard.
On the Elastic APM dashboard, 
we can see all the trace information at test1 function.
![截圖 2023-09-22 上午10 43 46](https://github.com/mingchanghou/OpenTelemetry_Example/assets/5379949/12c55943-a481-41f2-907d-dcb875d8ac08)
But at the handle function of socketserver BaseRequestHandle, I can't see any trace information.
![截圖 2023-09-22 上午10 44 06](https://github.com/mingchanghou/OpenTelemetry_Example/assets/5379949/30062fc0-b89f-491f-bdcd-dc6fb2da0786)

