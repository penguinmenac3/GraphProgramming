# Graph Programming
Code can be interpreted as a graph. Actually compilers already do that. However, this project takes that approach to the programmer.

![Image of the graph programming ui.](https://raw.githubusercontent.com/penguinmenac3/GraphProgramming/master/images/GraphProgrammingIDE.png)

For install instructions see installation section.

# Motivation
The world gets smarter and more connected. But who will programm all those smart bits in the internet of things?
A simple answer would be programmers. However, there is so much that you can do and so few programmers that can implement it.

And even an experienced programmer may often think why do I always have to do the same work and cannot reuse code easily.
Usually writing network code for IoT applications is a tedious task.
And once you have written your network logic you are no longer motivated to write the actual intelligence based on all that sensor information.
At least in hobby projects that is usually the case.

Wouldn't it be cool if you just had to implement a sensor transformation that somehow handles how the physical sensor is transformed into a data structure?
What if there is a piece of software that you give that data structure tell it a server and it pushes the data structure to the server automatically.
A user interface for the server could then show the sensor node and give you the possibility to drop it into a flow chart and connect it with other sensors that way.
Of course you can add custom algorithms you implement on the server and connect the sensors as inputs to them in the flowchart.

Well only sensing stuff and calculating stuff is not cool, is it?
What if you could also implement actors like sensors.
However instead of sending data structures they listen for data structures and do something when they receive one.

Now imagine what would be possible when you had such a tool!


And yet there is more you can do with it.

Parallelism in algorithms can sometimes be difficult.
What if I told you, when modeling your program as a graph the execution environment can automatically detect what parts can be running in paralell and do all the synchronisation stuff.

# Installation

## Linux

There are a few simple steps to get up and running on linux.

Before we can start you need all prerequisits.

```bash
sudo apt-get install python python-dev git
sudo pip install autobahn[twisted]

# Optional but recommended
sudo apt-get install libopencv-dev
```

First make a Graphs and a GraphLib folder somewhere where you want your data to be stored.
(Having full access to this folder is crutial for graph programming to work.)

```bash
# The user executing the server needs full access here!
cd ~
mkdir Graphs
mkdir GraphLib
touch GraphLib/__init__.py
```

Now clone the repository to a location where you want to install graph programming and cd into the folder.

```bash
# The user executing the server needs full access here!
cd /dir/where/to/install
git clone https://github.com/penguinmenac3/GraphProgramming.git
cd GraphProgramming
```

Next setup the links to your Data folders.
```bash
ln -s /home/<username>/Graphs grapheditor/data/private
ln -s /home/<username>/GraphLib python/privatelib
```

Now add your binaries to your home.
```bash
ln -s /dir/where/to/install/GraphProgramming/graphex.sh ~/graphex.sh
ln -s /dir/where/to/install/GraphProgramming/graphedit.sh ~/graphedit.sh
```

Finally test it.
```bash
~/graphedit.sh
```

Visit [localhost:8088](localhost:8088) in a Browser (e.g. Chrome, NOT Internet Explorer or Edge)

## Windows

Install linux and follow the linux guide.

Just kidding, there is no windows tutorial yet, however you can try similar to linux.

# One more thing

The implementation already supports opencv and raspi servo drivers from adafruit.
More robot stuff is on it's way.

![Image of the graph programming ui.](https://raw.githubusercontent.com/penguinmenac3/GraphProgramming/master/images/CVGraph.png)