#!/usr/bin/python

from __future__ import absolute_import, print_function, unicode_literals

from optparse import OptionParser
import logging
import time
import dbus
import dbus.service
import dbus.mainloop.glib
from dbus.exceptions import DBusException
from bluezutils import find_adapter, ADAPTER_INTERFACE, DEVICE_INTERFACE

log_formatter = logging.Formatter(
    "%(asctime)s %(levelname).1s: [btagent] %(name)s: %(message)s")
log_handler = logging.StreamHandler()
log_handler.formatter = log_formatter

LOG = logging.getLogger("agent")
LOG.setLevel(logging.DEBUG)
LOG.addHandler(log_handler)

try:
    from gi.repository import GObject
    LOG.debug("Imported GObject from gi.repository")
except ImportError:
    import gobject as GObject
    LOG.debug("Imported GObject from gobject")

# 110d is A2DP profile. See https://www.bluetooth.com/specifications/assigned-numbers/service-discovery
# for other IDs
ALLOWED_SERVICES = ("110d", "110e")

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
        LOG.info("Reveived Release, ignoring...")

    @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="s")
    def RequestPinCode(self, device):
        LOG.info("Received RequestPinCode (%s)", device)
        return str(PASSKEY)

    @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="u")
    def RequestPasskey(self, device_path):
        LOG.info("Received RequestPasskey (%s)", device_path)
        return dbus.UInt32(PASSKEY)

    @dbus.service.method(AGENT_INTERFACE, in_signature="ouq", out_signature="")
    def DisplayPasskey(self, device_path, passkey, entered):
        LOG.info("Received DisplayPasskey (%s, %06u entered %u)",
                 device_path, passkey, entered)

    @dbus.service.method(AGENT_INTERFACE, in_signature="os", out_signature="")
    def DisplayPinCode(self, device_path, pincode):
        LOG.info("Received DisplayPinCode (%s, %s)", device_path, pincode)

    @dbus.service.method(AGENT_INTERFACE, in_signature="ou", out_signature="")
    def RequestConfirmation(self, device_path, passkey):
        LOG.info("Received RequestConfirmation (%s, %06d)",
                 device_path, passkey)
        if PASSKEY == passkey:
            LOG.info("Passkeys match")
            self.__set_trusted(device_path)
            return

        LOG.warn("Passkeys don't match, returning error...")
        raise Rejected("Passkey doesn't match")

    @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="")
    def RequestAuthorization(self, device_path):
        LOG.info("Received RequestAuthorization (%s)", device_path)

    @dbus.service.method(AGENT_INTERFACE, in_signature="os", out_signature="")
    def AuthorizeService(self, device, uuid):
        LOG.info("Received AuthorizeService (%s, %s)", device, uuid)

        service_id = uuid[4:8]
        LOG.debug("s_id.lower = %s ALLOWED_SERVICES = %s",
                  service_id.lower(), ALLOWED_SERVICES)

        if service_id.lower() in ALLOWED_SERVICES:
            LOG.info("Service %s is in %s, allow",
                     service_id.lower(), ALLOWED_SERVICES)
            self.__set_trusted(device)
            return

        LOG.warn("Service not allowed")

    @dbus.service.method(AGENT_INTERFACE, in_signature="", out_signature="")
    def Cancel(self):
        LOG.info("Received Cancel")


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    parser = OptionParser()
    parser.add_option("-c", "--capability", action="store",
                      type="string", dest="capability")

    options, _ = parser.parse_args()
    capability = options.capability or "KeyboardDisplay"

    BUS = None
    while BUS is None:
        try:
            LOG.info("Attempting to connect to system bus...")
            BUS = dbus.SystemBus()
        except DBusException as ex:
            LOG.warn("Failed to connect to dbus %s: %s",
                     ex.get_dbus_name(), ex.message)

            time.sleep(5)

    # Create and register agent implementation
    LOG.info("Attempting to register Agent with capability '%s' ...", capability)
    Agent(BUS, AGENT_PATH)

    obj = BUS.get_object(BUS_NAME, "/org/bluez")
    manager = dbus.Interface(obj, "org.bluez.AgentManager1")
    manager.RegisterAgent(AGENT_PATH, capability)
    manager.RequestDefaultAgent(AGENT_PATH)
    LOG.info("Agent registered")

    LOG.info("Ensuring that adapter is discoverable/pairable...")
    try:
        props = dbus.Interface(find_adapter().proxy_object,
                               "org.freedesktop.DBus.Properties")

        props.Set(ADAPTER_INTERFACE, "Discoverable", True)
        props.Set(ADAPTER_INTERFACE, "Pairable", True)
        props.Set(ADAPTER_INTERFACE, "DiscoverableTimeout", dbus.UInt32(0))
        props.Set(ADAPTER_INTERFACE, "PairableTimeout", dbus.UInt32(0))
        LOG.info("Adapter is pairable/discoverable now")
    except DBusException as ex:
        LOG.warn("Failed to make adapter discoverable/pairable: %s. %s",
                 ex.get_dbus_name(), ex.message)

    GObject.MainLoop().run()
