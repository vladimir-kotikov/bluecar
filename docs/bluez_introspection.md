# Introspection XMLs for various bluez objects

To get those XMLs use the following command, replacing `/org/bluez` object path with the path you want ot introspect
```
dbus-send --system --type=method_call --print-reply \ --dest=org.bluez \    /org/bluez \    org.freedesktop.DBus.Introspectable.Introspect
```

## `bluez` root

```xml

<!DOCTYPE node PUBLIC "-//freedesktop//DTD D-BUS Object Introspection 1.0//EN""http://www.freedesktop.org/standards/dbus/1.0/introspect.dtd">
<node>
    <interface name="org.freedesktop.DBus.Introspectable">
        <method name="Introspect">
            <arg name="xml" type="s" direction="out"/>
        </method>
    </interface>
    <interface name="org.freedesktop.DBus.ObjectManager">
        <method name="GetManagedObjects">
            <arg name="objects" type="a{oa{sa{sv}}}" direction="out"/>
        </method>
        <signal name="InterfacesAdded">
            <arg name="object" type="o"/>
            <arg name="interfaces" type="a{sa{sv}}"/>
        </signal>
        <signal name="InterfacesRemoved">
            <arg name="object" type="o"/>
            <arg name="interfaces" type="as"/>
        </signal>
    </interface>
    <node name="org"/>
</node>
```

## `/org/bluez` object

```xml

<!DOCTYPE node PUBLIC "-//freedesktop//DTD D-BUS Object Introspection 1.0//EN"
"http://www.freedesktop.org/standards/dbus/1.0/introspect.dtd">
<node>
    <interface name="org.freedesktop.DBus.Introspectable">
        <method name="Introspect">
            <arg name="xml" type="s" direction="out"/>
        </method>
    </interface>
    <interface name="org.bluez.AgentManager1">
        <method name="RegisterAgent">
            <arg name="agent" type="o" direction="in"/>
            <arg name="capability" type="s" direction="in"/>
        </method>
        <method name="UnregisterAgent">
            <arg name="agent" type="o" direction="in"/>
        </method>
        <method name="RequestDefaultAgent">
            <arg name="agent" type="o" direction="in"/>
        </method>
    </interface>
    <interface name="org.bluez.ProfileManager1">
        <method name="RegisterProfile">
            <arg name="profile" type="o" direction="in"/>
            <arg name="UUID" type="s" direction="in"/>
            <arg name="options" type="a{sv}" direction="in"/>
        </method>
        <method name="UnregisterProfile">
            <arg name="profile" type="o" direction="in"/>
        </method>
    </interface>
    <interface name="org.bluez.Alert1">
        <method name="RegisterAlert">
            <arg name="category" type="s" direction="in"/>
            <arg name="agent" type="o" direction="in"/>
        </method>
        <method name="NewAlert">
            <arg name="category" type="s" direction="in"/>
            <arg name="count" type="q" direction="in"/>
            <arg name="description" type="s" direction="in"/>
        </method>
        <method name="UnreadAlert">
            <arg name="category" type="s" direction="in"/>
            <arg name="count" type="q" direction="in"/>
        </method>
    </interface>
    <interface name="org.bluez.HealthManager1">
        <method name="CreateApplication">
            <arg name="config" type="a{sv}" direction="in"/>
            <arg name="application" type="o" direction="out"/>
        </method>
        <method name="DestroyApplication">
            <arg name="application" type="o" direction="in"/>
        </method>
    </interface>
    <node name="hci0"/></node>
```

## hci0 adapter at /org/bluez/hci0

