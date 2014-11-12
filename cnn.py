def get_html(url):
    import urllib.request
    f = urllib.request.urlopen(url)
    html = f.read().decode("utf-8")
    f.close()
    return html

def get_inside_string(string, start, end):
    start_index = string.index(start) + len(start)
    end_index = string.index(end)
    result = string[start_index:end_index]
    return result

def get_today_transcript_links():
    today_url = get_today_transcript_page()
    links = get_all_links_from_page(today_url)
    return links

def get_today_transcript_page():
    import datetime
    datestring = str(datetime.date.today().year) + '.' + str(datetime.date.today().month) + '.' + str(datetime.date.today().day)
    url = "http://transcripts.cnn.com/TRANSCRIPTS/" + datestring + ".html"
    return url

def get_all_links_from_page(url):
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
    import urllib.request
    f = urllib.request.urlopen(url)
    html = f.read().decode("utf-8")
    f.close()
    return html

def get_inside_string(string, start, end):
    start_index = string.index(start) + len(start)
    end_index = string.index(end)
    result = string[start_index:end_index]
    return result

def get_today_transcript_links():
    today_url = get_today_transcript_page()
    links = get_all_links_from_page(today_url)
    return links

def get_today_transcript_page():
    import datetime
    datestring = str(datetime.date.today().year) + '.' + str(datetime.date.today().month) + '.' + str(datetime.date.today().day)
    url = "http://transcripts.cnn.com/TRANSCRIPTS/" + datestring + ".html"
    return url

def get_all_links_from_page(url):
    # Removes web formatting
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
    indices_to_remove = []
    for i in range(0, len(list)):
        if(list[i] == ''):
            indices_to_remove.append(i)
    
    items_removed = 0
    for index_to_remove in indices_to_remove:
        list.pop(index_to_remove - items_removed)
        items_removed += 1
        
    return list