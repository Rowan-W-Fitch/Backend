import pickle
import numpy as np
import queue
from apis.models import Beach
from rest_framework.response import Response
import os
import sys
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
class MachineLearningModel():

    pickle_model = None
    with open(os.path.join(os.path.join(BD, 'ml'),'linear_reg.pkl'), 'rb') as file:
        pickle_model = pickle.load(file)

    shit_array = np.array([0, 50, 0, 0, 0, 0, 0, 2, 2, 0, 0, 10000])

    #step 1, beach_queue is a queue of Beach objects
    def breakup_beaches(self, beach_queue, lat, lng):
        length = beach_queue.qsize()
        list = []
        while length > 0:
            ids = []
            outer = []
            inner = []
            while len(inner) < 3:
                if length == 0:
                    inner.append(self.shit_array)
                    ids.append(-1)
                else:
                    bch = beach_queue.get()
                    inner.append(bch.to_np_array(lat, lng))
                    ids.append(bch.id)
                    length -=1
            outer.append(np.array(inner))
            list.append((ids, np.array(outer)))
        return list

    #step 2 and 3, for each 3d np array, get winner and put into queue
    def queue_beaches(self, list):
        q = queue.Queue()
        #rank each trio of beaches
        for tup in list:
            out = self.pickle_model.predict(tup[1].transpose(0,2,1).reshape(1,-1))
            win_idx = -1
            max_score = -1
            #get highest ranked beach
            for i in range(len(out[0])):
                if out[0][i] > max_score:
                    win_idx = i
                    max_score = out[0][i]
            #put highest ranked beach into queue
            win_id = tup[0][win_idx]
            if win_id > 0:
                bch = Beach.objects.get(id = win_id)
                q.put(bch)
        return q

    #step 4
    def narrow_down(self, beach_queue, lat, lng):
        while beach_queue.qsize() > 1:
            list = self.breakup_beaches(beach_queue, lat, lng)
            beach_queue = self.queue_beaches(list)
        #now perform the ML model one more time, and return ranking as JSON
        fin_list = self.breakup_beaches(beach_queue, lat, lng)
        out = self.pickle_model.predict(fin_list[0][1].transpose(0,2,1).reshape(1,-1))
        #vals and idxs
        max = -1
        max_idx = -1
        mid = -1
        mid_idx = -1
        low = -1
        low_idx = -1
        #get vals and idxs
        for i in range(len(out[0])):
            if out[0][i] > max:
                max = out[0][i]
                max_idx = i

        for i in range(len(out[0])):
            if out[0][i] > mid and out[0][i] != max:
                mid = out[0][i]
                mid_idx = i

        for i in range(len(out[0])):
            if out[0][i] < mid:
                low = out[0][i]
                low_idx = i
        #get three beaches
        top_id = fin_list[0][0][max_idx]
        mid_id = fin_list[0][0][mid_idx]
        low_id = fin_list[0][0][low_idx]
        #start three bchs as none
        top_bch = None
        mid_bch = None
        low_bch = None
        #query them if the id no is valid
        if top_id > 0:
            top_bch = Beach.objects.get(id = top_id)
        if mid_id > 0:
            mid_bch = Beach.objects.get(id = mid_id)
        if low_id > 0:
            low_bch = Beach.objects.get(id = low_id)
        #return json of the ranks
        return Response({
            'best_name': top_bch.name if top_bch else "none",
            'best_lat':top_bch.latitude if top_bch else "none",
            'best_lon': top_bch.longitude if top_bch else "none",

            'mid_name': mid_bch.name if mid_bch else "none",
            'mid_lat': mid_bch.latitude if mid_bch else "none",
            'mid_lon': mid_bch.longitude if mid_bch else "none",

            'low_name': low_bch.name if low_bch else "none",
            'low_lat': low_bch.latitude if low_bch else "none",
            'low_lon': low_bch.longitude if low_bch else "none"
        })
