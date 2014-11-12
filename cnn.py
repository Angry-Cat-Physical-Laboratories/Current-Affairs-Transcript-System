def get_html(url):
    ''' Return the HTML content from the page at specified URL'''
    import urllib.request
    f = urllib.request.urlopen(url)
    html = f.read().decode("utf-8")
    f.close()
    return html

def get_inside_string(string, start, end):
	''' Return the substring beginning with start and ending with end'''
    start_index = string.index(start) + len(start)
    end_index = string.index(end)
    result = string[start_index:end_index]
    return result

def get_dated_transcript_links(date):
    ''' Return a list of of all transcripts posted by CNN on a specific date'''
    import datetime
    datestring = str(date.year) + '.' + str(date.month) + '.' + str(date.day)
    url = "http://transcripts.cnn.com/TRANSCRIPTS/" + datestring + ".html"
    links = get_all_links_from_page(url)
    return links

def get_dated_transcripts(date):
    urls = get_dated_transcript_links(date)

    # For each trasncript page listed for that date
    for url in urls:
	html = get_html(url)
	transcript_array = extract_content(html)

	# Identifies the longest string
	# Since the helper function returns every transcript-like HTML section,
	# and the HTML section containing all of the words said will always be the longest string,
	# by locating the longest string, we can avoid complicated string operations
	longest_string = 0
	index = 0
	for i in range(len(transcript_array)):
	    if(len(transcript_array[i][1]) > longest_string):
		longest_string = len(transcript_array[i][1])
		index = i

	body = transcript_array[index][1]

def get_transcript_links(url):
    '''Return a list of every transcript link found on a specified page'''
    html = get_html(url)
    body_start = '''<P><a href="/TRANSCRIPTS/" class="cnnTransProv">Return to Transcripts main page</a></P>'''
    body_end = '''<!-- /Content -->'''
    body = get_inside_string(html, body_start, body_end)    
    
    link_start = '''<a href="/TRANSCRIPTS/'''
    link_end = '''".html">'''
    links = []
    
    body_broken_by_link = body.split(link_start)
    
    # Extracts the actual transcript names
    for body_segment in body_broken_by_link:
        end_of_url = body_segment.index('"')
        url_section = body_segment[:end_of_url]
        url = "http://transcripts.cnn.com/TRANSCRIPTS/" + url_section
        links.append(url)
    
    # Removes stuff that aren't actually links
    indices_to_remove = []
    for i in range(0, len(links)):
        if(links[i].find("html") < 0):
            indices_to_remove.append(i)
    
    items_removed = 0
    for index_to_remove in indices_to_remove:
        links.pop(index_to_remove - items_removed)
        items_removed += 1
        
    return links   
    

def extract_content(page):
    ''' Extract the trancript text from a specified page, assumed to be valid'''
    start_string = '''<P><a href="/TRANSCRIPTS/" class="cnnTransProv">Return to Transcripts main page</a></P>'''
    end_string = '''<!-- /Content -->'''
    body = get_inside_string(page, start_string, end_string)
    
    # Sanitizes text
    text_to_remove = ["\t","&nbsp; "]
    for char in text_to_remove:
        body = body.replace(char, "")
        
    lines = body.split("\n")
    lines = remove_empty_items(lines)[:5]
    
    content = []
    
    for line in lines:
        line = line.replace("<br>", "\n")
        
        line_content = [get_inside_string(line, '="', '">'),get_inside_string(line, ">","</")]
        content.append(line_content)
        
    print(content)
    
def remove_empty_items(list):
    ''' Remove any empty items from the given list of strings'''
    indices_to_remove = []
    for i in range(0, len(list)):
        if(list[i] == ''):
            indices_to_remove.append(i)
    
    items_removed = 0
    for index_to_remove in indices_to_remove:
        list.pop(index_to_remove - items_removed)
        items_removed += 1
        
    return list