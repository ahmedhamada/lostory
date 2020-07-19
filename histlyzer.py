#!/bin/bash

import os
import urllib
from urlparse import urlparse
import sys
import time
import math

start = time.time()

'''

# exported files

result.html => arranged urls can open in the browser
result.js   => all uniq js files(request and download all js and analyze it)
fuzz.txt    => all uniq urls with its parameters(FUZZ)

'''

#1 config => result.html
not_important_extentions = ['.png','.jpg','.jpeg','.svg','.css','gif','.woff2','.woff','.eot','.ttf','.js']
show_js_with_parameters  = True

#2 config => result.js
skip_js=['.min.js','jquery.js']

#3 config => fuzz.txt
skip_js_extention = ['.png','.jpg','.css','.js','.svg','.woff','.ttf','.jpeg','.eot','.eot']
skip_parameters   = ['parameter_name','ref']


saving_place='lostory_results/'


#create saving place it not exits
if os.path.isdir(saving_place) == False:
	os.system('mkdir '+saving_place)

# argument-1 :provide a file to analyze
if len(sys.argv) > 1:
	history_file=sys.argv[1]
	if os.path.isfile(history_file) == False:
		exit('file you provide: '+ history_file +' not exist..exit!')
else:
	print("provide a file to analyize \nex: python "+sys.argv[0]+ ' urls_to_analyze.txt saving_directory \nor enter your file path here:')
	history_file=raw_input()

#verify provided file exists
if os.path.isfile(history_file) == False:
    exit('file: '+ history_file +' not exit :(')

# argument-2 :saving place =>  provide the file
if len(sys.argv) > 2:
	domain_folder = sys.argv[2]
else:
	#provide second value
	print("provide a directory to save the result \nex: python " + sys.argv[0] + ' urls.txt saving_directory_name \nor enter your custom directory here:')
	domain_folder=raw_input()

if domain_folder == "":	
	#random name
	domain_folder=str(time.time()).split('.')[0]
	os.system('mkdir '+ saving_place +domain_folder)
else:
	pass
	os.system('mkdir '+ saving_place +domain_folder +' 2> /dev/null')

full_folder_saving_place = saving_place+domain_folder+'/'

print('- - - - - - - - - - - - - - - - - - - - - - - - - -')
print('analyzing file : '+history_file)
print('- - - - - - - - - - - - - - - - - - - - - - - - - -')
print('saving place : '+full_folder_saving_place)
print('- - - - - - - - - - - - - - - - - - - - - - - - - -\n')

#open provided history file
f=open(history_file,'r')

total_history_lines = len(open(history_file).readlines(  ))


def colored_counter(text):
	return '<span style=" background-color: #ff5a5a; border-radius: 7px; padding: 2px;">'+str(text)+'</span>'

def progress(now, total):
	global my_progress
	try:
		my_progress = int(my_progress)
	except:
		my_progress = int(1) # initial value
		my_progress = int(my_progress)

	now = math.floor(now) / total * 100
	now = int (now) # from float to int

	if  my_progress < now :
		my_progress +=1
		sys.stdout.write("\b\b\b"+"#")
		sys.stdout.write(str(now).zfill(2)+"%")  # 00 representation
		sys.stdout.flush() # print it now
	if my_progress >= 99:
		my_progress = 1


print('1- generate html file')
#===================================

finished_url  = []
finished_path = set()
hirarcy_urls  = {}

html_result   = open(full_folder_saving_place+'result.html','w')

f.seek(0)

skip_extention = False
index          = 0

for line in f:
	
	index +=1
	progress(index, total_history_lines)
	
	line  = line.replace('\n','')
	parse = urlparse(line)

	scheme = parse.scheme
	tld    = parse.netloc
	path   = parse.path
	query  = parse.query

	# new subdomain
	if  tld  not in finished_url:
		hirarcy_urls[tld] = []
		finished_url.append( tld ) # new parent	
	# existed subdomain
	
	else:  	
	
		# is contain js ?
		if show_js_with_parameters == True  and  '.js' in line:
			#show js if have params
			if parse.query == "":
				skip_extention=True
			else:
				skip_extention=False

		#skip not important extention(png,jpg,....)
		for ex in not_important_extentions: 
			if ex in line:
				skip_extention=True

		if skip_extention == True:
			skip_extention=False #reset the value
			continue
		
		#child to an exist parent + based on path
		if path not in finished_path:
			hirarcy_urls[tld].append(  line  ) 
			finished_path.add(line + query ) # error here - became error when became bigger

