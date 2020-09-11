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

    #step 1, np_arrays is a queue of np arrays
    def breakup_beaches(self, np_arrays):
        length = np_arrays.qsize()
        list = []
        while length > 0:
            outer = []
            inner = []
            while len(inner) < 3:
                if length == 0:
                    inner.append(self.shit_array)
                else:
                    inner.append(np_arrays.get())
                    length -=1
            outer.append(np.array(inner))
            list.append(np.array(outer))
        return list

    #step 2 and 3, for each 3d np array, get winner and put into queue
    def queue_beaches(self, list):
        q = queue.Queue()
        #rank each trio of beaches
        for array in list:
            out = self.pickle_model.predict(array.transpose(0,2,1).reshape(1,-1))
            win_idx = -1
            max_score = -1
            #get highest ranked beach
            for i in range(len(out[0])):
                if out[0][i] > max_score:
                    win_idx = i
                    max_score = out[0][i]
            #put highest ranked beach into queue
            q.put(array[0][win_idx])

        return q

    #step 4
    def narrow_down(self, array_queue):
        while array_queue.qsize() > 1:
            list = self.breakup_beaches(array_queue)
            array_queue = self.queue_beaches(list)
        #now perform the ML model one more time, and return ranking as JSON
        fin_list =self.breakup_beaches(array_queue)
        out = self.pickle_model.predict(fin_list[0].transpose(0,2,1).reshape(1,-1))
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
        #return json of the ranks
        return Response({
            'best': self.query_np(fin_list[0][0][max_idx]).id,
            'best_name': self.query_np(fin_list[0][0][max_idx]).name,
            'best_lat': self.query_np(fin_list[0][0][max_idx]).latitude,
            'best_lon': self.query_np(fin_list[0][0][max_idx]).longitude,

            'mid': self.query_np(fin_list[0][0][mid_idx]).id,
            'mid_name': self.query_np(fin_list[0][0][mid_idx]).name,
            'mid_lat': self.query_np(fin_list[0][0][mid_idx]).latitude,
            'mid_lon': self.query_np(fin_list[0][0][mid_idx]).longitude,

            'low': self.query_np(fin_list[0][0][low_idx]).id,
            'low_name': self.query_np(fin_list[0][0][low_idx]).name,
            'low_lat': self.query_np(fin_list[0][0][low_idx]).latitude,
            'low_lon': self.query_np(fin_list[0][0][low_idx]).longitude
        })

    #query beaches based on an np val
    def query_np(self, np_array):
        print(
        int(np_array[0]),
        int(np_array[1]),
        int(np_array[2]),
        float(np_array[3]),
        float(np_array[4]),
        int(np_array[5]),
        int(np_array[6]),
        int(np_array[7]),
        int(np_array[8]),
        float(np_array[9]),
        float(np_array[10])
        )
        return Beach.objects.get(
            beach_dir = int(np_array[0]),
            wind_speed = int(np_array[1]),
            wind_dir = int(np_array[2]),
            swell1_height = float(np_array[3]),
            swell2_height = float(np_array[4]),
            swell1_period = int(np_array[5]),
            swell2_period = int(np_array[6]),
            swell1_dir = int(np_array[7]),
            swell2_dir = int(np_array[8]),
            tide_height = float(np_array[9]),
            water_temp = float(np_array[10])
        )
