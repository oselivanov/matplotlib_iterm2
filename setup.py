from setuptools import setup, find_packages

setup(
    name='matplotlib_iterm2',
    version='0.1.0',
    description='iTerm2 exterimental backend for matplotlib',
    long_description='iTerm2 exterimental backend for matplotlib uses '
                     'displaying images iterm2 nightly build feature',
    url='https://github.com/oselivanov/matplotlib_iterm2',
    author='Oleg Selivanov',
    author_email='oleg.a.selivanov@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='ipython iterm2 matplotlib backend',
    install_requires=['ipython', 'matplotlib', 'pillow'],
    packages=find_packages(),
)
