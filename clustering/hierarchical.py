from matplotlib import pyplot as plt
from random import sample
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import sys

def fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop('max_d', None)
    if max_d and 'color_threshold' not in kwargs:
        kwargs['color_threshold'] = max_d
    annotate_above = kwargs.pop('annotate_above', 0)

    ddata = dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        plt.title('Hierarchical Clustering Dendrogram (truncated)')
        plt.xlabel('sample index or (cluster size)')
        plt.ylabel('distance')
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
                plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                             textcoords='offset points',
                             va='top', ha='center')
        if max_d:
            plt.axhline(y=max_d, c='k')
    return ddata


def run_hierarchical(datalist, max_d, criteria ="ward"):
    my_list = [(x.name, -1) for x in datalist]
    X = [x.vector for x in datalist]
    print("Training hierarchical for max_d = "+str(max_d)+"...")
    Z = linkage(X, criteria)
    clusters = fcluster(Z, max_d, criterion="distance")
    for i in range(len(clusters)):
        my_list[i] = (my_list[i][0], clusters[i])
    return my_list



def run_hierarchical_with_plot(datalist, criteria='ward'):
    my_list = [(x.name, -1) for x in datalist]
    X = [x.vector for x in datalist]
    plot_X = []

    print("Generating selection for plotting dendogram")
    try:
        positions = sample(range(len(datalist)), 13000)
    except ValueError:
        positions = range(len(datalist))

    for p in positions:
        plot_X.append(X[p])

    sys.setrecursionlimit(10000)

    print("Training hierarchical for plot...")
    plot_Z = linkage(plot_X, 'ward')


    plt.title('Hierarchical Clustering Dendrogram (truncated)')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    max_d = 150
    fancy_dendrogram(
        plot_Z,
        truncate_mode='lastp',
        p=12,
        leaf_rotation=90.,
        leaf_font_size=12.,
        show_contracted=True,
        annotate_above=10,
        max_d=max_d
    )
    plt.show()

    try:
        max_d = str(input("Introduce new value for max_d"))
    except ValueError:
        pass

    print("Training hierarchical for max_d = " + str(max_d) + "...")
    Z = linkage(X, criteria)
    clusters = fcluster(Z, max_d, criterion="distance")

    for i in range(len(clusters)):
        my_list[i] = (my_list[i][0], clusters[i])

    return my_list