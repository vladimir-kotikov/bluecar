import types
import logging
from functools import wraps

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

class DBusProxy(object):

    def __init__(self, bus, object_path, interface, service="org.bluez"):
        self.__bus = bus
        self.__peer = bus[service][object_path]
        self.__proxy = None
        self._interface = interface

        # LOG.info("Created proxy for %s on %s", interface, object_path)
        print("Created proxy for %s on %s" % (interface, object_path))

    @property
    async def _proxy(self):
        if self.__proxy is None:
            self.__proxy = await self.__peer.get_async_interface(self._interface)

        return self.__proxy

    async def invoke_method(self, method_name, *args, **kwargs):
        # LOG.info("Attempting to invoke method %s with %s, %s", method_name, args, kwargs)
        print("Attempting to invoke method %s with %s, %s" % (method_name, args, kwargs))
        proxy = await self._proxy
        method = getattr(proxy, method_name)
        print("[D] Method %s" % method)
        result = await method(*args, **kwargs)
        print("[D] Result %s" % result)
        return result

    async def get_property(self, prop_name):
        proxy = await self._proxy
        return await getattr(proxy, prop_name)

def proxy_method(method_name):
    """factory that generates decorator for proxy method with given name"""

    if isinstance(method_name, types.FunctionType):
        raise Exception("'proxy_method' decorator can be used only as decorator factory")

    def decorator(method):
        """Decorates function so it calls appropriate proxy method with provided arguments"""

        @wraps(method)
        async def wrapper(self, *args, **kwargs):
            """Wraps method to call dbus proxy method instead"""
            await method(self, *args, **kwargs)
            return await self.invoke_method(method_name, *args, **kwargs)

        return wrapper

    return decorator


def proxy_property(property_name):
    """factory that generates decorator for proxy method with given name"""

    if isinstance(property_name, types.FunctionType):
        raise Exception("'proxy_property' decorator can be used only as decorator factory")

    def decorator(propgetter):
        """Decorates function so it calls appropriate proxy method with provided arguments"""

        async def wrapper(self):
            """Wraps method to call dbus proxy method instead"""
            return await self.get_property(property_name)

        return wrapper

    return decorator
