apt-dgrade
==========

What's ?
--------

It's an utility to help you to downgrade your system debian or debian-based.

This is helpful if you have enabled the experimental or sid repository and
installed something, for example the newer version of gnome-shell and want 
to downgrade to stable version, or any other situation like this.

It's based on [apt-downgrade](https://code.google.com/p/apt-downgrade/).

Which are the dependencies ?
----------------------------

It's written in Python language, then you'll need Python and Python libraries

* Python 2.7+
* Python APT

You can install these packages on debian with:
```bash
# run this command as root
apt-get install python python-apt
# or you can use aptitude
# run as root also
aptitude install python python-apt
```
For other distributions please refer to distribution's documentation.

Legal Information
-----------------

Copyright © 2013 Victor Aurélio.

This program is released under GNU General Public License(GNU GPL) either
version 3 of the License, or (at your option) any later version, for more 
details please see the [LICENSE](LICENSE) file.

