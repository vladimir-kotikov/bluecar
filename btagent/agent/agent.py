#!/usr/bin/python

from __future__ import absolute_import, print_function, unicode_literals

from optparse import OptionParser
import dbus
import dbus.service
import dbus.mainloop.glib
from dbus.exceptions import DBusException

try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject

from bluezutils import find_adapter, ADAPTER_INTERFACE, DEVICE_INTERFACE

# 110d is A2DP profile. See https://www.bluetooth.com/specifications/assigned-numbers/service-discovery
# for other IDs
ALLOWED_SERVICES = ("110d",)

BUS_NAME = 'org.bluez'
AGENT_INTERFACE = 'org.bluez.Agent1'
AGENT_PATH = "/bluecar/authagent"
PASSKEY = 123456


class Rejected(dbus.DBusException):
    """Represents Agent authorization rejection"""
    _dbus_error_name = "org.bluez.Error.Rejected"


class Agent(dbus.service.Object):
    """Represents bluez authorization Agent implementation"""

    def __set_trusted(self, device_path):
        proxy = self.connection.get_object("org.bluez", device_path)
        props = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")
        props.Set(DEVICE_INTERFACE, "Trusted", True)

    @dbus.service.method(AGENT_INTERFACE, in_signature="", out_signature="")
    def Release(self):
        print("Release")

    @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="s")
    def RequestPinCode(self, device):
        print("RequestPinCode (%s)" % (device))
        return str(PASSKEY)

    @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="u")
    def RequestPasskey(self, device_path):
        print("RequestPasskey (%s)" % (device_path))
        return dbus.UInt32(PASSKEY)

    @dbus.service.method(AGENT_INTERFACE, in_signature="ouq", out_signature="")
    def DisplayPasskey(self, device_path, passkey, entered):
        print("DisplayPasskey (%s, %06u entered %u)" % (device_path, passkey, entered))

    @dbus.service.method(AGENT_INTERFACE, in_signature="os", out_signature="")
    def DisplayPinCode(self, device_path, pincode):
        print("DisplayPinCode (%s, %s)" % (device_path, pincode))

    @dbus.service.method(AGENT_INTERFACE, in_signature="ou", out_signature="")
    def RequestConfirmation(self, device_path, passkey):
        print("RequestConfirmation (%s, %06d)" % (device_path, passkey))
        if PASSKEY == passkey:
            self.__set_trusted(device_path)
            return

        raise Rejected("Passkey doesn't match")

    @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="")
    def RequestAuthorization(self, device_path):
        print("RequestAuthorization (%s)" % (device_path))

    @dbus.service.method(AGENT_INTERFACE, in_signature="os", out_signature="")
    def AuthorizeService(self, device, uuid):
        print("AuthorizeService (%s, %s)" % (device, uuid))

        service_id = uuid[:3]
        if service_id.lower() in ALLOWED_SERVICES:
            print("Service is allowed, adding device to trusted")
            self.__set_trusted(device)

    @dbus.service.method(AGENT_INTERFACE, in_signature="", out_signature="")
    def Cancel(self):
        print("Cancel")


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    parser = OptionParser()
    parser.add_option("-c", "--capability", action="store",
                   type="string", dest="capability")

    options, _ = parser.parse_args()
    capability = options.capability or "KeyboardDisplay"

    BUS = None
    while BUS == None:
        try:
            print("Attepting to connect to system bus...")
            BUS = dbus.SystemBus()
        except DBusException as ex:
            print("Failed to connect to dbus %s: %s. %s" %
                  (ex.get_dbus_name(), ex._dbus_error_name, ex.message))

    # Create and register agent implementation
    print("Registering Agent with capability '%s' ..." % (capability,))
    Agent(BUS, AGENT_PATH)

    obj = BUS.get_object(BUS_NAME, "/org/bluez")
    manager = dbus.Interface(obj, "org.bluez.AgentManager1")
    manager.RegisterAgent(AGENT_PATH, capability)
    manager.RequestDefaultAgent(AGENT_PATH)
    print("Agent registered")

    print("Ensuring that adapter is discoverable/pairable...")
    try:
        props = dbus.Interface(find_adapter().proxy_object,
                               "org.freedesktop.DBus.Properties")

        props.Set(ADAPTER_INTERFACE, "Discoverable", True)
        props.Set(ADAPTER_INTERFACE, "Pairable", True)
        props.Set(ADAPTER_INTERFACE, "DiscoverableTimeout", dbus.UInt32(0))
        props.Set(ADAPTER_INTERFACE, "PairableTimeout", dbus.UInt32(0))
        print("Adapter is pairable/discoverable now")
    except:
        print("Failed to make adapter discoverable/pairable")

    GObject.MainLoop().run()
