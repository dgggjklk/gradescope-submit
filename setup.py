from setuptools import setup

setup(
    name='gradescope-submit',
    version='0.1.0',    
    description='My attempt at converting the gradescope-submit script to a python package for windows',
    url='https://github.com/dgggjklk/gradescope-submit',
    author='TWelsh',
    packages=['gradescope-submit'],
    install_requires=['mpi4py>=2.0',
                      'numpy',                     
                      ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Students',
        'Operating System :: Windows',
    ],
)
