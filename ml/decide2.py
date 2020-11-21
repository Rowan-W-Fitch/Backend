import pickle
import numpy as np
import queue
from apis.models import Beach
from rest_framework.response import Response
import os
import sys
import json
from rest_api_server.settings import BASE_DIR as BD
#the purpose of this file is to use the saved ML model to decide which beach to surf at
#inputs: an np array of beaches
#output: top 3 beaches to surf at

"""
steps:
1) take the np array of beaches, and break it into a list of 3d np arrays [ [ [ [b1], [b2], [b3] ] ], [ [ [b4], [b5], [b6] ] ], ...]
NOTE if the number of beaches % 3 != 0, then just add dummy beaches that are guarantered not to be chosen

2)for each 3d np array, apply to model and take the winner

3) place the winners into new 3d np arrays

4) repeat 2 and 3 until there is only one 3d np array

5) return the id's of the beaches, in rank via a JSON response

"""
class MachineLearningModel2():

    pickle_model = None
    with open(os.path.join(os.path.join(BD, 'ml'),'linear_reg.pkl'), 'rb') as file:
        pickle_model = pickle.load(file)

    shit_array = np.array([0, 50, 0, 0.1, 1.2, 2, 2, 2, 2, 100])

    #step 1, beach_queue is a queue of Beach objects
    def breakup_beaches(self, beach_queue, lat, lng):
        length = beach_queue.qsize()
        if length == 0:
            return None
        list = []
        outer = []
        ids = []
        while length > 0:
            inner = []
            while len(inner) < 3:
                if length == 0:
                    inner.append(self.shit_array)
                    ids.append(-1)
                else:
                    bch = beach_queue.get()
                    print(bch.name)
                    inner.append(bch.to_np_array(lat, lng))
                    ids.append(bch.id)
                    length -=1
            outer.append(np.array(inner))
        list.append((ids, np.array(outer)))
        return list

    #step 2 and 3, for each 3d np array, get winner and put into queue
    def get_ranks(self, beach_queue, lat, lng):
        list = self.breakup_beaches(beach_queue, lat, lng)
        if not list:
            return Response({
                json.dumps([])
            })
        #rank the beaches
        length = len(list[0][1])
        out = self.pickle_model.predict(list[0][1].transpose(0,2,1).reshape(length,-1))
        out = out.flatten()
        #get top3
        ids = []
        while len(out) > 0 and len(ids) < 3:
            max_idx = np.argmax(out)
            if list[0][0][max_idx] > 0:
                ids.append(list[0][0][max_idx])
                del list[0][0][max_idx]
            out = np.delete(out, max_idx)
        #get the beach objects
        arr = []
        for id_no in ids:
            bch = Beach.objects.get(id = id_no)
            arr.append({
                'name': bch.name,
                'lat': str(bch.latitude),
                'lon': str(bch.longitude)
            })
        #return arr in response
        json_arr = json.dumps(arr)
        return Response({
            json_arr
        })
