## Map generator

Generator of real-life like map for Engineering Distributed Infrastructure course at University of Warsaw. 
The project consists of designing, building and deploying a distributed application on a public cloud. 
Each team had an assigned Googler tutor who helped to scope the project; reviewed design documents and graded the final solution.

### About project
The main goal of this project is to relatively fast generate large graph with a few assumptions.
Graph has to be:

* planar, <br />
* weighted, <br />
* sparse, <br />
* provide 2D layout of vertices, <br />
* similar to google map

Every vertex represents crossroad and edge is a two-way street.

### Map partition
* 512 x 512 regions  <br />
* every region is 320 x 320 units  <br />
* point coordinates are integers  <br />
* for every region, there is randomized type of village with certain probability  <br />
* for every village, there is randomized number of crossroads according to village type  <br />
* expected number of points in a village is 45  <br />
* expected number of points on the map is 11 796 480

### Estimation of density and distribution of points
As a model I took the demographics of Poland and populated map to look like Poland
| Population  | Number of such villages | Estimation of number of crossroads |
| ----------- | ----------------------- | ---------------------------------- |
| 1M - 2M     | 1                       | 10.000 - 30.000                    |
| 500k - 1M   | 5                       | 5000 - 10.000                      |
| 200k - 500k | 10                      | 3000 - 5000                        |
| 100k - 200k | 25                      | 2000 - 4000                        |
| 20k - 100k  | 200                     | 500 - 2000                         |
| 10k - 20k   | 200                     | 200 - 500                          |
| 2k - 10k    | 600                     | 50 - 200                           |
| 10 - 2000   | 30.000                  | 5 - 50                             |

### Distribution of points inside region
* expected density is between ⅓ - ⅙   <br />
* inside given region, we choose rectangular area and recursivelt shorten it <br />
* as we achieve area with satisfying size, we randomly generate points and edges

### Connecting points inside regions
Euclidean minimum spanning tree:
* Delaunay triangulation
* Union–find data structure 

As we want to add extra edges, we modified Union-find data structure as follows:
* if two points a and b are in distincts sets, we add edge between them
* if two points a and b are in the same sets, we add edge between them with probability ¼

### Connecting regions
To avoid keeping 10^7 vertices and about 3 * 10^7 edges (which is about 1GB of data) we do as follows:
* save all region's verices and edges to file
* we compute convex hull and we keep in memory only vertices on it
* now we connect all regions in similar way as we connevted points inside regions and for two regions to connect we select the closest points on convex hulls of those regions

### Visualization of distribution of points in 64x64 regions:
![](https://media.giphy.com/media/25oX5fKVj2qtb5WCKL/giphy.gif)
