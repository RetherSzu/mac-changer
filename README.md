# Random MAC Address Changer

This script generates a random MAC address and provides the functionality to change the MAC address
of a network interface on Linux.

## What is MAC Address?

A MAC (Media Access Control) address is a unique identifier assigned to a network interface card (NIC)
by the manufacturer. It is a 48-bit address composed of six octets, typically represented in hexadecimal
format as six pairs of two characters separated by colons (e.g., `00:1A:2B:3C:4D:5E`).

## Why Change MAC Address?

There are several reasons why you might want to change your MAC address:

- **Enhancing Privacy and Security**: Changing your MAC address can help protect your privacy by preventing
  unauthorized tracking or identification of your device on a network. It can make it more difficult for
  network administrators or malicious actors to associate your network activity with your device.

- **Bypassing Network Restrictions or Filters**: In certain situations, network administrators or internet
  service providers may implement restrictions or filters based on MAC addresses. Changing your MAC address
  can help bypass such restrictions and access networks or services that might be otherwise inaccessible.

- **Troubleshooting Network Issues**: Changing the MAC address can be useful for troubleshooting network
  connectivity or compatibility issues. It allows you to simulate different network environments or test
  specific configurations without altering the actual hardware.

- **Network Simulations and Testing**: Researchers, network administrators, or developers may need to
  simulate multiple devices or test specific network scenarios. Changing MAC addresses provides a way to
  create virtual network environments and perform comprehensive testing.

## How Does This Script Work?

This script is a command-line tool that provides options to change and randomize the MAC address of a
specified network interface on Linux.

### Features

- `generate_random_mac_address()`: Generates a random MAC address.
- `change_mac_address(interface, new_mac)`: Changes the MAC address of a specified network interface
  on Linux, requiring root privileges to execute the necessary commands.
- `reset_mac_address(interface)`: Resets the MAC address of a network interface to its default value.
- `get_permanent_mac_address(interface)`: Retrieves the permanent MAC address of a network interface
  using the `ethtool` command.
- Command-line arguments (`-i`, `--interface`, `-m`, `--mac`, `-r`, `--reset`): Provide options to specify
  the network interface, set a custom MAC address, or reset the MAC address to its default value.

### Usage

Run the script with root privileges:

```bash
python script.py --interface <interface_name> [--mac <mac_address>] [--reset]
```

- `<interface_name>`: Name of the network interface.
- `<mac_address>` (optional): Custom MAC address to set. If not provided, a random MAC address will be generated.
- `--reset` (optional): Resets the MAC address of the specified interface to its default value.
