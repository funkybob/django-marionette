django-marionette
=================

A RPC library for Django

How does it work?
=================

Marionette provides a Mixin for Class Based Views.  Its ``dispatch`` method
intercepts all requests, and if it's a POST and has a X-RPC-Action header, will
attempt to invoke a method on the class with the matching name.

Quick Start
===========

First, you define a View

    from marionette import RPCMixin

    class MathView(RPCMixin, View):

As a shortcut, there is a pre-mixed view RPCView.


Next, you define your RPC methods:

    class MathView(RPCView):

        @rpc
        def sum(self, a, b):
            return a + b

The ``rpc`` decorator marks the method as remotely accessible.

Then, add it to your URLs:

    url(r'^rpc/$', MathView.as_view(), name'rpc-view'),

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

