import subprocess
import re
from optparse import OptionParser


def get_args():
    parser = OptionParser()
    parser.add_option("-i", "--interface", dest="interface",
                      help="interface to change")
    parser.add_option("-m", "--mac", dest="new_mac",
                      help="New MAC address")
    (options, args) = parser.parse_args()
    if not options.interface:
        parser.error('[-] please specify an interface')
    if not options.new_mac:
        parser.error('[-] please specify a new_mac')
    return options


def change_mac(interface, new_mac):
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])


def get_mac(interface):
    result = subprocess.check_output(['ifconfig', interface])
    mac_result = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', str(result))
    if mac_result:
        return mac_result.group(0)
    else:
        print('[-] could not read MAC address')


opts = get_args()
# print('[+] Current MAC: ', get_mac(opts.interface))
# change_mac(opts.interface, opts.new_mac)
# print('[+] MAC changed: ', get_mac(opts.interface))
