* title = Projects
* page_title = projects
* navkey = projects

Hey. Here's stuff I've made for my own fun. This page is *heavily* influenced by [Eevee's projects page](http://me.veekun.com/projects/).

## Web

### soofw <span class="sub">&#8210; [link](http://soofw.com/) / [github](http://github.com/scizzorz/soofw)</span>

This very web site. Written in [Python](http://www.python.org/). Powered by [Flask](http://flask.pocoo.org/). Stored in plain [Markdown](http://daringfireball.net/projects/markdown/) text files. Served by [nginx](http://www.nginx.org/) and [gunicorn](http://gunicorn.org/). Hosted on a [Linode](http://www.linode.com/) running [Ubuntu](http://www.ubuntu.com/).

I bought some old domain that I thought was totally badass when I was 15, but I decided it wasn't really that cool by the time I was 18. At the same time, I wasn't really a fan of those firstnamelastname.com domains, so I opted out of those. I decided the domain name didn't really matter as long as it was *simple*, so I spent some time searching for two, three, or four letter domains. They don't exist anymore. I moved on to five, and found soofw. It was simple, easily typed, and totally hipster, so I bought it.

Over the years it's been through a lot, but I've recently started to take it semi-seriously and updating it every so often...

### Canvas Demos <span class="sub">&#8210; [link](http://soofw.com/demos/)</span>

A collection of web experiments. Written in JavaScript. Powered by the HTML5 canvas element.

I like tinkering with new toys. I heard about HTML5 and its new canvas witchcraft, and since I kinda missed making pretty things with Flash, I leapt right into it. These are the results of all that tinkering. These are mostly just dirty coding done in my free time, so don't expect any high-quality code here. There's also a pretty good chance it won't work if you're using some ancient browser.

### Rainbow Heart <span class="sub">&#8210; [experiments page](http://www.chromeexperiments.com/detail/rainbow-heart/) / [link](http://soofw.com/demos/heart++) / [github](https://github.com/scizzorz/heart)</span>

A rainbow heart composed of elastic particles. Written in JavaScript. Powered by a handmade particle engine that utilizes the HTML5 canvas element.

This was one of the first canvas demos I did. I just kinda randomly applied for the [Chrome Experiments](http://www.chromeexperiments.com/) and they accepted me. I was pretty happy about that.

## Command Line

### trk <span class="sub">&#8210; [github](https://github.com/scizzorz/trk)</span>

A to do list manager. Written in [Python](http://www.python.org/).

Google Tasks was really starting to let me down. The lack of an official Android app killed me, and the web interface was just miserable. I figured that since I spent so much time in a terminal anyway, it would be the perfect place to set up a neat little task manager. It also gave me a pretty good chance to work on my Python skills. As one of my most actively used and developed projects, I've tried to polish `trk` as much as possible. Since its inception, I've rewritten it using another project of mine, `bumpy`, in order to be more flexible and powerful, although the rewrite is still under development.

### bumpy <span class="sub">&#8210; [github](https://github.com/scizzorz/bumpy), [pypi](https://pypi.python.org/pypi/bumpy)</span>

A library for building small projects, managing repetitive tasks, and CLI Python tools. Written in [Python](http://www.python.org/).

After learning about the wonders of Python, Flask, and SCSS for web development, I started using `make` to manage my repetitive tasks like compiling SCSS, launching a dev server, and generating static pages. Using `make` to call Python scripts felt a little... dirty, so I set about finding a way to call Python scripts from Python. Eventually I stumbled upon [Pynt](https://github.com/rags/pynt) and was pretty happy with it, until I tried it and started experiencing a weird bug when launching a Flask dev server. I got frustrated and started writing my own Python build system with heavy influence from Pynt. After getting it to a usable state and letting it launch a Flask dev server, I got the same bug and decided it was an issue with my Flask set ups or Flask itself, but decided I would continue developing `bumpy` anyway.

Eventually, I noticed the command line argument parsing I was using with `bumpy` could be pretty easily suited to making CLI Python tools, and immediately jumped back to `trk` and started rewriting it using `bumpy` instead, with a significant improvement in usability.

### clk <span class="sub">&#8210; [github](https://github.com/scizzorz/clk)</span>

A time tracker. Written in [Python](http://www.python.org/).

Sometimes I like to keep track of how much time I spend on a certain project. Because most of my work is done through a terminal, it made sense for me to write a time tracker that I could use from that environment.

Largely unused and inactive right now.

### multigit <span class="sub">&#8210; [github](https://github.com/scizzorz/multigit)</span>

A tool for checking up on multiple local git repos. Written in bash.

Frequently, I find myself working on several different projects in quick succession and easily lose track of which projects are uncommitted, unpushed, need to be fetched/merged, etc., so I created `multigit` to easily execute a command across multiple Git repos. For example, I can simply type `multigit status -s` and get a quick glimpse of each repo's status, or I can type `multigit pull` to automatically fetch and merge every repo that I'm tracking.

## Android Apps

### trk for Android <span class="sub">&#8210; [github](https://github.com/scizzorz/trk-android)</span>

A to do list manager. Written in [Java](http://www.java.com/) with the [Android SDK](http://developer.android.com/index.html).

Even though I spend a lot of my time in a terminal, there's plenty of situations where it's difficult or impossible for me to open a terminal and view my `trk` list. To remedy this, I've started developing an Android app using the same standards and specification that the command-line version of `trk` uses: a text file that contains a list of tasks and uses tags and patterns to organize and manage a to do list. Still under active development.

## Widgets

### LCD Clock <span class="sub">&#8210; [github](https://github.com/scizzorz/arduino-remote-lcd)</span>

A physical LCD clock. Written in C++ / [Python](http://www.python.org/). Powered by [Arduino](http://www.arduino.cc/).

Arduinos are frickin' sweet as heck. I bought a few and was just waiting for some idea to hit me. I'd also been using a little Android app I wrote to control my desktop music from my bed, but I didn't really like having to reach for my phone, turn the screen on, etc. just to change the song, so I started to think about an alternative way to control it. Then the idea struck, and I decided to use an Arduino to do it. The actual box is about 4 inches x 3 inches x 2 inches, has four [illuminated buttons](http://www.adafruit.com/products/558) for control, a [white monochrome character LCD](https://www.sparkfun.com/products/9052) for disply, and an [Arduino Micro](http://www.adafruit.com/products/1086) for brains.

*Pictures coming eventually.*


### Binary LED Clock <span class="sub">&#8210; [github](https://github.com/scizzorz/arduino-binary-clock)</span>

A physical LED binary clock. Written in C++ / [Python](http://www.python.org/). Powered by [Arduino](http://www.arduino.cc/).

Arduinos are neat. Clocks are neat. Binary is neat. Why not combine all three? Although it's not as practical, it looks nice and gets some conversations started. The box is about 8 inches x 3 inches x 1.5 inches, has ten colored LEDs (four for hours, six for minutes) for display, and an [Arduino Uno](http://www.adafruit.com/products/50) for brains. The LEDs are ordered in a specific pattern to make it more readable at night. Likewise, the red LEDs blink when inactive to provide a reference point in the dark.

*Pictures coming eventually.*

### Whiteboard Desk

My computer desk. Frame is made of wood, surface is made of whiteboard.

I was home for the summer and stuck using a cheap plastic table as my desk, which kinda sucked. Every time I moved my hand the whole desk shook and rattled my monitors. I talked to my uncle about making a desk, drew up some plans, and got to work. The whole desk is designed to be easily taken apart, transported, and reassembled; it only takes six screws to assemble / disassemble. The whiteboard is replaceable and costs about $10 for a new one. The frame is about 54 inches (wide) x 26 inches (deep) x 28 inches (tall).

*Pictures coming eventually.*
