"""iTerm2 exterimental backend for matplotlib.

Based on iTerm2 nightly build feature - displaying images in terminal.
http://iterm2.com/images.html#/section/home

Example:

import matplotlib
matplotlib.use('xxx')
from pylab import *
plot([1,2,3])
show()
"""

__author__ = 'Oleg Selivanov <oleg.a.selivanov@gmail.com>'

import os
import subprocess
import tempfile

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib._pylab_helpers import Gcf
from matplotlib.backend_bases import FigureManagerBase
from matplotlib.figure import Figure
from PIL import Image

# TODO(oleg): Show better message if PIL/Pillow is not installed.
# TODO(oleg): Check if imgcat script exists.


def show():
    for manager in Gcf.get_all_fig_managers():
        manager.show()
        # TODO(oleg): Check if it's okay to destroy manager here.
        Gcf.destroy(manager.num)


def new_figure_manager(num, *args, **kwargs):
    FigureClass = kwargs.pop('FigureClass', Figure)
    thisFig = FigureClass(*args, **kwargs)
    canvas = FigureCanvasAgg(thisFig)
    manager = FigureManagerTemplate(canvas, num)
    return manager


class FigureManagerTemplate(FigureManagerBase):
    def show(self):
        canvas = self.canvas
        canvas.draw()

        if matplotlib.__version__ < '1.2':
            buf = canvas.buffer_rgba(0, 0)
        else:
            buf = canvas.buffer_rgba()

        render = canvas.get_renderer()
        w, h = int(render.width), int(render.height)
        im = Image.frombuffer('RGBA', (w, h), buf, 'raw', 'RGBA', 0, 1)
        with tempfile.NamedTemporaryFile(suffix='.png', delete=True) as f:
            im.save(f.name)
            # Subprocess compatible with both ipython and jupyter console. See:
            # https://github.com/ipython/ipykernel/issues/310
            # https://github.com/oselivanov/matplotlib_iterm2/issues/3
            with subprocess.Popen(
                ['imgcat', f.name],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                close_fds=True,
            ) as process:
                for line in iter(process.stdout.readline, b""):
                    print(line.rstrip().decode("utf-8"))


FigureManager = FigureManagerBase
