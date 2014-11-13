# Functions which may be of interest to a user/developer
import linguistics

def get_descriptors_from_transcripts(transcript_dictionary):
      
    mass_text = ""
    for url in transcript_dictionary:
        mass_text += "\n" + transcript_dictionary[url]
    sentence_lists = get_sentence_lists(mass_text)
    semantic_descriptors = build_semantic_descriptors(sentence_lists)
    return semantic_descriptors
    

def get_dated_transcripts(date):
    urls = get_dated_transcript_links(date)

    # Dictionary containing the transcripts for a given date
    # [URL] = BODY
    transcript_dictionary = {}

    # For each trasncript page listed for that date
    for url in urls:
        transcript_array = get_transcript(url)

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
                
        # The body of the transcript given by url
        body = transcript_array[index][1]
        transcript_dictionary[url] = body
    return transcript_dictionary
    

def get_transcript(url):
    ''' Extract the trancript text from a specified page, assumed to be valid'''
    
    page = get_html(url)
    
    start_string = '''<P><a href="/TRANSCRIPTS/" class="cnnTransProv">Return to Transcripts main page</a></P>'''
    end_string = '''<!-- /Content -->'''
    body = get_inside_string(page, start_string, end_string)
    
    # Sanitizes text
    text_to_remove = ["\t","  "]
    for char in text_to_remove:
        body = body.replace(char, "")
        
    lines = body.split("\n")
    lines = remove_empty_items(lines)[:5]
    
    content = []
    
    for line in lines:
        line = line.replace("<br>", "\n")
        
        line_content = [get_inside_string(line, '="', '">'),get_inside_string(line, ">","</")]
        content.append(line_content)
    return content
    


# Helper functions dealing with transcript internals

def get_dated_transcript_links(date):
    ''' Return a list of of all transcripts posted by CNN on a specific date'''
    import datetime
    datestring = str(date.year) + '.' + str(date.month) + '.' + str(date.day)
    url = "http://transcripts.cnn.com/TRANSCRIPTS/" + datestring + ".html"
    links = get_transcript_links(url)
    return links

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

# Back-end / helper functions
#  Web operations, string operations
def get_html(url):
    ''' Return the HTML content from the page at specified URL'''
    import urllib.request
    f = urllib.request.urlopen(url)
    html = f.read().decode("utf-8")
    f.close()
    return html

def get_inside_string(string, start, end):
    ''' Return the substring beginning with start and ending with end
            Exclusive, i.e. the returned string does not include the start or end substrings'''
    start_index = string.index(start) + len(start)
    end_index = string.index(end)
    result = string[start_index:end_index]
    return result

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

# Most of this forked (i.e. shamelessly stolen) from Assignment #2

def get_sentence_lists(text):
    ''' Return a list (of sentences) of lists (words in each sentence) for a given string. Makes a few a
        assumptions about the properties of the text -- most of which can be modified within the function itself.

        Input Information:
        2 input parameters: ( <body of text file> ) 
        <body of text file> -- String, containing the full text of all textual documents to be analyzed.
        
        Output Information:
        - Return a list of sentances, each sentance is in turn a list of all words within that sentance
                Note that the text file is stripped of all high ASCII character
                Sentances are delimited by ? ! .
                Words are split by spaces or , - -- : ; ' ""        
    '''


    # If there is no text, e.g. if there were no valid files opened
    if(text == ""):
        return []

    # Removes all word wrapping
    text = text.replace('\n', ' ')

    # Applies basic text formatting
    text = text.lower()

    # Replaces non-delimiter punctuation with a space
    # e.g. so that "school's" becomes "school s"
    #print("Removing punctuation...")
    punctuation = [',', '-', '--', ':', ';', "'", '''"''']

    for a_punctuation in punctuation:
        text = text.replace(a_punctuation, ' ')
  
    # Replaces all sentence delimiters with a period
    #print("Adding sentence delimiters...")
    sentence_delimiters = ['?', '!']
    
    for delimiter in sentence_delimiters:
        text = text.replace(delimiter, '.')

    # Splits on the delimiter
    #print("Splitting sentences...")
    sentences = text.split('.')

    # Strips any characters we do not want to have in
    # any of our analyzed text (e.g. high ASCII)
    #print("Removing high ASCII character...")
    lower = 97
    upper = 122
    for sentence_index in range (0, len(sentences)):
        for ascii_index in range(0, 255):
            if (((ascii_index < lower) or (ascii_index > upper)) and (not ascii_index == 32)):
                sentences[sentence_index] = sentences[sentence_index].replace(chr(ascii_index), ' ')
    
    # Splits each sentence by word
    #print("Splitting sentences by word...")
    sentences_as_lists = []
    for sentence in sentences:
        sentence_list = sentence.split()
        sentences_as_lists.append(sentence_list)

    # Removes empty lists
    #print("Identifying empty lists...")
    lists_to_remove = []
    for i in range(0, len(sentences_as_lists)):
        if(sentences_as_lists[i] == []):
            lists_to_remove.append(i)
    #print("Removing empty lists...")
    #print("Must remove", len(lists_to_remove),"empty lists.")
    
    lists_removed = 0
    for list_to_remove in lists_to_remove:
        #print("Lists remaining to be removed:", (len(lists_to_remove) - lists_removed))
        sentences_as_lists.pop(list_to_remove - lists_removed)
        lists_removed += 1
    # print("All sentence lists prepared!")

    return sentences_as_lists

def build_semantic_descriptors(sentences):
    '''This function will build a dictionary of semantic descriptors using a list of lists of words.

       Input Information:
       1 input parameter: (<sentences>)
       
       <sentences> --- Array, This input must be a list that contains lists of word from English sentences.
                       Each sub list must represent a sentence, and the elements of the sublist is a word from the sentence.
       
       Output Information:
       - This function will return a single dictionary, that are the semantic descriptors.
       - It is recommended that this function is not ran directly in console as the output insist of a very large dictionary,
         and will take a long time to for python to print out the values.
       '''
    semantic_sim = {} 
    for i in sentences:
        word_set = set(i)
        for x in word_set:
            if x not in semantic_sim.keys():
                semantic_sim[x] = {}
            for y in word_set:
                if x != y:
                    if y not in semantic_sim[x]:
                        semantic_sim[x][y] = 0
                    semantic_sim[x][y] += 1
    return semantic_sim

 
#Functions Provided by M. Guerzhoy

def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 2.
    '''
    sum_of_squares = 0.0  # floating point to handle large numbers
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    '''Return the cosine similarity of sparse vectors vec1 and vec2,
    stored as dictionaries as described in the handout for Project 2.
    '''
    if vec1 == {} or vec2 == {}:
        return -1
    dot_product = 0.0  # floating point to handle large numbers
    for x in vec1:
        if x in vec2:
            dot_product += vec1[x] * vec2[x]
    return dot_product / (norm(vec1) * norm(vec2))

import math