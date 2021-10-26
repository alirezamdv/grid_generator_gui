## Grid Generator GUI
This is a graphical user interface for triangle software.
Triangle generates exact Delaunay triangulations, constrained Delaunay triangulations, conforming Delaunay triangulations, Voronoi diagrams,
and high-quality triangular meshes. [More](https://www.cs.cmu.edu/~quake/triangle.html)
-----
### Installation

#### Using miniconda (recommended for Ollie users)
SSh to Ollie using -Y flag.
Load miniconda using:
```sh
 $ module load miniconda
  ```
Then download the cod in your work/ollie/home directory and navigate in the directory:
```shell
$ git clone https://gitlab.awi.de/amahdavi/grid_generator_gui.git
$ cd grid_generator_gui
```
Create a Conda environment using:
```shell
$ conda env create --file environment.yml
```
Activate the environment:
```shell
$ conda activate grid_generator
```
Then install the software like:
```shell
$ python setup.py install 
```
Now you can Run the Application using:
```shell
$ python start.py
```
--------
#### Using pip
Create a virtual environment using:
```shell
$ python3 -m venv venv
```
Then activate it:
```shell
$ source venv/bin/activate
```
Install the packages like:
```shell
$ pip install .
```
Run the Application :
```shell
$ python start.py
```
-------