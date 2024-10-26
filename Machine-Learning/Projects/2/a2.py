import kmeans
import gmm
import gmm_skl
import pca
import pca_cluster
import q7
import hierachial
import q9

def runall():
    kmeans.main()
    gmm.main()
    gmm_skl.main()
    pca.main()
    pca_cluster.main()
    q7.main()
    hierachial.main()
    q9.main()

if __name__ == '__main__':
    runall()