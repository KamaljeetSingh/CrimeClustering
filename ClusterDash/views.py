from django.shortcuts import render,HttpResponse
from ClusterDash.ML.ClusterDash import Clustering
import pickle
import json
# Create your views here.

def cluster_home(request):

    if 'pie_sub' in request.POST:
        cl_ob = Clustering.cluster_class()
        k = int(request.POST.get('nocluster'))
        charges_list = request.POST.getlist('charges')
        print(charges_list)
        cl_ob.make_cluster(k,charges_list)
        c = cl_ob.count_clusters()
        top = cl_ob.top_features(k,charges_list)
        features_all = cl_ob.get_features()
        points = cl_ob.give_lat_lon()
        features_all.pop(0)
        features_all.pop(0)
        features_all.pop()
        features_all.pop()
        features_all.pop()
        print(points)
        # pickle object
        save_obj = open("cluster_obj.pickle", "wb")
        pickle.dump(cl_ob, save_obj)
        save_obj.close()
        return render(request, 'ClusterDash/Cluster_html.html', {'features': features_all , 'cl_count':c , 'flag':1,
                                                                 'top':top, 'k':k, 'points':points})

    if 'pic_img' in request.POST:
        cl_ob_pickle = open("cluster_obj.pickle", "rb")
        cl_ob = pickle.load(cl_ob_pickle)
        cl_ob_pickle.close()
        print(cl_ob.clusters)
        return cl_ob.plot_map()

    if request.is_ajax():
        place = request.POST.get('text')
        cl_ob_pickle = open("cluster_obj.pickle", "rb")
        cl_ob = pickle.load(cl_ob_pickle)
        cl_ob_pickle.close()
        # print(cl_ob.give_row(place))
        data_list = cl_ob.give_row(place)
        print("In views")
        print(data_list)
        return HttpResponse(json.dumps(data_list),content_type="application/json")


    cl = Clustering.cluster_class()
    features_all = cl.get_features()
    features_all.pop(0)
    features_all.pop(0)
    features_all.pop()
    features_all.pop()
    cl.give_row("CIVIL LINES")
    points = 20
    return render(request, 'ClusterDash/Cluster_html.html', {'features': features_all, 'flag':0, 'points':points})

