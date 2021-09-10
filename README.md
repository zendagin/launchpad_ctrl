This is a ros package for `Novation Launchpad MK2` using python.
There are two nodes `launchpad_node.py` and `launchpad_manager.py`.

## launchpad_node.py
`launchpad_node.py` is a node commmunicate with the launchpad with `pygame`. To use this node please install `pygame` and its dependencies `sdl1.2`.

It will publish a topic `launchpad_key_event` on every key event. The msg `LaunchpadKey` contains `x`(uint), `y`(uint), `keydown`(bool) and `type`(string). Notice that x value means vertical and y value means horizontal starting from bottom left(0, 0).

It also subscribe color topics for lighting the launchpad. See content of `launchpad_node.py`, definations of .msg files, and [Launchpad MK2 Programmers Reference Manual](https://d2xhy469pqj8rc.cloudfront.net/sites/default/files/novation/downloads/10529/launchpad-mk2-programmers-reference-guide-v1-02.pdf) for more details.

## launchpad_manager.py
`launchpad_manager.py` is a node using with `launchpad_node.py` provides higher level interfaces and functions for launchpad applications. It can support up to 4 modes and hide the buttons `Session`, `User 1`, `User 2`, `Mixer` for swiching mode. It can takes up to 4 arguments for user definded mode and overwrite from `Srssion` botton to `Mixer` botton. Please enter the full class path `package.file.class` for the arguments. A folder with a file `__init__.py` will be considered as a python package.

### Behaviour
When the node starts, it will create all mode objects. Which means that __init__() of the mode classes will be call. It will also pass the mode number (0 to 3) as parameter. Whenever a mode is switched (and mode 0 just after startup) its start() function will be called, and pause() function of the old mode. Moreover, when a keyevent is recived, it will call execute() function of current mode and pass the LaunchpadKey object to it. See `launchpad_manager.py` and `basic_mode.py` for more details.

### Write a custom mode
As metioned above, a mode should define `__init__(self, modeNumber)`, `start(self)`, `pause(self)`, and `execute(self, LaunchpadKey)`. Also, a mode is expected to handle its own color layout by pubulishing color related topics directly. `BasicMode` in `basic_mode.py` is already implemented color related functions. It is strongly recomand to inherit from `BasicMode` and overide exsisted functions when writing a new custom mode.



