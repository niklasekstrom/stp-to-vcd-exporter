# Exporter of traces from .stp to .vcd format

When using the SignalTap feature in
[Quartus](https://www.intel.com/content/www/us/en/products/details/fpga/development-tools/quartus-prime.html)
the traces are natively stored in the
[.stp](https://www.intel.com/content/www/us/en/programmable/quartushelp/17.0/reference/glossary/def_stp.htm)
file format.

The .stp file format does not have broad support (if any?) outside of Quartus.
An alternative file format for traces is the
[Value Change Dump (.vcd)](https://en.wikipedia.org/wiki/Value_change_dump)
format. There are many tools available to visualize .vcd files, such as this
online viewer: [https://vc.drom.io/](https://vc.drom.io/).

It is possible to export traces to .vcd format from inside of Quartus. However,
the exporter in Quartus has some limitations, such as that buses are exported
as their individual signals, and a few other minor annoyances.

This repository contains a program written in Python that reads an .stp file and
writes out a corresponding .vcd file. The program is simple enough so that you
might be able to modify the code if you want to customize the output further.
