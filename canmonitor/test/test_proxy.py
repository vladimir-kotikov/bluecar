import asyncio
from unittest.mock import Mock

import pytest
import pytest_asyncio
from dbus.proxy import proxy_method, proxy_property

class FakeProxy(Mock):
    @proxy_method("Super")
    def super_method(self, *args, **kwargs): pass

    @property
    @proxy_property("Super")
    def super_property(self): return "Awesome"


class AsyncProxy():
    @proxy_method("Async")
    async def async_method(self): pass
    @property
    @proxy_property("Async")
    async def async_prop(self): pass
    async def invoke_method(self, method_name): pass
    async def get_property(self, prop_name): return "Awesome"

@pytest.fixture
def proxy():
    return FakeProxy()

@pytest.fixture
def async_proxy():
    return AsyncProxy()

def test_method_decorator(proxy):
    proxy.super_method()
    proxy.invoke_method.assert_called_once_with("Super")

    proxy.super_method("foo", bar="baz")
    proxy.invoke_method.assert_called_with("Super", "foo", bar="baz")

def test_property_decorator(proxy):
    val = proxy.super_property
    proxy.get_property.assert_called_once_with("Super")

def test_incorrect_usage():
    with pytest.raises(Exception):
        class BadProxy:
            @proxy_method
            def bad_usage(self): pass

    with pytest.raises(Exception):
        class BadProxy2:
            @proxy_property
            def bad_usage(self): pass

@pytest.mark.asyncio
async def test_async_call(async_proxy):
    get = async_proxy.async_prop
    assert asyncio.iscoroutine(get)

    call = async_proxy.async_method()
    assert asyncio.iscoroutine(call)

    await call

    val = await get
    assert val == "Awesome"
