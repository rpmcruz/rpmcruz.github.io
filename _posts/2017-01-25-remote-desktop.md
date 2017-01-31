---
layout: post
title: Remote Desktop Sharing
category: ubuntu
---

OMG Ubuntu recently published a piece on the [least known feature of Ubuntu.](http://www.omgubuntu.co.uk/2017/01/ubuntu-hud-user-poll)

That made me wonder: what is the least known application of Ubuntu?

[Actually I meant to write this post for a while, but I thought this would make a better opening. :)]

Remmina is an [hidden gem](http://www.remmina.org/) in the Linux desktop. It allows to seamless connect to the desktop of another computer using the protocols VNC (Linux) or RDP (Windows).

I had colleagues using TeamViewer in Linux because they were unware these tools were available out-of-the-box. TeamViewer is a desktop sharing tool that uses a centralized server rather than doing a direct connection. The drawbacks are obvious: (a) slower since it requires extra communication to the centralized server, (b) TeamViewer sees whatever you send, (c) the Linux version is not native and uses Wine (argh), (d) it is always polling resources for some reason, and (e) it is illegal to use in your work unless you buy a license.

As an example, let us connect to our own machine for fun:

![Remmina1](/img/2017-01-25/01-remmina1.png)

![Remmina2](/img/2017-01-25/01-remmina2.png)

You must first enable desktop sharing. You can access it through the Dash by searching "desktop sharing" or through the command "vino-preference".

![Vino](/img/2017-01-25/01-vino.png)

But, but... what if my computer does not have a public IP? Fear not. As long as your company has a public computer with sshd running, you can simply ssh-tunnel through it. Remmina makes this incredibly easy. You can just specify the IP of the public computer and your (username, password) tuple. You can also use a SSH key, which you can create very easily through [seahorse](https://help.gnome.org/users/seahorse/stable/) (search for "key" in the Dash.)

Free bonus - Other cool desktop sharing tricks:

Instead of sharing your complete desktop, why not run the editor in your computer and run the code in the server?

First of all, you'll want to create a ssh tunnel: ssh -L 8888:riquix:8888 rpcruz@public.inesctec.pt, where `rpcruz@public.inesctec.pt` is your username and public computer address, `riquix` is the computer within the private network where you work, and the numbers are the port you want to access. The ports can differ, in case the port in your machine is being used.

You can also use [Jupyter](http://jupyter.org/), which is a web server that features an editor and a bunch of things. It is usually used for programming in Python, because it was originally developed to run Python code, but it can run code of pretty much any language. Run it in your work computer: `jupyter notebook --ip`, and then access by opening your browser in your computer and going to `localhost:8888`. The editor will run at local speed, and the code will run at the server speed and can also access remote files (since it is running in that machine!). [Note: you need to type `%matplotlib inline` in the editor so matplotlib works.)

![Jupyter](/img/2017-01-25/01-jupyter.png)

For Python, you can also do the same using Spyder, which is a Python IDE for scientific computing. It looks and feels a lot like the Matlab interface. It can use IPython for the console, which uses the same technology as Jupyter (which was, in fact, formely called IPython Notebook before supporting multiple languages). Run Spyder in your local machine, and then open a new console using "Connect to an existing kernel" and you can then connect to your remote Jupyter.

You can do something identical using R with [RStudio](https://www.rstudio.com/) and AFAIK Matlab as well. RStudio is built using web technologies to make this possible and easy, even your desktop version is a web-wrapper! It uses by default the port 8787.


PS: Thanks to [José Devezas](http://josedevezas.com/) for prompting me to start a blog! This will be an opportunity to improve my English and writting skills, and connect with other similarly minded people.