```xml

<!DOCTYPE node PUBLIC "-//freedesktop//DTD D-BUS Object Introspection 1.0//EN"
"http://www.freedesktop.org/standards/dbus/1.0/introspect.dtd">
<node>
    <interface name="org.freedesktop.DBus.Introspectable">
        <method name="Introspect">
            <arg name="xml" type="s" direction="out"/>
        </method>
    </interface>
    <interface name="org.bluez.Adapter1">
        <method name="StartDiscovery"></method>
        <method name="StopDiscovery"></method>
        <method name="RemoveDevice">
            <arg name="device" type="o" direction="in"/>
        </method>
        <property name="Address" type="s" access="read"></property>
        <property name="Name" type="s" access="read"></property>
        <property name="Alias" type="s" access="readwrite"></property>
        <property name="Class" type="u" access="read"></property>
        <property name="Powered" type="b" access="readwrite"></property>
        <property name="Discoverable" type="b" access="readwrite"></property>
        <property name="DiscoverableTimeout" type="u" access="readwrite"></property>
        <property name="Pairable" type="b" access="readwrite"></property>
        <property name="PairableTimeout" type="u" access="readwrite"></property>
        <property name="Discovering" type="b" access="read"></property>
        <property name="UUIDs" type="as" access="read"></property>
        <property name="Modalias" type="s" access="read"></property>
    </interface>
    <interface name="org.freedesktop.DBus.Properties">
        <method name="Get">
            <arg name="interface" type="s" direction="in"/>
            <arg name="name" type="s" direction="in"/>
            <arg name="value" type="v" direction="out"/>
        </method>
        <method name="Set">
            <arg name="interface" type="s" direction="in"/>
            <arg name="name" type="s" direction="in"/>
            <arg name="value" type="v" direction="in"/>
        </method>
        <method name="GetAll">
            <arg name="interface" type="s" direction="in"/>
            <arg name="properties" type="a{sv}" direction="out"/>
        </method>
        <signal name="PropertiesChanged">
            <arg name="interface" type="s"/>
            <arg name="changed_properties" type="a{sv}"/>
            <arg name="invalidated_properties" type="as"/>
        </signal>
    </interface>
    <interface name="org.bluez.Media1">
        <method name="RegisterEndpoint">
            <arg name="endpoint" type="o" direction="in"/>
            <arg name="properties" type="a{sv}" direction="in"/>
        </method>
        <method name="UnregisterEndpoint">
            <arg name="endpoint" type="o" direction="in"/>
        </method>
        <method name="RegisterPlayer">
            <arg name="player" type="o" direction="in"/>
            <arg name="properties" type="a{sv}" direction="in"/>
        </method>
        <method name="UnregisterPlayer">
            <arg name="player" type="o" direction="in"/>
        </method>
    </interface>
    <interface name="org.bluez.CyclingSpeedManager1">
        <method name="RegisterWatcher">
            <arg name="agent" type="o" direction="in"/>
        </method>
        <method name="UnregisterWatcher">
            <arg name="agent" type="o" direction="in"/>
        </method>
    </interface>
    <interface name="org.bluez.HeartRateManager1">
        <method name="RegisterWatcher">
            <arg name="agent" type="o" direction="in"/>
        </method>
        <method name="UnregisterWatcher">
            <arg name="agent" type="o" direction="in"/>
        </method>
    </interface>
    <interface name="org.bluez.ThermometerManager1">
        <method name="RegisterWatcher">
            <arg name="agent" type="o" direction="in"/>
        </method>
        <method name="UnregisterWatcher">
            <arg name="agent" type="o" direction="in"/>
        </method>
        <method name="EnableIntermediateMeasurement">
            <arg name="agent" type="o" direction="in"/>
        </method>
        <method name="DisableIntermediateMeasurement">
            <arg name="agent" type="o" direction="in"/>
        </method>
    </interface>
    <interface name="org.bluez.NetworkServer1">
        <method name="Register">
            <arg name="uuid" type="s" direction="in"/>
            <arg name="bridge" type="s" direction="in"/>
        </method>
        <method name="Unregister">
            <arg name="uuid" type="s" direction="in"/>
        </method>
    </interface>
    <node name="dev_98_01_A7_AE_52_5C"/>
    <node name="dev_A4_51_6F_8A_AF_59"/></node>
```

## Device connected to `hci0` adapter

```xml

<!DOCTYPE node PUBLIC "-//freedesktop//DTD D-BUS Object Introspection 1.0//EN"
"http://www.freedesktop.org/standards/dbus/1.0/introspect.dtd">
<node>
    <interface name="org.freedesktop.DBus.Introspectable">
        <method name="Introspect">
            <arg name="xml" type="s" direction="out"/>
        </method>
    </interface>
    <interface name="org.bluez.Device1">
        <method name="Disconnect"></method>
        <method name="Connect"></method>
        <method name="ConnectProfile">
            <arg name="UUID" type="s" direction="in"/>
        </method>
        <method name="DisconnectProfile">
            <arg name="UUID" type="s" direction="in"/>
        </method>
        <method name="Pair"></method>
        <method name="CancelPairing"></method>
        <property name="Address" type="s" access="read"></property>
        <property name="Name" type="s" access="read"></property>
        <property name="Alias" type="s" access="readwrite"></property>
        <property name="Class" type="u" access="read"></property>
        <property name="Appearance" type="q" access="read"></property>
        <property name="Icon" type="s" access="read"></property>
        <property name="Paired" type="b" access="read"></property>
        <property name="Trusted" type="b" access="readwrite"></property>
        <property name="Blocked" type="b" access="readwrite"></property>
        <property name="LegacyPairing" type="b" access="read"></property>
        <property name="RSSI" type="n"access="read"></property>
        <property name="Connected" type="b" access="read"></property>
        <property name="UUIDs" type="as" access="read"></property>
        <property name="Modalias" type="s" access="read"></property>
        <property name="Adapter" type="o" access="read"></property>
    </interface>
    <interface name="org.freedesktop.DBus.Properties">
        <method name="Get">
            <arg name="interface" type="s" direction="in"/>
            <arg name="name" type="s" direction="in"/>
            <arg name="value" type="v" direction="out"/>
        </method>
        <method name="Set">
            <arg name="interface" type="s" direction="in"/>
            <arg name="name" type="s" direction="in"/>
            <arg name="value" type="v" direction="in"/>
        </method>
        <method name="GetAll">
            <arg name="interface" type="s" direction="in"/>
            <arg name="properties" type="a{sv}" direction="out"/>
        </method>
        <signal name="PropertiesChanged">
            <arg name="interface" type="s"/>
            <arg name="changed_properties" type="a{sv}"/>
            <arg name="invalidated_properties" type="as"/>
        </signal>
    </interface>
    <interface name="org.bluez.Network1">
        <method name="Connect">
            <arg name="uuid" type="s" direction="in"/>
            <arg name="interface" type="s" direction="out"/>
        </method>
        <method name="Disconnect"></method>
        <property name="Connected" type="b" access="read"></property>
        <property name="Interface" type="s" access="read"></property>
        <property name="UUID" type="s" access="read"></property>
    </interface>
    <interface name="org.bluez.MediaControl1">
        <method name="Play"></method>
        <method name="Pause"></method>
        <method name="Stop"></method>
        <method name="Next"></method>
        <method name="Previous"></method>
        <method name="VolumeUp"></method>
        <method name="VolumeDown"></method>
        <method name="FastForward"></method>
        <method name="Rewind"></method>
        <property name="Connected" type="b" access="read"></property>
    </interface>
    <node name="fd0"/>
    <node name="player0"/></node>"
```
