import numpy as np
import math
import random
from scipy.optimize import minimize

def fun(args):
    x_input, y_input, target_x, target_y = args[0], args[1], args[2], args[3]
    count = len(x_input)
    v = lambda x: sum(
        (x[0] * x_input[i] + x[1] * y_input[i] + x[2] - target_x[i]) ** 2
        + (x[3] * x_input[i] + x[4] * y_input[i] + x[5] - target_y[i]) ** 2
        for i in range(count)
    )
    return v


def trans(file_path=r".\node_coord.csv"):
    rec_coord = {}
    rec_gps = {}
    with open(file_path, 'r') as f:
        f.readline()
        lines = f.readlines()
        for line in lines:
            lines = line.split(',')
            node_id = int(lines[0])
            rec_coord[node_id] = (float(lines[1]), float(lines[2]))
            if len(lines) == 5 and lines[3] != '' and lines[4] != '':
                rec_gps[node_id] = float(lines[3]), float(lines[4])
    if len(rec_gps) < 3:
        raise Exception("At least 3 coordinates of longitude and latitude are required")
    # if len(rec_gps) < 10:
    #     keys = [key for key in rec_gps.keys()]
    # else:
    keys = list(rec_gps.keys())
    x_input = [rec_coord[key][0] for key in keys]
    y_input = [rec_coord[key][1] for key in keys]
    target_x = [rec_gps[key][0] for key in keys]
    target_y = [rec_gps[key][1] for key in keys]
    args = [x_input, y_input, target_x, target_y]

    x0 = np.array([1, 1, 1, 1, 1, 1])
    res = minimize(fun(args), x0, method='SLSQP')

    trans_rec = {}
    trans_fun = lambda x,y:(res.x[0]*x+res.x[1]*y+res.x[2],res.x[3]*x+res.x[4]*y+res.x[5])

    for key in rec_coord:
        if key in keys:
            trans_rec[key] = rec_gps[key]
        else:
            trans_rec[key] = trans_fun(rec_coord[key][0], rec_coord[key][1])

    with open(r'./new_node_coord.csv', 'w+', newline='') as f:
        lines = []
        f.write('node_id,x_coord,y_coord,x_old,y_old,\n')
        for key in trans_rec:
            line = str.format(
                "{0},{1},{2},{3},{4}\n".format(key, trans_rec[key][1],trans_rec[key][0],rec_coord[key][0], rec_coord[key][1]))
            lines.append(line)
        f.writelines(lines)
    print('OK')


if __name__ == '__main__':

    file_path=r".\node_coord.csv"

    rec_coord = {}
    rec_gps = {}
    with open(file_path, 'r') as f:
        f.readline()
        lines = f.readlines()
        for line in lines:
            lines = line.split(',')
            node_id = int(lines[0])
            rec_coord[node_id] = (float(lines[1]), float(lines[2]))
            if len(lines) == 5 and lines[3] != '' and lines[4] != '':
                rec_gps[node_id] = float(lines[3]), float(lines[4])
    if len(rec_gps) < 3:
        raise Exception("At least 3 coordinates of longitude and latitude are required")

    # trans()