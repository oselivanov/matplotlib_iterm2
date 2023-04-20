"""
iTerm2 experimental backend for matplotlib. Based on iTerm2 nightly build feature
for displaying images in the terminal: http://iterm2.com/images.html#/section/home
"""

__author__ = 'Oleg Selivanov <oleg.a.selivanov@gmail.com>'

import os
import shutil
import subprocess
import tempfile

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib._pylab_helpers import Gcf
from matplotlib.backend_bases import FigureManagerBase
from matplotlib.figure import Figure

# Whether to close figures
# TODO: Make this configurable
CLOSE = True

try:
    from IPython import get_ipython
except ImportError:
    get_ipython = lambda: None

try:
    from PIL import Image
except ImportError:
    raise RuntimeError("Package 'pillow' is required for matplotlib_iterm2 backend.")

if 'TERM_PROGRAM' in os.environ:
    terminal = os.environ['TERM_PROGRAM']
else:
    terminal = 'unknown'

if 'iTerm' not in terminal:
    raise RuntimeError(
        'Current terminal {!r} is not compatible with matplotlib_iterm2 backend. '
        "Please use 'iTerm' instead: http://iterm.com".format(terminal)
    )
if not shutil.which('imgcat'):
    raise RuntimeError(
        "iTerm2 executable 'imgcat' not found in $PATH. For install "
        'instructions see: https://iterm2.com/documentation-images.html'
    )


def _draw_output(output):
    # Print the figure returned as output
    if isinstance(output.result, matplotlib.figure.Figure):
        _draw_safe(output.result)


def _draw_queue():
    # Print the figures created in a cell
    if not show._draw_triggered:
        return
    figs = (None,)
    if not CLOSE:
        figs = set(fm.canvas.figure for fm in Gcf.get_all_fig_managers())
        figs = [fig for fig in show._draw_queue if fig in figs]  # active only
    try:
        for fig in figs:
            _draw_safe()
    finally:
        # Clear flags for next round
        show._draw_queue.clear()
        show._draw_triggered = False


def _draw_safe(fig=None):
    # Safely flush the figure or figures
    try:
        return fig.show() if fig else show()
    except Exception as e:
        # Safely show traceback if in IPython, else raise
        ip = get_ipython()
        if ip is None:
            raise e
        else:
            ip.showtraceback()


def draw_if_interactive():
    # Signal that the current active figure should be drawn at the
    # end of cell execution. This is called inside pyplot.figure().
    manager = Gcf.get_active()
    if manager is None:
        return  # no active figure
    if not matplotlib.is_interactive():
        return  # interactive draw disabled
    # Queue up the figure and set flag to ensure it will be drawn
    fig = manager.canvas.figure
    try:
        show._draw_queue.remove(fig)
    except ValueError:
        pass
    show._draw_queue.append(fig)
    show._draw_triggered = True


def new_figure_manager(num, *args, **kwargs):
    # Generate instance of manager subclass
    cls = kwargs.pop('FigureClass', Figure)
    fig = cls(*args, **kwargs)
    canvas = FigureCanvas(fig)
    return FigureManagerInline(canvas, num)


def show():
    # Show all the figures
    try:
        for manager in Gcf.get_all_fig_managers():
            manager.show()
    finally:
        if CLOSE:
            matplotlib.pyplot.close('all')


class FigureCanvas(FigureCanvasAgg):
    # Figure canvas required for pyplot backends in matplotlib > 3.6.
    required_interactive_framework = None


class FigureManagerInline(FigureManagerBase):
    # Manager that prints using subprocess compatible with ipython and jupyter console.
    # https://github.com/ipython/ipykernel/issues/310
    # https://github.com/oselivanov/matplotlib_iterm2/issues/3
    def show(self):
        canvas = self.canvas
        canvas.draw()
        if matplotlib.__version__ < '1.2':
            buf = canvas.buffer_rgba(0, 0)
        else:
            buf = canvas.buffer_rgba()
        render = canvas.get_renderer()
        dims = (int(render.width), int(render.height))
        image = Image.frombuffer('RGBA', dims, buf, 'raw', 'RGBA', 0, 1)
        with tempfile.NamedTemporaryFile(suffix='.png', delete=True) as temp:
            image.save(temp.name)
            with subprocess.Popen(
                ['imgcat', temp.name],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                close_fds=True,
            ) as process:
                print('')  # required to avoid indenting jupyter-vim figures
                for line in iter(process.stdout.readline, b''):
                    print(line.rstrip().decode('utf-8'))


# Use default figure manager
FigureManager = FigureManagerBase

# This list is populated by draw_if_interactive and cleared by _draw_queue
show._draw_queue = []

# This flag will be reset by draw_if_interactive when called
show._draw_triggered = False

# Register shell event
shell = get_ipython()
if shell is not None:
    from matplotlib import get_backend
    from IPython.core.pylabtools import activate_matplotlib
    activate_matplotlib(get_backend())
    shell.events.register('post_execute', _draw_queue)
    shell.events.register('post_run_cell', _draw_output)
