import pandas as pd
from sklearn.cluster import KMeans
from sklearn.manifold import MDS
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.shortcuts import render,HttpResponse
from random import *
import numpy as np
import base64


class cluster_class:

    def __init__(self):
        self.df = pd.read_csv("ClusterDash/static/ClusterDash/clustering_police_station.csv")
        self.df1 = pd.read_csv("ClusterDash/static/ClusterDash/charged_main_dataset.csv")

    def get_features(self):
        return list(self.df.columns.values)

    def make_cluster(self,k,charges_list):
        self.num_cl = k
        self.charges=charges_list
        self.km=KMeans(n_clusters=k).fit(self.df.loc[:,charges_list])
        self.clusters=self.km.labels_.tolist()
        self.df["cluster"] = self.clusters
        self.df.to_csv("ClusterDash/static/ClusterDash/clustering_police_station22.csv")

    def count_clusters(self):
        dfc = pd.DataFrame(self.df.cluster.value_counts().tolist(), index=self.df.cluster.value_counts().index, columns=["count"])
        dic =  dfc.to_dict()
        print(dic['count'])
        return dic['count']

    def top_features(self,k,charges_list):
        self.top_list=[]
        pd.crosstab(index=self.df1.pstation, columns=self.df1.group_charge)
        ordered_centroids = self.km.cluster_centers_.argsort()[:, ::-1]
        for i in range(k):
            self.top_list.append(self.df.loc[:, charges_list].columns[ordered_centroids[i, :4]].tolist())
        return self.top_list

    def give_lat_lon(self):
        df2 = pd.read_csv("ClusterDash/static/ClusterDash/clustering_police_station22.csv")
        arr = []
        for i,c in df2.iterrows():
            arr_dict = dict()
            arr_dict['lat']=c['lat']
            arr_dict['lng']=c['lon']
            arr_dict['cluster']=c['cluster']
            arr_dict['pstation']=c['pstation']
            for i in self.top_list[int(c['cluster'])]:
                arr_dict[i]=c[i]
            arr.append(arr_dict)
        print("LATTTTLONNNN")
        print(arr)
        return arr

    def random_color(self):
        letter = '0123456789ABCDEF'
        color = '#'
        for m in range(0, 6):
            color = color + letter[randint(0,15)]
        return color

    def plot_map(self):
        dist=1-cosine_similarity(self.df.loc[:,self.charges])
        mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)

        pos = mds.fit_transform(dist)
        xs, ys = pos[:, 0], pos[:, 1]

        cluster_colors = {}
        cluster_names = {}
        for i in range(0,self.num_cl):
            cluster_colors[i] = self.random_color()
            cluster_names[i] = "Cluster "+ str(i)


        # In[20]:

        #create data frame that has the result of the MDS plus the cluster numbers and titles
        self.df1 = pd.DataFrame(dict(x=xs, y=ys, label=self.clusters, pstation=self.df.pstation))

        #group by cluster
        groups = self.df1.groupby('label')


        # set up plot
        fig, ax = plt.subplots(figsize=(17, 9)) # set size
        ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling

        #iterate through groups to layer the plot
        #note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
        for name, group in groups:
            ax.plot(group.x, group.y, marker='o', linestyle='', ms=12,
                    label=cluster_names[name], color=cluster_colors[name],
                    mec='none')
            ax.set_aspect('auto')
            ax.tick_params(        axis= 'x',          # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom='off',      # ticks along the bottom edge are off
                top='off',         # ticks along the top edge are off
                labelbottom='off')
            ax.tick_params(        axis= 'y',         # changes apply to the y-axis
                which='both',      # both major and minor ticks are affected
                left='off',      # ticks along the bottom edge are off
                top='off',         # ticks along the top edge are off
                labelleft='off')

        ax.legend(numpoints=1)  #show legend with only 1 point

        #add label in x,y position with the label as the film title
        for i in range(len(self.df)):
            ax.text(self.df1.ix[i]['x'], self.df1.ix[i]['y'], self.df1.ix[i]['pstation'], size=8)

        canvas = FigureCanvasAgg(fig)
        response = HttpResponse(content_type='image/png')
        canvas.print_png(response)
        return response

    def give_row(self,place):
        diction_list = []
        df_list = self.df.values.T.tolist()
        ind = self.df[self.df['pstation'] == place].index.values.astype(int)[0]
        print(df_list[1][ind])
        i=0
        for col in self.df:
            diction = {}
            diction["charge"]=col
            diction["value"]= df_list[i][ind]
            diction_list.append(diction)
            i=i+1
        diction_list.pop(0)
        diction_list.pop(0)
        diction_list.pop()
        diction_list.pop()
        diction_list.pop()
        return (diction_list)




