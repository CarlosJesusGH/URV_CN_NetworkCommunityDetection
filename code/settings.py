# Directories and files
output_summary_path = "../output/summary.csv"
output_csv_comparison = "../output/community_comparison.csv"
output_csv_modularity = "../output/community_modularity.csv"
output_latex_path = "../report/latex.tex"
input_networks_path = "../input/"   # Sometimes is better going dir by dir or even network by network
output_directory = "../output/"
# Flags
show_figures = True
save_figures = False
save_pickle = False
print_latex_report = False
print_summary_csv = False
# Vertex colors
vertex_colors = [ 'red', 'blue', 'green', 'cyan', 'pink', 'orange', 'grey', 'yellow', 'white',
                  'black', 'purple', 'magenta', 'darkblue', 'darkgreen', 'salmon', 'yellowgreen']

# CSV headers
csv_header_comparison = ['network_name',
                         'comp1_vi', 'comp1_nmi', 'comp1_ji',
                         'comp2_vi', 'comp2_nmi', 'comp2_ji',
                         'comp3_vi', 'comp3_nmi', 'comp3_ji']
csv_header_modularity = ['network_name', 'mod_ref', 'mod_m1', 'mod_m2', 'mod_m3']