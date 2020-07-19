# about lostory repo
lostory means lost-history, it is a simple python script to get any website history from 3 different sources (commoncrawl, wayback machine, alienvault )

# what the tool generate?
it will generates some files as a result
  - result.html&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;=> arranged styled urls can open in the browser
  - result.js&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;=> all unique js files(you can download all the list and analyze it)
  - fuzz.txt&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;=> all unique urls with its parameters(FUZZ)
  - fuzz_uniq.txt&nbsp;&nbsp;=> only all unique query

# usage
  - python lostory.py example.com


# if you have a list of urls and want to analyze the urls.
  - python histlyzer.py urls.txt saving_dir_name
