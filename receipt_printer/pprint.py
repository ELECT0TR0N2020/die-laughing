# A simple python script to print to the printer from stdin

# NEEDS SUDO TO ROOT !!!

from sys import stdin
from escpos.printer import Usb

""" Seiko Epson Corp. Receipt Printer (EPSON TM-T88III) """
p = Usb(0x0416, 0x5011)#, 0, profile="TM-T88III")

for line in stdin:
	p.text(line)

p.text("\n\n\n")
