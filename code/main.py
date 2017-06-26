import networkx as nx
import igraph as igraph
import os, time
import utils_files
import utils_latex
import utils_networks
import settings as settings
import matplotlib.pyplot as plt
import community    # Community detection tool for networkx - http://perso.crans.org/aynaud/communities/

# Mark start time
startTime = time.clock()

# Remove output files and directories
utils_files.silent_remove(settings.output_directory, is_dir=True)
# if settings.print_summary_csv:
#     utils_files.silent_remove(settings.output_summary_path, is_dir=True)
# if settings.print_latex_report:
#     utils_files.silent_remove(settings.output_latex_path, is_dir=True)
# Create default directories
os.makedirs(os.path.dirname(settings.output_directory), exist_ok=True)
os.makedirs(os.path.dirname(settings.output_directory + "toy/"), exist_ok=True)
os.makedirs(os.path.dirname(settings.output_directory + "model/"), exist_ok=True)
os.makedirs(os.path.dirname(settings.output_directory + "real/"), exist_ok=True)
os.makedirs(os.path.dirname(settings.output_directory + "temp/"), exist_ok=True)
os.makedirs(os.path.dirname(settings.output_directory + "clu_files/"), exist_ok=True)


# Define input directory and loop over it recursively
inputDirectory = settings.input_networks_path

