=======
asyhttp
=======

.. image:: https://badge.fury.io/py/asyhttp.svg
   :target: https://pypi.org/project/asyhttp
   :alt: Latest PyPI package version

This is asyhttp, a simple module to perform asynchronous HTTP requests using asyncio and aiohttp.

It provides a trivial way to perform a set of async HTTP requests.

Features
--------
- Proxy support
- Custom headers 
- Allow redirects 
- Use TLS

How to use loop()
-----------------
asyhttp loop() accepts some ``args``

- ``urls`` a set of dictionaries, each dict represent an HTTP request.
- ``proxy`` (str) proxt URL, str (optional).
- ``process_out`` a user defined function that can be used to process the response of each HTTP request.
  It will be called by the async function that perform each HTTP request, as soon as the response arrive (optional). 
- ``redirects`` (bool) – If set to True, follow redirects. False by default (optional).
- ``verify_tls`` (bool) True for check TLS cert validation, False by default (optional). 

Getting started
---------------

.. code:: python

	from asyhttp import loop

	requests = [	{'url':'http://exam.ple/page.html', 'method':'GET'},
			{'url':'http://exam.ple/page.html', 'method':'POST', 'body' : 'blabla'}
	] 
	loop(urls=requests)

Use cases
---------
asyhttp loop can be useful to write quick bruteforces against vulnerable systems
or as a core for tools like dirfister.

An early version of this code comes from https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html

Docs
----

Process HTTP responses
^^^^^^^^^^^^^^^^^^^^^^
By default, asyhttp loop print on stdout HTTP status code and reason for each response received.
You can override its default behavior writing custom code to process the response your HTTP requests.
Your code has to be written in a function and passed to loop as a kwarg called process_out.
That function will be called by the async function that perform each of your HTTP requests,
as soon as the response arrive. 

In your custom code you can process:
- url: url of the HTTP request
- return_code 
- reason
- resp_body
- user_data

Example
"""""""

.. code:: 

	pip install asyhttp

.. code:: python

	from asyhttp import loop
	requests = [{'url':'http://exam.ple/page.html', 'method':'GET'}]
	loop(urls=requests)

Example
"""""""
.. code:: python

	from asyhttp import loop

	def process_output(url,return_code,reason,resp_body,user_data):
		if return_code == 200:
			sys.stdout.write("url")

	requests = [{'url':'http://exam.ple/page.html', 'method':'GET'}]
	loop(urls=requests,process_out=process_output)

asyhttp loop's ``args``
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- ``urls``
- ``process_out``
- ``proxy``
- ``verify_tls``
- ``redirects``

Supported HTTP methods
^^^^^^^^^^^^^^^^^^^^^^
- GET
- POST
- HEAD

HTTP requests format
^^^^^^^^^^^^^^^^^^^^

.. code:: python

	{'method':'GET', 'url':'http://exam.ple/page.html'}
	{'method':'POST', 'url':'http://exam.ple/page.html','body':'blablabl=balbal'}
	{'url':'http://exam.ple/page.html', 'method':'GET', 'headers' : 'X-Custom-Header:YEAH'}

Proxy support
^^^^^^^^^^^^^

.. code:: python

	loop(urls=url_dict_list,proxy="http://127.0.0.1:8080")

Custom headers
^^^^^^^^^^^^^^
To add HTTP headers to a request, pass them as a dict.

.. code:: python

	{'url':'http://exam.ple/page.html', 'method':'GET', 'headers' : {'User-agent':'YEAH'}}

Allow redirects
^^^^^^^^^^^^^^^
False by default

.. code:: python

	loop(urls=requests,process_out=process_response,redirects=True)

Verify TLS
^^^^^^^^^^
False by default

.. code:: python

	loop(urls=requests,process_out=process_response,verify_tls=True)
