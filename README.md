# External matplotlib backend for iterm2

External matplotlib backend uses iTerm2 inline image display feature.

![matplotlib_iterm2](https://github.com/oselivanov/matplotlib_iterm2/raw/master/demo.png)

## Installation
 1. Install iTerm2 nightly build https://iterm2.com/downloads/nightly/#/section/home
 2. Grab imgcat utility from http://iterm2.com/images.html#/section/home and drop it somewhere in your PATH.
 3. git clone https://github.com/oselivanov/matplotlib_iterm2
 4. Symlink matplotlib_iterm2 to your site-packages (it's weird, I know, see TODO).
 5. Add following to ipython_config.py ([ipython profile config](https://ipython.org/ipython-doc/dev/config/intro.html)):

    ```python
    c = get_config()

    from IPython.core.pylabtools import backends
    backends['iterm2'] = 'module://matplotlib_iterm2.backend_iterm2'

    from IPython.core.shellapp import backend_keys
    backend_keys.append('iterm2')

    c.TerminalIPythonApp.pylab = 'iterm2'
    ```

## TODO
 
 - Write directly to terminal instead of using imgcat.
 - Add setup.py and upload matplotlib_iterm2 to pypi.
 - Use less hacky approach to enable matplotlib_iterm2 in ipython.
