# The Package Branch of Lindu Software
[![PyPI version](https://badge.fury.io/py/lindu.svg)](https://badge.fury.io/py/lindu)
[![GitHub issues](https://img.shields.io/github/issues/comp-geoph-itera/lindu-software)](https://github.com/comp-geoph-itera/lindu-software/issues)
[![GitHub forks](https://img.shields.io/github/forks/comp-geoph-itera/lindu-software)](https://github.com/comp-geoph-itera/lindu-software/network)
[![GitHub stars](https://img.shields.io/github/stars/comp-geoph-itera/lindu-software)](https://github.com/comp-geoph-itera/lindu-software/stargazers)
[![GitHub license](https://img.shields.io/github/license/comp-geoph-itera/lindu-software)](https://github.com/comp-geoph-itera/lindu-software/blob/dev/LICENSE.md)

<p align="center">
	<img src="https://github.com/comp-geoph-itera/lindu-software/blob/package/src/lindu/Widgets/Images/screenshots/lindu-logo.png" alt="Lindu Logo" width="200"/>
	<br>
	Lindu Software Logo
	<br>
</p>
Progress of Lindu Software Codes (for seismological data processing: determining and relocating hypocenter; traveltime tomography)

This is the package branch for the future release.

See the [changelog file](https://github.com/comp-geoph-itera/lindu-software/blob/package/CHANGELOG.md)

# Developer
If you would like to be the collaborator, feel free to pull request.

# Installation
Now, pip can be used for installing Lindu.
```bash
pip install lindu
```

# Python version
The minimum version is 3.8.

# How to Use
```python
import lindu
lindu.run()
```

# Build a package
In the parent repository, type these commands:
```bash
pip install --upgrade build
python -m build
```

# References
If you will use this software, please add these references to your research:
```
@article{styawan_lindu_2020,
	title = {Lindu {Software}: {A} {Free} {Seismological} {Data} {Processing} {Software} {For} {Traveltime} {Tomography} {Using} {Python} {Framework}},
	volume = {537},
	copyright = {All rights reserved},
	issn = {1755-1315},
	shorttitle = {Lindu {Software}},
	url = {https://doi.org/10.1088%2F1755-1315%2F537%2F1%2F012017},
	doi = {10.1088/1755-1315/537/1/012017},
	abstract = {Earthquake data can be used to infer some physical properties for representing the subsurface condition. The 3-Dimensional (3D) seismic velocity structure as a kind of these important properties contains the information of variation in lithology change and fluid saturation. The most common method for inverting from the travel time of seismic event into 3D seismic velocity structure is travel time tomography which is based on the relation between velocity and travel time of P- and S-wave. Based on this concept, we develop a module of Lindu software to infer this seismic velocity structure from travel time data. This module is a part of seismological data processing sequences that have been integrated into Lindu software. The Lindu software uses Python framework, a kind of high-level programming languages. The pseudo-bending raytracing method is employed to calculate the travel time between the event sources and stations and also to build the kernel matrix. The resolution test that relates density of rays and resulted tomogram uses the synthetic Checkerboard Resolution Test (CRT) by using Damped-Least Squares (DLS) method for the inversion. For validating this module, it has been tested by using both synthetic and real data.},
	language = {en},
	urldate = {2020-09-07},
	journal = {IOP Conference Series: Earth and Environmental Science},
	author = {Styawan, Yudha and Firdaus, Ruhul and Yudistira, Tedi and Suhendi, Cahli},
	month = aug,
	year = {2020},
	note = {Publisher: IOP Publishing},
	pages = {012017}
}

@article{styawan_preliminary_2019,
	title = {The preliminary results of {Lindu} software: a free seismological data processing using python framework},
	volume = {311},
	copyright = {All rights reserved},
	issn = {1755-1315},
	shorttitle = {The preliminary results of {Lindu} software},
	url = {https://doi.org/10.1088%2F1755-1315%2F311%2F1%2F012078},
	doi = {10.1088/1755-1315/311/1/012078},
	abstract = {LINDU software is developed to solve integrated earthquake data processing. It is GUI based software that fulfil the needed for user friendly type of software. The Python framework is used for computation and visualization and integrates the common programs for earthquake data processing, such as GAD.exe, JHD.exe, and HypoDD.exe. It is also integrates the common procedure of routine data processing in earthquake seismology and works in local and regional scale. In this paper, we shows the preliminary results of LINDU software for several functions. To identify arrival time of P-wave we employ Akaike Information Criterion (AIC), MER (Modified Energy Ratio) and S/L Kurt�s method. The results of these method will be considered as guided � auto picking. However, the results also can be treated as reference for picking manually with Seisgram2k.jar. Geiger�s method is employed to locate the event location. The events can be relocated and 1D velocity can be updated by employing Joint Hypocenter Determination (JHD). The next method to relocate the event location is Double Difference (DD) algorithm. The precision result of Lindu software has been tested using IRIS and real data available which run seamlessly.},
	language = {en},
	urldate = {2020-09-07},
	journal = {IOP Conference Series: Earth and Environmental Science},
	author = {Styawan, Yudha and Andika, Putu Pradnya and Suhendi, Cahli and Firdaus, Ruhul and Sudibyo, Maria R. P. and Erlangga, I. F. and Ry, Rexha Verdhora},
	month = aug,
	year = {2019},
	note = {Publisher: IOP Publishing},
	pages = {012078}
}

@article{andika_lindu_2019,
	title = {Lindu {Software}: {An} {Open} {Source} {Seismological} {Data} {Processing} {Using} {Python} {Framework} {To} {Relocate} {Hypocenter} ({Preliminary} {Software})},
	volume = {318},
	copyright = {All rights reserved},
	issn = {1755-1315},
	shorttitle = {Lindu {Software}},
	url = {https://doi.org/10.1088%2F1755-1315%2F318%2F1%2F012021},
	doi = {10.1088/1755-1315/318/1/012021},
	abstract = {Recorded seismogram of an earthquake data contains the earth structure information. Researchers developed the method to extract the information and derives it into the program codes. However, generally, the program codes developed only for specific function and work on only specific scale. Almost the existing programs have a limitation, for example, they work on command-line based and less user-friendly. Lindu software is developed to solve these problems. In this paper, we show the preliminary results of Lindu software, a GUI � based software which is open source and developed in python platform. This software integrates the common procedure of routine data processing in earthquake seismology and works in local and regional scale. It is designed to read multi-component data on multi-station. To identify events automatically, we employ SL Kurt�s method and use the results as guided auto�picking. However, the picked time also can be changed manually. Furthermore, we employ Joint Hypocenter Determination (JHD) algorithm to locate the hypocenter of earthquake events and update the 1D velocity model simultaneously. Then the events can be relocated by employing the double-difference method. The software was tested on the available data from IRIS and BMKG and shows the acceptable and reliable results.},
	language = {en},
	urldate = {2020-09-07},
	journal = {IOP Conference Series: Earth and Environmental Science},
	author = {Andika, Putu Pradnya and Styawan, Yudha and Suhendi, Cahli and Firdaus, Ruhul},
	month = aug,
	year = {2019},
	note = {Publisher: IOP Publishing},
	pages = {012021}
}
```

# Galleries
<p align="center">
	<img src="https://github.com/comp-geoph-itera/lindu-software/blob/package/src/lindu/Widgets/Images/screenshots/lindu-dev-5.PNG" alt="Lindu Development" width="800"/>
	<br>
	Lindu Progress (2021-10-27)
	<br>	
</p>