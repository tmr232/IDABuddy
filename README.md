# IDABuddy

## What is it?

IDABuddy is a reverse-engineer's best friend. Designed to be everything
Clippy the Office Assistant was, and more!

IDABuddy will always be there for you. Friendly and helpful while you
work. Offering tips and friendly chat.

And best of all - since it is open-source, it will never be taken away
from you!


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

Visual settings are stored in `config.yml`, as well as documentation.

#### Available avatars:

<img width="200" src="idabuddy/avatar/Clippy.png">
<img width="200" src="idabuddy/avatar/superida.png">
<img width="200" src="idabuddy/avatar/xmasida.png">

Or create your own!


## In The Press

IDABuddy was presented in a lightning talk at 32c3. Watch the video [here](https://youtu.be/zMp2jAHquns?t=1h33m25s).