def count_urls_number(subdomain):
	length = len(subdomain)
	if int(length) < 1:
		return ''
	else:
		return '<span style="margin-left: 20px; background-color: gold; border: 1px solid;">' + str(length) + '</span>'

html_result.write("""
<link href="https://drive.google.com/uc?export=view&id=1_9xMyPQNOzl0OITZe1BJf8R73U22KYLc" rel="stylesheet" type="text/css" />
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<style>
.parent {
    background-color: green;
}
.hidden{
	display:none;
}
*{
	font-size:13px;
}
</style>
""")
html_result.write('</head><body>')
html_result.write('<h1>result: </h1>')
html_result.write("<ul class=\"tree\">")

for url_item in hirarcy_urls:
	html_result.write('<li class="parent-li" ><a class="parent" onsad="hideChildren()" '+ url_item +'>  parent: '+ url_item + str(count_urls_number(hirarcy_urls[url_item]))  +  '</a><ul>')
	
	for i in hirarcy_urls[url_item]:
		html_result.write('<li class="submenu"><a target="_blank" href="'+ i +'">'+ i +'</a></li>')  # child
	html_result.write('</ul></li>')
html_result.write("""
<script>
//collapse later
</script>
""")

html_result.write("</ul></body></html>")
html_result.close()



print('\n2- start analyzing js')
#====================================

#2 generate_uniq_js_file
url_w_path=[]

f.seek(0)

js_f=open(full_folder_saving_place+'result.js','w')

skip=False
index = 0
for line in f:
	index +=1
	progress(index , total_history_lines)
	line = line.replace('\n','')
	parse=urlparse(line)

	scheme = parse.scheme
	tld    = parse.netloc
	path   = parse.path
	query  = parse.query
	
	# skip if not js
	if ".js" not in line:
		continue

	# skip files
	for i in skip_js:
		if i in line:
			skip=True
			continue

	if skip ==True:
		skip=False #reset
		continue

	# skip if already saved
	if tld +'/'+path not in url_w_path:
		url_w_path.append(tld +'/'+path)
		js_f.write(tld +'/'+path +'\n' )
js_f.close()


print('\n3-generate fuzzing files')
#======================================

def generate_params_without_values(params_with_values):
	all_params_name={}
	splited_with_and_sign = params_with_values.split('&')
	for i in splited_with_and_sign:
		splited_with_equal_sign=i.split('=')
		all_params_name[splited_with_equal_sign[0]]='FUZZ'
	return(urllib.urlencode(all_params_name))


fuzz_file      = open(full_folder_saving_place+'fuzz.txt','w')
fuzz_uniq_file = open(full_folder_saving_place+'fuzz_uniq.txt','w')

already_saved_url_with_no_value_query = set()
already_saved_params_and_value        = set()

f.seek(0)


#3 uniq url + params  => fuzz.txt
#4 uniq parms         => fuzz_uniq.txt
index = 0
for line in f:
	index +=1
	progress(index , total_history_lines)
	
	line   = line.replace('\n','')
	parse  = urlparse(line)

	scheme = parse.scheme
	tld    = parse.netloc
	path   = parse.path
	query  = parse.query

	if query == "":
		continue

	#skip extention
	for extention in skip_js_extention:
		if extention in path:
			skip=True
			break

	# skip parameters
	for param in skip_parameters:
		if param+'=' in generate_params_without_values(query):
			skip=True
			break

	if skip == True:
		skip=False  # reset
		continue

	full_url_without_fixed_params= scheme +'://'+ tld + path + '?' + generate_params_without_values(query)

	if full_url_without_fixed_params not in already_saved_url_with_no_value_query:
		already_saved_url_with_no_value_query.add(full_url_without_fixed_params)
		fuzz_file.write(full_url_without_fixed_params+'\n')
		full_params = generate_params_without_values(query)

	if full_params not in already_saved_params_and_value:
		already_saved_params_and_value.add(full_params)
		fuzz_uniq_file.write(full_url_without_fixed_params+'\n')

js_f.close()


print('\nfinished :)')