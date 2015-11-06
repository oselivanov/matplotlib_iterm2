# External matplotlib backend for iterm2

External matplotlib backend uses iTerm2 inline image display feature.

![matplotlib_iterm2](https://github.com/oselivanov/matplotlib_iterm2/raw/master/demo.png)

## Installation

*Disclamer*: IPython support of external backends is really clunky, so in
order to make this backend work we do some black magic in ipython
user profile.

 1. Install iTerm2 nightly build https://iterm2.com/downloads/nightly/#/section/home
 2. Grab imgcat utility from http://iterm2.com/images.html#/section/home and drop it somewhere in your PATH.
 3. pip install matplotlib_iterm2
 4. Add following code to your ~/.ipython/PROFILE/ipython_config.py
    ([ipython profile config](https://ipython.org/ipython-doc/dev/config/intro.html)):

    ```python
    c = get_config()

    from IPython.core.pylabtools import backends
    backends['iterm2'] = 'module://matplotlib_iterm2.backend_iterm2'

    from IPython.core.shellapp import backend_keys
    backend_keys.append('iterm2')

    c.TerminalIPythonApp.pylab = 'iterm2'
    ```

*Note*: After the installation, on startup python will show you something like:
 
    [TerminalIPythonApp] WARNING | GUI event loop or pylab initialization failed
    UsageError: Invalid GUI request 'iterm2', valid ones are:['osx', 'qt4', 'glut', 'gtk3', None, 'pyglet', 'wx', 'none', 'qt', 'gtk', 'tk']

That's fine, it'll work anyway.

## TODO

 - Use less hacky approach to enable matplotlib_iterm2 in ipython.
 - Write directly to terminal instead of using imgcat.
 - Do something w/ warnings on startup.
