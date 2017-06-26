# Community detection

Apply at least three different community detection algorithms for the attached networks. It is not necessary to implement them, you may use any freely available software. At least one of the algorithms must be based on the optimization of modularity (but not all of them), and you must use at least two different programs (i.e. do not use the same application all the time).

Some of the provided networks have a partition of reference, obtained from external information. In these cases, you have to compare your partitions with them, using at least the following standard measures: Jaccard Index, Normalized Mutual Information (arithmetic normalization), and Normalized Variation of Information. It is not necessary to implement the calculation of these indices, you may use any program (e.g. Radatools).

The objective is to compare the partitions obtained with the different algorithms, to try to conclude which is the best method you have found.

The delivery must include:

* Brief description of the algorithms and the programs used.

* Selected parameters for each algorithm and/or network, and the scripts used (if any).

* The obtained partitions, in Pajek format (*.clu)

* For each network and partition, a plot with color-coded communities. To facilitate the comparison of partitions:

	- If the network contains coordinates for the nodes (e.g. airports_UW.net), use them to establish the position of the nodes. Otherwise, use the Kamada-Kawai (without separation of components) to distribute the nodes in the plane. Avoid circular layouts.

	- The position of the nodes must not change for all the partitions of the same network.

	- Put all the plots of the different partitions of the same network close to each other, i.e. do not group by algorithm, group by network.

* A table with the comparison measures between your partitions and the reference ones, grouped by network.

* A table with the modularity values of all the partitions (including the reference ones), grouped by network.

* Your conclusions about the advantages and quality of the used algorithms.

It is not expected that the obtained partitions be equal to the reference ones or between them, with some exceptions.
