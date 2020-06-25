<p align="center">
  <img width="2000" height="250" src="/images/banner.png">
</p>

Python scripts to help procedurally generate maps using perlin noise.

## Blend
### Command Line Arguments
```shell
Usage: blend.py [OPTIONS] IMAGE1 IMAGE2 MASK

Options:
  -o TEXT   output file
```
### Example
#### input
```shell
> python blend.py dirt.png grass.png mask.png
```
#### output
<p align="center">
  <img width="1000" height="225" src="/images/blend.png">
</p>

## genNoise

### Command Line Arguments
```shell
Usage: noiseMap.py [OPTIONS] SIZE SCALE

Options:
  -l INT    number of bit levels
  -o TEXT   output file
```
### Example
#### input
```shell
> noiseMap.py 1024 50
```
#### output
<p align="left">
  <img width="250" height="250" src="/images/noiseMap.png">
</p>

## waterGeometry

### Command Line Arguments
```shell
Usage: waterGeometry.py [OPTIONS] HEIGHT_MAP

Options:
  -o TEXT   output file
```
### Example
#### input
```shell
> python waterGeometry.py heightMap.png
```
#### output
##### input mask
<p align="left">
  <img width="250" height="250" src="/images/water1.png">
</p>

##### render of output obj file
<p align="left">
  <img width="250" height="250" src="/images/water2.png">
</p>

## genPoints
### Command Line Arguments

Usage: genPoints.py [OPTIONS] MASK LEVELS
```shell
Options:
  -o TEXT                 output file
  -c <INT, INT, INT>...   colors to use for points
  -r INT...               max/min radii
  -sampleRadius INT       sample radius for poisson
  -rejectionSamples INT   number of rejection sample for poisson
```
### Example
#### input
```shell
> python genPoints.py -c 255 255 0 -c 0 255 0 mask.png 8
```
#### output
<p align="left">
  <img width="250" height="250" src="/images/genPoints.png">
</p>
