import requests
import json


# cail  -- 1, check --2

error_limit = 1 # pixel
def equl_with_error(pos1, pos2):
    if(len(pos1) != len(pos2)):
        return 0
    else:
        for i in range(0,len(pos1)):
            if(abs(pos1[i]-pos2[i]) > error_limit):
                return 0
    return 1
# find elements in list1 but not in list2
def find_difference(list1,list2):
    difference = []
    for pos1 in list1:
        # flag - also in list2
        flag = 0
        for pos2 in list2:
            if(equl_with_error(pos1, pos2)):
                flag = 1
        if(flag == 0):
            to_be_add = []
            for i in range (0,len(pos1)):
                to_be_add.append(int(pos1[i]))
            difference.append(to_be_add)
    return difference

# basic info of the server
server_address = '192.168.1.54'
headers = {'content-type':'application/json'}

# open GPIO
def GPIO_start():
    payload = {}
    r =  requests.post('http://'+server_address+':18888/server_func/GPIO_start', data=json.dumps(payload), headers=headers)
    return (r.json()['result'])


# close GPIO
def GPIO_clean():
    payload = {}
    r =  requests.post('http://'+server_address+':18888/server_func/GPIO_clean', data=json.dumps(payload), headers=headers)
    return (r.json()['result'])

# check a special pattern
def look(smf_num, cali_or_check):
    payload = { 'smf_num':smf_num, 'cali_or_check':cali_or_check }
    r =  requests.post('http://'+server_address+':18888/server_func/look', data=json.dumps(payload), headers=headers)
    pos = r.json()['pos']
    pointNum = r.json()['pointNum']
    return pos, pointNum

# get standard ledlist from PCB_config.py
def get_st_ledlist():
    payload = {}
    r =  requests.post('http://'+server_address+':18888/server_func/st_ledlist', data=json.dumps(payload), headers=headers)
    return (r.json()['st_ledlist'])

# get length of smf
def get_smf_len():
    payload = {}
    r =  requests.post('http://'+server_address+':18888/server_func/smf_len', data=json.dumps(payload), headers=headers)
    return (r.json()['smf_len'])

# upload new ledlist
def upload_new_ledlist(new_ledlist):
    payload = {'new_ledlist': new_ledlist}
    r =  requests.post('http://'+server_address+':18888/server_func/upload_new_ledlist', data=json.dumps(payload), headers=headers)
    return (r.json()['result'])

# get special frame
def get_frame(smf_num, cali_or_check):
    payload = { 'smf_num':smf_num, 'cali_or_check':cali_or_check }
    r = requests.post('http://'+server_address+':18888/server_func/get_frame', data=json.dumps(payload), headers=headers)
    img = r.json()['frame']
    frame = img.decode('base64')
    tmp_frame = open('/tmp/frame.png','w')
    tmp_frame.write(frame)
    tmp_frame.close()
    return 'frame got'

# advanced settings interface
def set_ads(neo_low, neo_high, neo_test_num):
    payload = {'ads_num': 0, 'neo_low': neo_low, 'neo_high':neo_high}
    r = requests.post('http://'+server_address+':18888/server_func/set_ads', data=json.dumps(payload), headers=headers)
    low = r.json()['low']
    high = r.json()['high']
    payload = {'ads_num': 1, 'neo_test_num': neo_test_num}
    r = requests.post('http://'+server_address+':18888/server_func/set_ads', data=json.dumps(payload), headers=headers)
    times = r.json()['test_num']
    return low, high, times

def get_ads():
    payload = {'ads_num': 0}
    r = requests.post('http://'+server_address+':18888/server_func/get_ads', data=json.dumps(payload), headers=headers)
    low = r.json()['low']
    high = r.json()['high']
    payload = {'ads_num': 1}
    r = requests.post('http://'+server_address+':18888/server_func/get_ads', data=json.dumps(payload), headers=headers)
    times = r.json()['test_num']
    return low, high, times
