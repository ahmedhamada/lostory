# -*- coding: utf-8 -*-
#!/bin/python

'''
-generate fuzzing urls params
-generate js urls file
-generate graphical 
-grap content from 3 sources (commoncrawl + waybackmachine + alienvalut)

#later: google with proxies, 

https://medium.com/@vbsreddy1/unboundlocalerror-when-the-variable-has-a-value-in-python-e34e097547d6
'''

import json
import requests
import os
import sys
import time
from threading import Thread
import threading
import random
import Queue
from random import uniform
import math

start = time.time()

print("""
█   █▀█ █▀ ▀█▀ █▀█ █▀█ █▄█
█▄▄ █▄█ ▄█  █  █▄█ █▀▄  █ v1
░░░ coded by ahmed hamada. ░░░
""")

Red       = '\033[0;31m'
Green     = '\033[0;32m'
Yellow    = '\033[0;33m'
Color_Off = '\033[0m'  # Text Reset

folder = 'lostory_results/'

#verify providing
if len(sys.argv) >= 2:
    target = sys.argv[1]
else:
    exit("provide domain: python " + sys.argv[0] + ' example.com' )

#create if folder not exists
if os.path.isdir(folder) == False:
    os.mkdir(folder,0755)

#create if folder not exists
if os.path.isdir(folder+target) == False:
    os.mkdir(folder+target,0755)

#verify it created!
if os.path.isdir(folder) == False:
    print('failed to create a folder to save the result\n permisions denied.\n eixt')
    quit()

def count_text_lines(res):
    count_lines=0
    for line in res:
        if "\n" in line:
            count_lines = count_lines + 1
    return str(count_lines)

#commoncrawl save data
def save_data(req_commoncrawl,filename):
    try:
        # print(req_commoncrawl)
        commoncrawl_data = req_commoncrawl.text.split("\n")[:-1]
        z = open(folder +target+'/'+str(filename), "a")
    except:
        pass
    # z = open(folder + 'big_result_commoncrawl_file', "a") # same file
    for entry in commoncrawl_data:
        try:
            url = json.loads(entry)['url']
            z.write(str(url)+"\n" )
        except:
            pass
    z.close()



# == archieve ==
sys.stdout.write('loading...')
sys.stdout.flush()
req_archieve = requests.get('http://web.archive.org/cdx/search/cdx?url=*.'+target+'./*&output=text&fl=original&collapse=urlkey')
#save result
f = open(folder+target+'/'+ "archieve.com.txt", "w")
f.write(req_archieve.text)
f.close()
try:
    sys.stdout.write('\b\b\b\b\b\b\b\b\b\b')
    sys.stdout.flush()
    print('[+] archieve lines:'+ count_text_lines(req_archieve.text) )
except:
    pass



# == commoncrawl ==#
q = Queue.Queue()

is_commoncrawl_blocked = True
while is_commoncrawl_blocked == True:
    try:
        req_commoncrawl_sources= requests.get('https://index.commoncrawl.org/collinfo.json')
        sources = json.loads(req_commoncrawl_sources.text)
        is_commoncrawl_blocked=False
    except:
        print('commoncrawl maybe blocked you   -   wait and i will try again   -  return response: \n'+req_commoncrawl_sources.text)
        is_commoncrawl_blocked=True
    time.sleep(2)


#put in queue
for value in sources:
    q.put("http://index.commoncrawl.org/"+str(value['id'])+"-index?url="+target+"/*&output=json")

retry_number=0
def run():
    global retry_number
    global q 
    while not q.empty():
        url=q.get()
        try: # if error happen(timeout ,etc) , var res will not be defined 
            res=(requests.get(url, timeout=20, verify=False) )
            exception_error = False
        except:
            exception_error = True
            print('----- timeout -----')

        if exception_error == True:
            if retry_number < 100:
                retry_number += 1
                q.put(url)
                continue
        else:
            if int(res.status_code) >= 500 and retry_number < 150 :
                retry_number +=1
                q.put(url)
                continue

        save_data(res , time.time())
        time.sleep(uniform(0.0001,0.02))
        if int(res.status_code) == 200 and q.qsize() > 0:
            print(Green +'  [+] queue size: ' + str(q.qsize() )+' => status_code: '+str(res.status_code ) + Color_Off )
        elif int(res.status_code) != 200 and q.qsize() > 0:
            print(Red+'  [+] queue size: ' + str(q.qsize() )+' => status_code: '+str(res.status_code ) + Color_Off )
    time.sleep(0.5) # more is better
    q.task_done()


# = threading =
threads = []
for i in range(22):
    thread = threading.Thread(target=run)
    threads.append(thread)
    thread.start()
    # print("Current Thread count: %i." % threading.active_count())
for thread in threads:
    thread.join()

print('- retries number: '+str(retry_number) + '\n')


# == alien vault ==
for i in range(0,1):
    url = 'https://otx.alienvault.com/api/v1/indicators/hostname/'+target+'/url_list?limit=50&page='+str(i)

    req_alien = requests.get(url)
    alien_decoded = json.loads(req_alien.text)
    
    # analyze  or  exit if no result
    alien = open(folder +target+'/'+'alien.txt',"a")
    if target in req_alien.text:
        for key in alien_decoded['url_list']:
            try:
                alien.write(str(key['url'])+'\n')
                # alien_exit=0
            except:
                pass
    else:
        print('\n=> fully retrieved results for alien \n')
        break
    print('[+] extracting from alienvault - '+ str(len(alien_decoded['url_list'])) + ' url extracted ' )

#collect all data into one file
full_folder=folder+target+"/" 

generate_all_text="cat "+ full_folder+"* | sort | uniq > "+full_folder+"all.txt"

os.system(generate_all_text)

print('\n=> script finished fetching from sources....start analyzing script histliszer.py :) \n')

res=os.system("python histlyzer.py "+full_folder+"all.txt" + " " + target)

os.system('rm '+ full_folder+"1*")

seconds = int(time.time()  - int(start))
print('script take: ' + str(seconds) + ' seconds')