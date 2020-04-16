# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 14:43:40 2020

@author: Jonathan Meyers
http://orcid.org/0000-0002-6698-3420
"""

import os
import re
import copy



def custom_alert(stringToPrint):
    
    print(stringToPrint)


def open_txt_file(filename):
    '''
    Imports text from a text file encoded in utf-16-le format. 
    Returns a list of strings (each new line a new list item)
    
    Requires the filename to be the full filename including extension.
    '''

    imported = [] #initialize the list
    
    try:
        with open(filename,encoding='utf-16-le') as f:
            for line in f:
                imported.append(line)
    #            print(repr(line))
    except (UnicodeDecodeError):
        with open(filename,encoding='utf-8') as f:
            for line in f:
                imported.append(line)
    #            print(repr(line))        

    return imported



def get_entry_key_from_linenumber(lines,linenumber):
    '''
    Given the list of strings and a linenumber, this function traces up from the linenumber to find the entry key id
    
    Make sure you give it the current set of lines or it might give you false information.
    '''
#    print('in get_entry_key_from_linenumber, the linenumber is')
#    print(linenumber)
#    print('and the lines are')
#    print(lines)
    cur = linenumber
    while cur >= 0:
        try:
            entryID = re.search(r'^.*@(.*){(.*),',lines[cur]).group(2) #find something of this format: @(something){(something),
        except:
            entryID = None
        
        if entryID != None:
            cur = 0
            return entryID
        
        cur -= 1

    if entryID == None:
        entryID = -1        
    return entryID



def get_field_from_linenumber(lines,linenumber):
    '''
    Given the list of strings and a linenumber, this function traces up from the linenumber to find the field name
    
    Make sure you give it the current set of lines or it might give you false information.
    '''
    
    cur = linenumber
    while cur >= 0:
        try:
            fieldname = re.search(r'^(.*)=\s*{.*}.*',lines[cur]).group(1)
            fieldname = fieldname.strip()
            
        except:
            try:
                # it might be the entryid row. Try that.
                fieldname = re.search(r'^.*@(.*){(.*),',lines[cur]).group(2)
                fieldname = fieldname.strip()
                
            except:
                fieldname = None
                

            
        if fieldname != None:
            cur = 0
            return fieldname
        
        cur -= 1
        
    if fieldname == None:
        fieldname = '??'
    return fieldname

def get_entry_key_from_grouped(group_lines):
    '''
    Given the group list of stings, will give you the entry key
    '''
    
    keyline = group_lines[0]
    
    try:
        keyfind = re.search(r'^.*@.*{(.*),',keyline)
        entryID = keyfind.group(1)
    except:
        entryID = '??'
        
    return entryID
        
    
    
def get_field_from_grouped(group_lines,fieldidx):
    '''
    Given the list of strings and line number in group, will give you the field name
    '''
    
    fieldline = group_lines[fieldidx]
    
    try:
        fieldfind = re.search(r'^(.*)=\s*{.*}.*',fieldline)
        field = fieldfind.group(1)
    except:
        field = '??'
        
    return field


def remove_entryContainer(lines):
    '''
    given the list of strings for a bibtex entry,
    
    Return a list of strings without the first and last line (the entry container lines)
    '''
    copylines = copy.deepcopy(lines)
    if copylines[-1].strip() == '}':
        copylines.pop(-1)
    try:
        res = re.search(r'^@[a-zA-Z]*{.*,',copylines[0])
        res.group(0)
        copylines.pop(0) #the first line is the header. Get rid of.
    except:
        ''
        
    return lines
    


def get_listOfFields_fromEntry(lines):
    '''
    Given the list of strings for a bibtex entry,
    
    Returns the list of fieldnames
    '''
#    print(lines)
    
    fieldlines = remove_entryContainer(lines)
            
    fieldnames = [] 
    fieldvalues = []       
    
    for i in range(len(fieldlines)):
        try:
            res = re.search(r'^([a-zA-Z]*)\s*=\s*{(.*)},',fieldlines[i])
            fieldnames.append(res.group(1).strip().lower())
            fieldvalues.append(res.group(2).strip())
        except:
            ''
    
    
#    print(lines)
#    print(fieldnames)
#    print(fieldvalues)
    
    return fieldnames, fieldvalues


def get_fieldValue_fromEntry(lines, field):
    '''
    Takes a list of strings (an entry) and a fieldname
    
    Returns the value for that particular field
    '''
    
    fieldnames_all, fieldvalues_all = get_listOfFields_fromEntry(lines)
    
    value = '??' #init
    for i in range(len(fieldnames_all)):
        if fieldnames_all[i] == field:
            value = fieldvalues_all[i]
            break
    
    return value


 





def convert_non_ascii_to_latex(string_in,needApproval=False):
    '''
    Iterates through a string and replaces non-ascii characters with an ascii character found in a dictionary.
    
    Returns the corrected string.
    '''
    
    approved = True #default    


    
    # Dictionary
    nonascii_to_latex = {
        b'\x13 ':'-',
        b'\x12"':'-',
        b'\x10 ':'-',
        b'\xbc\x03':'\\textmu{}',
        b'\xe9\x00':'{\\\'e}',
        b'\x19 ':'\'',
        b'H"':'$\\approx$',
        b'\xd7\x00':'$\\times$',
        b'\xb0\x00':'\\textdegree{}',
        b'\xf6\x00':'{\\"o}',
        b'\xe5\x00':'{\\aa}',
        b'\xed\x00':'{\\\'i}',
        b'\xe1\x00':'{\\\'a}',
        b'\xf3\x00':'{\\\'o}',
        b'\xff\xfe':''
        }
    
    
    listed = list(string_in) #convert temporarily to a list
    log_changed_idx = [] #initialize a list of the characters changed
    
    for i in range(len(listed)):
        try:
            listed[i].encode('ascii')
            # No problems here. This character is already ascii
            
            
        except: #for those non-ascii characters:
            try:
                old = listed[i]
#                print('old was {}'.format(old)) # for debugging
                new = nonascii_to_latex[old.encode('utf-16le')] #try using the dictionary above
#                print('new is {}'.format(new))
                

                if needApproval:
                    custom_alert(''.join(listed))
                    custom_alert('\n\n-----\nSpecial Character Alert: Check this change.\n-----\n\n')
                    custom_alert(old)
                    custom_alert('to------')
                    custom_alert(new)
                    approve = input('\n\nApprove (y/n)? ')
                    if approve.lower() != 'y':
                        approved = False
                

                if approved:
                    listed[i] = new # it worked! Replace the character
                    log_changed_idx.append([i,old,new])
                else:
                    log_changed_idx.append([i,old,'BibTex Fixerupper APPROVAL DENIED'])
            
            except: #there was probably not a dictionary key for this character.
                log_changed_idx.append([i,old,'BibTex Fixerupper NOT DEFINED IN DICTIONARY'])
                custom_alert('Found non-ascii character not defined in the dictionary: {}({}). Index {:d} in the line:\n{}\n\n'.format(listed[i],listed[i].encode('utf-16le'),i,''.join(listed)))
                custom_alert('Make sure you insert that into the dictionary!')
                input('Got the message (y/n)?')
                           

            
    return ''.join(listed), log_changed_idx
    


def catch_non_ascii(list_in,needApproval=False):
    '''
    Goes through a list of strings and identifies which characters are non-ascii characters.
    Uses a dictionary to change those characters to either ascii or a LaTeX form form of the character.
    
    Returns the corrected list of strings.
    '''



    log_non_ascii = [] #initialize output log

    for i in range(len(list_in)): # go through the lines
        
        
        #try encoding as ascii. If it fails, it's not ascii and will move to except condition
        try:
            list_in[i].encode('ascii') 


        #if the whole line isn't ascii, identify which character is the culprit
        except: 
            ascii_line, log_char = convert_non_ascii_to_latex(list_in[i],needApproval=needApproval)
            
            list_in[i] = ascii_line #replace the old with the new
            
            for lc in range(len(log_char)):
#                print(log_char[lc])
                log_char[lc].insert(0,i)
                log_non_ascii.append(log_char[lc]) #line number, character number, old char, new char
            

    max_len_orig = max_char_length([x[3] for x in log_non_ascii])
    if len(log_non_ascii) > 0: # if some changes were made, record them in the output log
#        for lna in range(len(log_non_ascii)):
#            print(log_non_ascii[lna])
        numNotDefined = [z[3] for z in log_non_ascii].count('BibTex Fixerupper NOT DEFINED IN DICTIONARY')
        log = ['There were {} total non-ascii characters and {} that were not defined in the dictionary.\n'.format(len(log_non_ascii),numNotDefined)]
                
        log.append('Special characters identified included:\n')
        for d in range(len(log_non_ascii)):
            
            if log_non_ascii[3] == 'BibTex Fixerupper NOT DEFINED IN DICTIONARY':
                log.append('XXXXXXX {} \t\t(in {} of {}) -- NOT DEFINED IN DICTIONARY\n'.format(\
                           log_non_ascii[d][2],\
                           get_field_from_linenumber(list_in,log_non_ascii[d][0]),\
                           get_entry_key_from_linenumber(list_in,log_non_ascii[d][0]),\
                           ))
            
            elif log_non_ascii[3] == 'BibTex Fixerupper APPROVAL DENIED':
                log.append('XXXXXXX {} not changed to {} \t\t(in {} of {}) -- APPROVAL FOR CHANGE DENIED\n'.format(\
                           log_non_ascii[d][2],\
                           get_field_from_linenumber(list_in,log_non_ascii[d][0]),\
                           get_entry_key_from_linenumber(list_in,log_non_ascii[d][0]),\
                           ))
            
            else: # the approved ones
                log.append('\t- {} to {}{} \t(in {} of {})\n'.format(\
                           log_non_ascii[d][2],\
                           log_non_ascii[d][3],\
                           ' ' * (max_len_orig - len(log_non_ascii[d][3])),\
                           get_field_from_linenumber(list_in,log_non_ascii[d][0]),\
                           get_entry_key_from_linenumber(list_in,log_non_ascii[d][0]),\
                           ))
            
            
    return list_in, log




def delete_tabs(list_in):
    '''
    Scans a list of strings and gets rid of extra white space
    '''
    
    for i in range(len(list_in)):
        list_in[i] = list_in[i].lstrip() # only on left side
    
    return list_in




def deleteField_grouped(grouped_in,field,needApproval=False):
    '''
    Takes a list of lists (grouped entries) and a field that should be removed.
    Uses a subfunction to delete those fields from the record.
    
    Outputs an updated list of lists
    '''
    
    
    log_changes = []
    for i in range(len(grouped_in)):
        grouped_in[i],log_deleteFieldSingle = deleteField(grouped_in[i],field,needApproval=needApproval)
        
        if len(log_deleteFieldSingle) > 0:
            for j in range(len(log_deleteFieldSingle)):
                log_changes.append(log_deleteFieldSingle[j])
    
    log_deleteField = [] #initialize                
    log_deleteField.append('\n\n\nThere were {} "{}" fields deleted from the records:\n'.format(len(log_changes),field))
    for i in range(len(log_changes)):
        log_deleteField.append('\t- {}\n'.format(log_changes[i]))
        
        
        
    return grouped_in,log_deleteField
    
    

def deleteField(list_in,field,needApproval=False):
    '''
    Takes a list of strings in
    Goes backwards through it, deleting any line that contains the defined field.
    
    Returns the updated list of strings
    '''
        
    log_deleted = []
    for i,e in reversed(list(enumerate(list_in))):
        if list_in[i].lower().find(field)==0:
            list_in.pop(i)
            log_deleted.append(get_entry_key_from_grouped(list_in))
    
    
    return list_in, log_deleted
        

def max_char_length(list_in):
    '''
    Takes a list of strings.
    Iterates through. First measures length of each item. Then reports the maximum length.
    
    Returns a number
    '''
    return max([len(x) for x in list_in])

def checkPages_grouped(grouped_in):
    '''
    Takes a list of lists (grouped entries) and uses a sub-function to verify/correct what is in the pages field
    
    Returns the enhanced list of lists
    '''
    
    #initialize these log groups
    log_changes = []
    log_missing = []
    log_blank = []
    log_onepage = []
    
    for i in range(len(grouped_in)):
        grouped_in[i],log_pagesSingle = checkPages(grouped_in[i])
        
        if len(log_pagesSingle) > 0: #if something is in the log
            if log_pagesSingle[2] == 'BLANK PAGES':
                log_blank.append(log_pagesSingle)
            elif log_pagesSingle[2] == 'ONE PAGE':
                log_onepage.append(log_pagesSingle)
            elif log_pagesSingle[2] == 'NO PAGES':
                log_missing.append(log_pagesSingle)
            else:
                log_changes.append(log_pagesSingle)
            
#    print(log_changes)
#    print(log_missing)
#    print(log_blank)
#    print(log_onepage)
    
    log_pages = [] #initialize
    log_pages.append('\n\n\nThere were {} "Pages" fields automatically formatted:\n'.format(len(log_changes)))
    
    max_len_orig = max_char_length([x[1] for x in log_changes])
#    print(max_len_orig)
    for i in range(len(log_changes)):
#        print(log_changes[i])
        log_pages.append('\t- {}{} --- changed to --- \t{}\t(from {})\n'.format(log_changes[i][1],' '*(max_len_orig-len(log_changes[i][1])+1),log_changes[i][2],log_changes[i][0]))
        
    log_pages.append('\n\n\nThere were {} entries with a blank "Pages" field:\n'.format(len(log_blank)))
    for i in range(len(log_blank)):
#        print(log_blank[i])
        log_pages.append('\t- {}\n'.format(log_blank[i][0]))

    log_pages.append('\n\n\nThere were {} entries with a "Pages" field with one single page (this may not matter to you):\n'.format(len(log_onepage)))
    for i in range(len(log_onepage)):
#        print(log_onepage[i])
        log_pages.append('\t- {}\n'.format(log_onepage[i][0]))        

    log_pages.append('\n\n\nThere were {} entries with no "Pages" field (this may not matter to you):\n'.format(len(log_missing)))
    for i in range(len(log_missing)):
#        print(log_missing[i])
        log_pages.append('\t- {}\n'.format(log_missing[i][0]))        
        
        
    return grouped_in,log_pages 
    
    




def checkPages(list_in):
    '''
    Given a list of strings (a bibtex entry), it checks for:
        missing page fields
        blank page fields
        fields with only one page number
        fields with only wone hyphen (for latex)
    
    Returns the revised list of strings
    '''
    
    pagesidx = -1
    log_pagesSingle = []
    
    entryid = get_entry_key_from_grouped(list_in)
#    print(entryid)
    fieldnames,fieldvalues = get_listOfFields_fromEntry(list_in) #get lists of all field names and values
#    print(fieldnames)
#    print(fieldvalues)
    
    if 'pages' in fieldnames:
        for f in range(len(fieldnames)):
            pagesidx = f if fieldnames[f] == 'pages' else pagesidx
            
        pagesval_in = fieldvalues[pagesidx].strip()
#        print(pagesval_in)
#        print(list_in[pagesidx+1])
        
        if pagesval_in == '': #even though there was a header, there was no value
            #don't worry about fixing
            log_pagesSingle = [entryid, list_in[pagesidx+1][:-2], 'BLANK PAGES'] #report in log
#            print(log_pagesSingle)
            
        elif pagesval_in.find('-') == -1: #no hyphen, must be only one page
            #don't worry about changing the value
            log_pagesSingle = [entryid, list_in[pagesidx+1][:-2], 'ONE PAGE']
#            print(log_pagesSingle)
        
        else: #there is a value, and it has hyphen(s)
            try:
    #            pagesearch = re.search(r'^([^-]{0,3})\s*([a-zA-Z0-9]*)',pagesval_in)
                pagesearch = re.search(r'^([a-zA-Z0-9]*)\s*-{0,3}\s*([a-zA-Z0-9]*)',pagesval_in)
                page1 = pagesearch.group(1).strip()
                page2 = pagesearch.group(2).strip()
                
                pagesval_out = 'pages = {}{}--{}{},\n'.format('{',page1,page2,'}')
                if list_in[pagesidx+1] != pagesval_out:
                    log_pagesSingle = [entryid, list_in[pagesidx+1][:-2],pagesval_out[:-2]]
                    list_in[pagesidx+1] = pagesval_out #make the change
#                    print(log_pagesSingle)
                    
                
            except:
                custom_alert(list_in)
                custom_alert(pagesval_in)
                custom_alert('\n\n-----\nError regex pages.\n-----\n\n')
                input('Got the message (y/n)? ')
            
    else:
        log_pagesSingle = [entryid,'','NO PAGES']
#        print(log_pagesSingle)

    
    return list_in,log_pagesSingle




def group_by_entry(list_in):
    '''
    Scans through a list of strings and groups the list of strings into a list of lists based on their emtry starter symbol @
    
    Makes sure that the first line is of format @(citationtype){(name),
    and that the last line is a closing brace with a newline marker, }\n
    
    Returns a list of list of strings
    '''
    
    grouped_list = []
    
    scanning = False
    startline = 0 #initialize
    openbrace = 0 #initialize
    endline = -1 #initialize
    i = 0 #while loop iterator
    endi = len(list_in) - 1 #this might change
    while i <= endi:
        
        #count the open braces
        #when 0, should be the end of an entry.
        openbrace += list_in[i].count('{') - list_in[i].count('}') 
        
        
        try:
#            print(list_in[i])
#            re.search(r'^@[a-zA-Z]*{.*',list_in[i]).group(0) #if you find an @ symbol with an open brace close to to it (separated by the type of entry in only letters), you've found the starter symbol
            headersearch = re.search(r'^@([a-zA-Z]*){([^=]*),(.*)',list_in[i])
            headersearch.group(0) #if this works, it found a header and will continue
#            print('I found an @ symbol!')
            foundEntryStarter = True
        except:
            foundEntryStarter = False
        
        
        if not scanning and foundEntryStarter:
            scanning = True
            startline = i
            
            citetype = headersearch.group(1)
            entryid = headersearch.group(2)
            extraline = headersearch.group(3)
            
            list_in[i] = '@{}{}{},\n'.format(citetype.lower(),'{',entryid)
            
            if extraline != '':
                list_in.insert(i+1,extraline.strip()+'\n')
                endi += 1
                
            
                
        elif scanning and foundEntryStarter:
            custom_alert(list_in)
            custom_alert(list_in[i])
            custom_alert('\n\n-----\nError: There must be a missing brace.\n-----\n\n')
            input('Got the message (y/n)? ')
            grouped_list = []
            break
        
        if scanning and openbrace == 0:
            scanning = False
            endline = i
            
            endbracepos = list_in[i].rfind('}')
            if endbracepos != 0: #closing brace is not on its own line. Fix it.
                list_in[i] = list_in[i][:endbracepos]+list_in[i][endbracepos+1:]
                list_in.insert(i+1,'}\n')
                i += 1
                endline += 1
                endi += 1
            grouped_list.append(list_in[startline:endline+1]) #add group to the output list.


        i += 1


    
#    for i in range(len(grouped_list)):
#        print(grouped_list[i],'\n')
#    
    
    return grouped_list


    


def findEntryContent(list_in):
    '''
    Takes a list of strings (a bibtex entry)
    Flattens the list into a string
    Uses regex to find the @(type){entryID... and closing brace }
    
    Returns the citation type, entryID, and the contents (all as a strings)
    '''
    
    entryStr = ''.join(list_in).strip()
    entryStr = entryStr.replace('\n',' ') #regexp doesn't like these.
#    print(repr(entryStr))
    
    try:
        res = re.search(r'^@([a-zA-Z]*){([^,]*),(.*)}$',entryStr)
        
        citetype = res.group(1).strip()
#        print(citetype)
        entryid = res.group(2).strip()
#        print(entryid)
        contents = res.group(3).strip()
#        print(contents)
        
        
        
    except:
        custom_alert('Something bad happened')
        custom_alert('I have never had this happen before.')
        input('Got the message (y/n)?')
        citetype = 'Failed at findEntryContent'
        entryid = 'Failed at findEntryContent'
        
    return citetype.lower(), entryid, contents




def findAll_inString(string,substring):
    return [i for i in range(len(string)) if string.startswith(substring,i)]





def separateFields(entryContent):
    '''
    Takes a string of all the entry content (excluding the @(type){ and the closing marker}).
    Note that the markers can be braces, quotes, or none. Pretty cool, huh? They all become braces later.
    
    Scans through the entry and splits at all commas. Checks that the presumed field title matches one in the fieldtitle variable listed below. If not, it recombines it with the prior line.
    I think this method should work...
    
    Then it figures out what field separator was used and switches it for braces to create consistency.
    
    Outputs a list of strings.
    '''
    
    
    #
    fieldtitles = ['author','title','journal','year','date','volume','number','pages','month','note',\
                   'translator','annotator','commentator','subtitle','titleaddon','editor','editora',\
                   'editorb','editorc','journalsubtitle','issuetitle','issuesubtitle','language',\
                   'origlanguage','series','eid','issue','month','pages','version','note','issn',\
                   'addendum','pubstate','doi','eprint','eprintclass','eprinttype','url','urldate',\
                   'introduction','foreword','afterword','titleaddon','maintitle','mainsubtitle',\
                   'maintitleaddon','part','edition','series','location','isbn','pages','pagetotal',\
                   'day','publisher','keywords','abstract','school','type','address',\
                   #ones below are just for testing
                   'othernote','removednote',\
                   ]
    
    
    #first split at commas to try to separate into respective fields.
    entrySplit = entryContent.split(',')

    realfields = ['' for x in range(len(entrySplit))] #initialize
    j = -1 # for keeping track of the real fields
    for i in range(len(entrySplit)):
        
        #presume that the first word is the field title.
        splitEq = entrySplit[i].split('=')
        fieldname = splitEq[0].lower().strip()
        
        #now check that presumption. If it matches an approve field title above, we'll add it to the growing list of approved real fields
        if fieldname in fieldtitles:
            j += 1

            

        #either put this line with the last line (not a new field) or on a new line (real field)
        realfields[j] = ','.join([realfields[j],entrySplit[i]])
        


    for i,e in reversed(list(enumerate(realfields))):
        # get rid of empty rows (from initialized list)    
        if realfields[i] == '':
            realfields.pop(i)
        # or get rid of the extra comma we added on the left. Add one to to the right.
        else:
            realfields[i] = realfields[i].lstrip(' , ')
            realfields[i] = realfields[i] if realfields[i].endswith(',') else realfields[i]+','
            
#            if realfields[i].count('=') > 1:
#                custom_alert('\n\n-------------------------\
#                             \nThis row has more than one equal sign. Check?')
##                custom_alert(real)
#                custom_alert(realfields[i])
#                input('Got the message (y/n)? ')
            
#    for i in range(len(realfields)):
#        print(repr(realfields[i]))
            

            
            
    # GREAT! We now have a good idea of where the fields are. Now let's make sure they are formatted the way we want them (with braces mostly)
    fields_out = [] #initialize a list we'll output
    for i in range(len(realfields)):
#        print(repr(realfields[i]))
        
        try:
            res = re.search(r'^([a-zA-Z]*)\s{0,3}=(.*),',realfields[i]) #doesn't care about field separators
            fieldname = res.group(1).lower().strip()
#            print(fieldname)
            fieldval = res.group(2).strip()
#            print(fieldval)
            
            inQuotes = True if fieldval[0]=='"' and fieldval[-1]=='"' else False
            inBraces = True if fieldval[0]=='{' and fieldval[-1]=='}' else False
            
            if inQuotes or inBraces:
                fieldval = fieldval[1:-1].strip() #remove the quotes or braces
                
#            print(fieldval)
            fields_out.append('{} = {}{}{},\n'.format(fieldname,'{',fieldval,'}')) #compile the line into the field name space = space brace field value brace comma newline
            
        except:
            custom_alert(entryContent)
            custom_alert(realfields[i])
            custom_alert('\n\n-----\nError: Problem separating the fields.\n-----\n\n')
            input('Got the message (y/n)? ')
            
            
            
#    for i in range(len(fields_out)):
#        print(repr(fields_out[i]))


    return fields_out
            
            


def cleanUpFields_grouped(grouped_in):
    '''
    Takes a list of lists of bibtex entries.
    uses a subfunction to clean up each entry
    
    Outputs repaired list of lists
    '''
    
    # go through each of the grouped entries and identify the fields spanning multiple lines
    log_cleanups = [] #initialize
    
    for i in range(len(grouped_in)):
        grouped_in[i],log_cleanupsingle = cleanUpFields_single(grouped_in[i])
        for j in range(len(log_cleanupsingle)):
            log_cleanups.append(log_cleanupsingle[j])
        

    log_cleanup = []
    if len(log_cleanups) > 0:
        log_cleanup.append('\n\n\nThere were {} fields that had more than one equal sign. As this is a possible source of error in the code, please review:\n'.format(len(log_cleanups)))
        for i in range(len(log_cleanups)):
            log_cleanup.append('\t- in {}:\n\t\t{}\n'.format(log_cleanups[i][1],log_cleanups[i][0]))
    else:
        log_cleanup.append('\n\n\nThere were 0 fields that had more than one equal sign. Hakuna Matata!.\n\n')
        
    return grouped_in,log_cleanup


        

def cleanUpFields_single(list_in):
    '''
    Takes a list of strings (a BibTex entry) and puts it through two functions to clean it up and make it consistent
    
    Returns a list of strings that is perfectly formatted.
    '''
    
#    print('\n\n',list_in)

    entrytype,entryid,content = findEntryContent(list_in)
    trigger = '@{}{}{},\n'.format(entrytype,'{',entryid) #format the trigger
    
    
    content_refined = separateFields(content)
    
#    print(trigger)
#    print(content_refined)
    
    

    
    
    #combine the entryID and the content into one list of lists
    content_refined.insert(0,trigger)
    content_refined.append('}\n') #close the entry 
            
    log_cleanup = [] #initialize            
    for i in range(len(content_refined)):
        if content_refined[i].count('=') > 1:
            log_cleanup.append([content_refined[i],entryid])
            
#    print(repr(content_refined))
    

    return content_refined, log_cleanup








def delete_emptylines(list_in):
    '''
    Scans through a list of strings and deletes empty rows.
    Does this backwards so it can pop them as we go and not change indexing.
    
    We'll add the nice clean whitespace back later.
    '''

    for i,e in reversed(list(enumerate(list_in))):
        if list_in[i] == '':
            list_in.pop(i)
    return list_in


def add_extranewlines(list_in):
    '''
    Scans through a list of strings and adds a newline marker \n at the end of the last row if not already there.
    
    Purpose is to create consistency in future scanning.
    '''
    
    lastentry = len(list_in)-1
    
    if not list_in[lastentry].endswith('\n'):
        list_in[lastentry] = list_in[lastentry] + '\n'

    
    return list_in





    

def commentField_grouped(grouped_in,field):
    '''
    Comments out a field by appending "removed" in front of the field name. This is the only way that I've found LaTeX allows.
    
    Returns the revised list of lists
    '''
    
    log_changes = []
    for i in range(len(grouped_in)):
        grouped_in[i],log_commentSingle = commentField(grouped_in[i],field)
        
        if len(log_commentSingle) > 0:
            log_changes.append(log_commentSingle)
            
#        print(log_changes)
    
    log_commentField = [] #initialize                
    log_commentField.append('\n\n\nThere were {} "{}" fields commented from the records:\n'.format(len(log_changes),field))
    for i in range(len(log_changes)):
#        print(log_changes[i])
        log_commentField.append('\t- {}\t(from {})\n'.format(log_changes[i][0],log_changes[i][1]))
        
        
        
    return grouped_in,log_commentField        




def commentField(list_in,field):
    '''
    Comments out a field by appending "removed" in front of the field name. This is the only way that I've found LaTeX allows.
    
    Returns a list of strings
    '''
    
    log_commentFieldSingle = []
    for i in range(len(list_in)):
        if list_in[i].lower().find(field.lower()) == 0: #if the the line matches the field
            newline = 'removed' + list_in[i]
            
            list_in[i] = newline
            
            log_commentFieldSingle = [newline[:-2],get_entry_key_from_grouped(list_in)]
                
    return list_in, log_commentFieldSingle






def addDOI_grouped(grouped_in):
    '''
    Takes a list of lists (grouped entries) and uses a sub-function to add the doi or url if missing
    or enters the need for a url/doi in the log.
    
    Returns the enhanced list of lists
    '''
    
    log_changes = []
    log_missing = []
    for i in range(len(grouped_in)):
        grouped_in[i],log_addDOIsingle = addDOI(grouped_in[i])
        
        if len(log_addDOIsingle) > 0:
            log_missing.append(log_addDOIsingle) if log_addDOIsingle[1] == 'MISSING URL AND DOI' else log_changes.append(log_addDOIsingle)
            
#    print(log_changes)
#    print(log_missing)
    
    log_addDOI = [] #initialize
    log_addDOI.append('\n\n\nThere were {} URL/DOI fields automatically added:\n'.format(len(log_changes)))
    for i in range(len(log_changes)):
#        print(log_changes[i])
        log_addDOI.append('\t- {}\t(from {})\n'.format(log_changes[i][1],log_changes[i][0]))
        
    log_addDOI.append('\n\n\nThere were {} entries lacking both URL and DOI fields:\n'.format(len(log_missing)))
    for i in range(len(log_missing)):
#        print(log_missing[i])
        log_addDOI.append('\t- {}\n'.format(log_missing[i][0]))        
        
        
    return grouped_in,log_addDOI       
    




def addDOI(list_in):
    '''
    Takes a list of strings (one bibtex entry) and identifies if it has a DOI field.
    If it does not, but it has the DOI in the URL field, it will add the DOI field automatically.
    If it doesn't have a DOI in the URL, it will make a note in the output file.
    
    Returns a modified list of strings
    '''

#    print(list_in)
    
    #defaults
    hasURL = False
    URLidx = -1
    hasDOI = False
    DOIidx = -1
    log_addDOIsingle = []
    
    entryid = get_entry_key_from_grouped(list_in)
#    print(entryid)
    fieldnames,fieldvalues = get_listOfFields_fromEntry(list_in) #get lists of all field names and values
    
    if 'url' in fieldnames:
        hasURL = True
        for f in range(len(fieldnames)):
            URLidx = f if fieldnames[f] == 'url' else URLidx
    
    if 'doi' in fieldnames:
        hasDOI = True
        for d in range(len(fieldnames)):
            DOIidx = d if fieldnames[d] == 'doi' else DOIidx

    

    if hasDOI and hasURL:
        '' #great. Don't need to do anything.
        
    elif not hasDOI and hasURL:
#        print('Does not have DOI, has URL')
        URLval = fieldvalues[URLidx]
#        print(URLval)
        
        try:
            URLsearch = re.search(r'^.*doi.org/(.*)$',URLval, re.IGNORECASE)
            URLDOI = URLsearch.group(1)
            DOIentry = 'doi = {}{}{},\n'.format('{',URLDOI,'}')
            list_in.insert(URLidx,DOIentry) #insert the DOI into the list
            log_addDOIsingle = [entryid,DOIentry[:-2]]
        except:
            ''
    elif hasDOI and not hasURL:
#        print('Does have the DOI but not the URL') #easy fix. We'll add the URL
        DOIval = fieldvalues[DOIidx]
#        print(DOIval)
        
        URLentry = 'url = {}{}{},\n'.format('{https://doi.org/',DOIval,'}')
        list_in.insert(DOIidx+1,URLentry)
        log_addDOIsingle = [entryid,URLentry[:-2]]
        
    elif not hasDOI and not hasURL: #can't do anything besides alert the user in the log
        log_addDOIsingle = [entryid,'MISSING URL AND DOI']
        
        
    return list_in,log_addDOIsingle
        








def get_insidebrace(string_to_search):
    foundit = re.search(r'^.*{(.*)}.*$',string_to_search)
    return foundit.group(1)

def get_field_value(list_in,field):
    
    for i in range(len(list_in)):
        if list_in[i].lower().find(field.lower()) == 0:
            return get_insidebrace(list_in[i])


def unique(repetitive_list):
    unique_list = []
    for i in repetitive_list:
        if i not in unique_list:
            unique_list.append(i)
    return unique_list



def get_unique_fieldvalues(grouped_data, field):
    '''
    Takes a list of lists (the grouped bibtex entries)
    Finds all unqiue values of the field specified.
    Example: for the journals field, will list all the journals in your bibtex library
    
    Returns a list of strings
    '''
    
    values = [] #init
    for i in range(len(grouped_data)):
        
        value = get_fieldValue_fromEntry(grouped_data[i],field) #get the value from this entry
        if value != '??': #gets ?? if the field doesn't exist
            values.append(value)
        
        
    unique_values = sorted(unique(values), key=str.lower) #get unique, sorted
    
    
    log_unique = []
    log_unique.append('\n\n\nThere are {} unique values in the "{}" field:\n'.format(len(unique_values),field))
    for i in range(len(unique_values)):
        log_unique.append('\t- {}\n'.format(unique_values[i]))
    
    
    return unique_values, log_unique



def get_missing_fieldvalues(grouped_data, field):
    '''
    Takes a list of lists (the grouped bibtex entries)
    Finds all missing values of the field specified.
    
    Returns a list of strings
    '''
    
    entries_missingField = [] #init
    for i in range(len(grouped_data)):
        
        value = get_fieldValue_fromEntry(grouped_data[i],field) #get the value from this entry
        if value.strip() in ['??','']: #gets ?? if the field doesn't exist
            entries_missingField.append(get_entry_key_from_grouped(grouped_data[i]))
    
    
    log_missing = []
    log_missing.append('\n\n\nThere are {} entries having empty or missing the "{}" field:\n'.format(len(entries_missingField),field))
    for i in range(len(entries_missingField)):
        log_missing.append('\t- {}\n'.format(entries_missingField[i]))
    
    
    return entries_missingField, log_missing
        
        








def main(docpath,docname,printChangeLog=True):
    os.chdir(docpath)
    doctext = open_txt_file(docname)
#    print(doctext)
    
    from datetime import datetime
    now = datetime.now()

    log_changes = [] #initialize the log of changes
    log_changes.append('Log of changes to {} on {}\n\n\n'.format(docname,now.strftime("%m/%d/%Y %H:%M:%S")))

    rev,log_non_ascii = catch_non_ascii(doctext,needApproval=False) #revision 1. replace special characters with ascii and/or latex forms
    log_changes.append(log_non_ascii)
    
    rev = delete_tabs(rev) #revision 2. delete meaningless tabs on left
    rev = add_extranewlines(rev) #revision 3. Make sure end has some \n markers. Prevents problems later.
    rev = delete_emptylines(rev) #revision 4. get rid of any empty lines
    grouped = group_by_entry(rev) # group by entry
    
    grouped,log_cleanup = cleanUpFields_grouped(grouped) # clean up each entry (line spacing, field spacing, etc.)
    log_changes.append(log_cleanup)
    
    grouped,log_deleteFields = deleteField_grouped(grouped,'abstract') #delete abstract field. Too bulky.
    log_changes.append(log_deleteFields)
    
    grouped,log_commented = commentField_grouped(grouped,'note') #comment out this field. Have to do this in a particular way though or LaTeX doesn't like it.
    log_changes.append(log_commented)
    
    grouped,log_addDOI = addDOI_grouped(grouped) #adds the doi or url automatically if possible
    log_changes.append(log_addDOI)
    
    grouped,log_pages = checkPages_grouped(grouped) #checks the page field for 1 page and for double hyphen
    log_changes.append(log_pages)
        
    journals,log_journals = get_unique_fieldvalues(grouped,'journal')
    log_changes.append(log_journals)
    
    titles,log_titles = get_unique_fieldvalues(grouped,'title')
    log_changes.append(log_titles)
    
    
    ### missing fields?
    missing_author,log_missing = get_missing_fieldvalues(grouped,'author')
    log_changes.append(log_missing)    
    
    missing_title,log_missing = get_missing_fieldvalues(grouped,'title')
    log_changes.append(log_missing)        
    
    missing_journal,log_missing = get_missing_fieldvalues(grouped,'journal')
    log_changes.append(log_missing)        
        
    missing_year,log_missing = get_missing_fieldvalues(grouped,'year')
    log_changes.append(log_missing)       

    missing_volume,log_missing = get_missing_fieldvalues(grouped,'volume')
    log_changes.append(log_missing)             
    
    

#    for i in range(len(grouped)):
#        print(grouped[i],'\n\n')

    
    
    fid = open(docname[:-4]+'_output.txt','w', encoding='ascii')
    for w in range(len(grouped)):
#        print('\n\n\n')
#        print(final[w])
        fid.writelines(grouped[w])
        fid.write('\n\n\n\n\n')
    fid.close()
        
    
    
    if printChangeLog:
        fidcl = open(docname[:-4]+'_log.txt','w', encoding='utf-8')
        for w in range(len(log_changes)):
            fidcl.writelines(log_changes[w])
        fidcl.close()



def autorun():

    needFile = True
    while needFile:
        fullfilepath = input('Please type in the full file path for the BibTex file you want to clean up (hint: type something like c:\\folder\\file.txt or type q to quit):\n')
        print(repr(fullfilepath))
        needFile = False if os.path.isfile(fullfilepath) else True
        
        needFile = False if fullfilepath.lower() == 'q' else needFile
        
    
    if fullfilepath.lower() != 'q':
        docpath, docname = os.path.split(fullfilepath)
        main(docpath,docname,printChangeLog=True)
        print('Finished cleaning up!')
    else:
        print('Quit Confirmed.')    




if __name__ == '__main__':
    
    
    autorun()



            