for subdir, dirs, files in os.walk(inputDirectory):
    for file in files:
        if file.endswith(".net"):
            # Create file path
            net_name = file.replace('.net', '')
            filePath = subdir + os.sep + file
            print('\n==========================='); print(filePath)

            # Read pajek network into igraph
            # g = igraph.read(filePath, format="pajek")
            g = igraph.Graph.Read(filePath, format="pajek")
            # Simplify the graph by removing self-loops and/or multiple edges
            g.simplify()

            clu_file = filePath.replace('.net', '.clu')
            if utils_files.check_if_exists(clu_file):
                membership_ref = utils_files.read_file_into_array(file_name = clu_file)
                membership_ref.pop(0)  # Remove first position in array (first line only says the number of vertices)
                membership_ref = list(map(int, membership_ref))     # Transform strings to ints
                # Subtract 1 from every value in the list, this is because some pajek clu files start the membership labelling from 1
                if 0 not in membership_ref:
                    membership_ref = [x - 1 for x in membership_ref]
            else:
                membership_ref = [0] * g.vcount()
            print(membership_ref)

            # Find communities using method 1 (based on the betweenness of the edges in the network)
            # FROM: http://stackoverflow.com/questions/25254151/using-igraph-in-python-for-community-detection-and-writing-community-number-for
            # Method description: http://igraph.org/c/doc/igraph-Community.html#idm470942725872
            if "airports_UW" not in file:   # For some reason this method (edge betweenness) last too much in airports network
                dendrogram_m1 = igraph.Graph.community_edge_betweenness(g)  # Calculate dendrogram
                clusters_m1 = dendrogram_m1.as_clustering() # Convert it into a flat clustering
                membership_m1 = clusters_m1.membership  # Get the membership vector
            else:
                membership_m1 = [0] * g.vcount()
            print(membership_m1)

            # Find communities using method 2 (based on the optimization of modularity, fastgreedy)
            # FROM: https://lists.nongnu.org/archive/html/igraph-help/2007-09/msg00011.html
            # Method description: http://igraph.org/c/doc/igraph-Community.html#idm470942730032
            dendrogram_m2 = igraph.Graph.community_fastgreedy(g)    # Calculate dendrogram
            clusters_m2 = dendrogram_m2.as_clustering() # Convert it into a flat clustering
            membership_m2 = clusters_m2.membership  # Get the membership vector
            print(membership_m2)

            # Find communities using method 3 (based on louvain method)
            # FROM: http://perso.crans.org/aynaud/communities/
            # Install it using: pip install python-louvain
            # Method description: https://sites.google.com/site/findcommunities/
            # first compute the best partition
            g_nx = nx.Graph(nx.read_pajek(filePath))
            partition = community.best_partition(g_nx)
            membership_m3 = list(partition.values())
            print(membership_m3)

            # Plot resulting community detection separately in a temporal file
            utils_networks.plot_graph_with_communities(g, membership_ref, file_name="../output/temp/temp_1.png")
            utils_networks.plot_graph_with_communities(g, membership_m1, file_name="../output/temp/temp_2.png")
            utils_networks.plot_graph_with_communities(g, membership_m2, file_name="../output/temp/temp_3.png")
            utils_networks.plot_graph_with_communities(g, membership_m3, file_name="../output/temp/temp_4.png")

            # Read all temporal created images and create a sub-ploted figure
            utils_networks.plot_all_temp_images(file, subdir[subdir.rfind('/')+1:])

            # Save pajek clu files
            utils_networks.save_graph_in_clu_format(comm=membership_m1, path="../output/clu_files/" + net_name + "_edge_bet.clu")
            utils_networks.save_graph_in_clu_format(comm=membership_m2, path="../output/clu_files/" + net_name + "_fastgreedy.clu")
            utils_networks.save_graph_in_clu_format(comm=membership_m3, path="../output/clu_files/" + net_name + "_louvain.clu")

            # Compare communities detected using different methods
            # FROM: http://igraph.org/python/doc/igraph.clustering-module.html#compare_communities
            comp1_vi = igraph.compare_communities(membership_ref, membership_m1, method="vi")  # variation of information metric of Meila (2003)
            comp1_nmi = igraph.compare_communities(membership_ref, membership_m1, method="nmi") # normalized mutual information as defined by Danon et al (2005)
            comp1_ji = utils_networks.compare_communities(membership_ref, membership_m1, method="jaccard-index")    # Jaccard Index

            comp2_vi = igraph.compare_communities(membership_ref, membership_m2, method="vi")  # variation of information metric of Meila (2003)
            comp2_nmi = igraph.compare_communities(membership_ref, membership_m2, method="nmi")  # normalized mutual information as defined by Danon et al (2005)
            comp2_ji = utils_networks.compare_communities(membership_ref, membership_m2, method="jaccard-index")  # Jaccard Index

            comp3_vi = igraph.compare_communities(membership_ref, membership_m3, method="vi")  # variation of information metric of Meila (2003)
            comp3_nmi = igraph.compare_communities(membership_ref, membership_m3, method="nmi")  # normalized mutual information as defined by Danon et al (2005)
            comp3_ji = utils_networks.compare_communities(membership_ref, membership_m3, method="jaccard-index")    # Jaccard Index

            # Compute modularity value for every partition including reference ones
            mod_ref = igraph.Graph.modularity(g, membership_ref)
            mod_m1 = igraph.Graph.modularity(g, membership_m1)
            mod_m2 = igraph.Graph.modularity(g, membership_m2)
            mod_m3 = igraph.Graph.modularity(g, membership_m3)

            # Add new values to compare communities table
            compare_communities_values = [file, comp1_vi, comp1_nmi, comp1_ji, comp2_vi, comp2_nmi, comp2_ji, comp3_vi, comp3_nmi, comp3_ji]
            utils_files.add_row_to_csv(path=settings.output_csv_comparison, headers=settings.csv_header_comparison, values=compare_communities_values)

            # Add new values to compare communities table
            modularity_values = [file, mod_ref, mod_m1, mod_m2, mod_m3]
            utils_files.add_row_to_csv(path=settings.output_csv_modularity, headers=settings.csv_header_modularity, values=modularity_values)


# Delete temporal files
utils_files.silent_remove("../output/temp/", is_dir=True)
# Show execution statistics after finishing
measuredTime = time.clock() - startTime
print('Execution time = {}'.format(measuredTime))