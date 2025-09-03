import pickle as pkl 
import numpy as np

with open('finished_teams_dict.pkl', 'rb') as f:
    teams_dict = pkl.load(f)

with open('finished_top1000.pkl', 'rb') as f: 
    top1000 = pkl.load(f) 


print(top1000)
