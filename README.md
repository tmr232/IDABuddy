# IDABuddy


## Requirements

1. [Sark](https://github.com/tmr232/sark)
1. [Sark's plugin-loader plugin](http://sark.readthedocs.org/en/latest/plugins/installation.html)
1. [PyYAML](http://pyyaml.org/)

## Installation

1. Clone the IDABuddy repository
1. Add `idabuddy\idabuddy_plugin.py` to your `plugins.list` (`%AppData%\HexRays\plugins.list` or `C:\Program Files (x86)\IDA 6.9\cfg\plugins.list`).
1. Launch IDA


## Configuration

### What can I say?

IDABuddy's messages are stored in `sayings.yml`.

Basic sayings are lists of strings, spoken out one after the other.

Address sayings are single strings, with `{}` in them to denote the location
to put the address to jump to.

### How do I look?

Visual settings are stored in `config.yml`.

You can change the `stylesheet` to change the looks of the talk bubble,
or change the `image` to use a different buddy image.

<img style="float: right;" src="help.png">
