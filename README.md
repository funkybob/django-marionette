django-marionette
=================

A RPC library for Django

How does it work?
=================

First, you define a Resource class:

    from marionette import Resource, rpc

    class MyResource(Resource):


Next, you define your RPC methods:

    class MyResource(Resource):

        @rpc
        def sum(self, a, b):
            return a + b

The ``rpc`` decorator marks the method as remotely accessible.

Then, add it to your URLs:

    url(r'^rpc/$', MyResource.as_view(), name'my-resource'),


Finally, invoke it by POSTing JSON data to that URL, with the header X-RPC-Action set to the method name.

Some helpful JavaScript for this, if you're using jQuery:

    rpc_call = function(method, data, callback) {
        $.ajax({
            type: 'POST',
            url: '{% reverse "my-resource" %}',
            data: JSON.stringify(data || {}),
            headers: {
                'X-RPC-Action': method,
                'Content-Type': 'application/json'
            },
            success: callback || null
        });
    };


    rpc_call('sum', {'a': 1, 'b': 41}, function (data) { alert(data); });

