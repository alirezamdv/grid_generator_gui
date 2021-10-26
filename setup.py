from setuptools import setup

setup(
    name='grid_generator_gui',
    version='0.1.0',
    packages=['src', 'src.polygons'],
    url='',
    license='',
    author='Alireza Mahdavi',
    author_email='a.mahdavi@outlook.com',
    description='a graphical user interface for Triangle.c software.',
    install_requires=[
        'Jinja2==3.0.1',
        'netCDF4==1.5.7',
        'numpy==1.21.2',
        'pyside2==5.14.2.2',
        'PyQt5==5.15.5',
        'pyqtlet==0.3.3',
        'PyQtWebEngine==5.15.5'
    ]
)
