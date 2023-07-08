"""
Random MAC Address Changer

This script generates a random MAC address and provides the functionality to change the MAC address
of a network interface on Linux.

The `generate_random_mac()` function generates a random MAC address.

The `change_mac_address()` function changes the MAC address of a specified network interface on Linux,
requiring root privileges to execute the necessary commands.

The `reset_mac_address()` function resets the MAC address of a network interface to its default value.

Usage:
    python script.py --interface <interface_name> [--mac <mac_address>] [--reset]

Note:
    Changing MAC addresses without proper authorization may have legal implications.
    Use this script responsibly and ensure you have appropriate permissions.

"""

import random
import subprocess
import argparse
import sys


def print_color(text):
    """
    Prints colored text to the console.

    :param text: Text to be printed.
    :type text: str

    Colors:
        - {W} : white (normal)
        - {R} : red
        - {G} : green
        - {O} : orange
        - {B} : blue
        - {P} : purple
        - {C} : cyan
        - {GR}: gray
        - {D} : dims current color. {W} resets.

    Replacements:
        - {+} : Displays a plus sign in green. Example: {+}
        - {!} : Displays an exclamation mark in orange. Example: {!}
        - {?} : Displays a question mark in white. Example: {?}
        - {*} : Displays an asterisk in white. Example: {*}

    :Example:

    >>> print_color("{R}Error occurred: {!} Something went wrong.")
    \033[31mError occurred: \033[33m[\033[31m!\033[33m]\033[0m Something went wrong.
    >>> print_color("{+} Task completed successfully.")
    \033[0m\033[2m[\033[0m\033[32m+\033[0m\033[2m]\033[0m Task completed successfully.

    :Note:
        - The colors are applied using ANSI escape codes, which may not work on all platforms or consoles.
        - Use the provided color codes and replacements to format the text as needed.

    """
    # Basic console colors
    colors = {
        "W": "\033[0m",  # white (normal)
        "R": "\033[31m",  # red
        "G": "\033[32m",  # green
        "O": "\033[33m",  # orange
        "B": "\033[34m",  # blue
        "P": "\033[35m",  # purple
        "C": "\033[36m",  # cyan
        "GR": "\033[37m",  # gray
        "D": "\033[2m"   # dims current color. {W} resets.
    }

    # String replacements
    replacements = {
        "{+}": "{W}{D}[{W}{G}+{W}{D}]{W}",
        "{!}": "{O}[{R}!{O}]{W}",
        "{?}": "{W}[{C}?{W}]",
        "{*}": "{W}[{C}*{W}]",
    }

    # Apply color and replacement formatting
    output = text
    for (key, value) in replacements.items():
        output = output.replace(key, value)
    for (key, value) in colors.items():
        output = output.replace("{" + key + "}", value)

    # Print the formatted text
    sys.stdout.write(output + "\n")
    sys.stdout.flush()


def generate_random_mac_address():
    """
    Generates a random MAC address.

    :return: Randomly generated MAC address as a string.
    :rtype: str
    """
    # Generate a random MAC address
    mac = [random.randint(0x00, 0xff) for _ in range(6)]
    mac[0] &= 0xfe
    # Format the MAC address
    return ":".join([f"{octet:02x}" for octet in mac])


def change_mac_address(interface, new_mac):
    """
    Changes the MAC address of a network interface on Linux.

    :param interface: Name of the network interface.
    :type interface: str
    :param new_mac: New MAC address to set.
    :type new_mac: str

    :raises subprocess.CalledProcessError: If the command execution fails.
    :note: Requires root privileges.
    """
    try:
        subprocess.check_call(["ifconfig", interface, "down"])
        subprocess.check_call(["ifconfig", interface, "hw", "ether", new_mac])
        subprocess.check_call(["ifconfig", interface, "up"])
    except subprocess.CalledProcessError as exception:
        print_color("{!} Error executing command: " + str(exception))
        sys.exit(1)


def get_permanent_mac_address(interface):
    """
    Retrieves the permanent MAC address of a network interface using ethtool.

    :param interface: Name of the network interface.
    :type interface: str

    :return: Permanent MAC address of the network interface.
    :rtype: str
    """
    try:
        output = subprocess.check_output(["ethtool", "-P", interface]).decode()
        lines = output.strip().split("\n")
        for line in lines:
            if "Permanent address" in line:
                return line.split(" ")[2].strip()
    except subprocess.CalledProcessError as exception:
        print_color("{!} Error executing command: " + str(exception))
        sys.exit(1)


def get_valid_interfaces():
    """
    Retrieves the valid network interfaces on a Linux system.

    :return: List of valid network interfaces.
    :rtype: list[str]
    """
    try:
        output = subprocess.check_output(["ip", "link", "show"])
        lines = output.decode().splitlines()
        interfaces = [lines[index].split(":")[1].strip()
            for index in range(len(lines))
                if lines[index].strip()[0].isdigit() and "link/ether" in lines[index + 1]
        ]
        return interfaces
    except subprocess.CalledProcessError:
        return []


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Random MAC Address Changer")
    parser.add_argument("-i", "--interface", required=True, help="Network interface name")
    parser.add_argument("-m", "--mac", help="Custom MAC address to set")
    parser.add_argument("-r", "--reset", action="store_true", help="Reset MAC address to default")
    args = parser.parse_args()

    # Check if running with root privileges
    if subprocess.check_output(["id", "-u"]).decode().strip() != "0":
        print_color("{!} Execute the script with root priviliege")
        sys.exit(1)

    # Check if the given interface is valid
    validInterfaces = get_valid_interfaces()
    if args.interface not in validInterfaces:
        print_color("{!} Invalid interface: " + args.interface)
        print_color("{*} Valid interface:")
        for validInterface in validInterfaces:
            print(f"\t{validInterface}")
        sys.exit(1)

    # Reset the MAC address to its default value
    if args.reset:
        # Retrieve the permanent MAC address
        permanent_mac = get_permanent_mac_address(args.interface)
        if permanent_mac:
            print_color("{+} Permanent MAC address: " + permanent_mac)
        else:
            print_color(
                "{!} Failed to {R}retrieve{W} the permanent MAC address.")

        # Reset MAC address
        change_mac_address(args.interface, permanent_mac)
        print_color("{+} MAC address {G}reset{W} to default.")
        sys.exit(0)

    # Generate or retrieve the MAC address
    if args.mac:
        new_mac_address = args.mac
    else:
        new_mac_address = generate_random_mac_address()
    print_color("{+} Generated MAC address: " + new_mac_address)

    # Change the MAC address on the specified interface
    change_mac_address(args.interface, new_mac_address)
    print_color("{+} MAC address changed {G}successfully{W} !")
