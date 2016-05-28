#/usr/bin/env python

# todo: sort and insert new, handle path as argv? 
# todo: handle multiple hits on incr_me match

import sys
import fileinput
from os.path import expanduser, join

agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

usage = "usage: %s [list [alphanum]] | [update "\
        "[alphanum]] | [check alphanum] | [when alphanum]" %(sys.argv[0])
grab = []

def get_ep_name(line):
    return line.split('\t')[0].strip()

def get_last_seen(line):
    marker = line.find("; ") + len("; ")
    return line[marker: marker + len("sXYeZz")].strip()

def get_current_ep(last):
    # num = get_num(line)
    # return num[num.find("e")+1:]
    return last[4:]

def get_next_ep(last, far=1):
    cur = int(get_current_ep(last))
    head, sep, tail = last.rpartition(str(cur).zfill(2))
    return head + str(cur+int(far)).zfill(2) + tail

def incr_me(line, word_match, next_):
    if line and line.startswith(word_match):
        curr = get_last_seen(line)
        nex_ = get_next_ep(curr, next_)
        line = line.replace(curr, nex_)
        print("Updated  %s: %s  =>  %s" %(get_ep_name(line), curr, nex_))
    grab.append(line)

def list_me(line, word_match):
    if line.startswith(word_match):
        sys.stdout.write(line)

def seek_me(line, word_match):
    if line.startswith(word_match):
        host = "http://cda.pl"
        word = get_ep_name(line)
        seen = get_last_seen(line)
        next = get_next_ep(seen)
        query = "%s/info/%s+%s" % (host, word, next)
        print("Last seen: %s %s next...%s" %(word, seen, next))
        print("Looking up... %s" % query)
        r = requests.get(query, headers=agent)
        q = """onclick="moreVideo();return false;">"""
        q_loc = r.text.find(q) + len(q)
        q_loc_close = r.text.find("<", q_loc + 5)
        if not "0" in r.text[q_loc: q_loc_close]:
            txt = '"/video/'
            href_start = r.text.find(txt, q_loc) + len(txt)
            href_end = r.text.find(">", href_start) - 1
            print("1st hit:\n" + host + txt[1:] + r.text[href_start: href_end])
        else:
            print("Not found...")

def find_next_air(line, word_match):
    now = datetime.datetime.now()
    now = now.strftime("d_%-d_%-m_%Y")
    # this webpage uses format d_31_5_2016 what a braindead idea...
    if line.startswith(word_match):
        name, episode = line.split('\t')[0].strip(), get_next_ep(get_last_seen(line))
        print "Matched:", name, episode
        host = "http://www.pogdesign.co.uk/cat/"
        r = requests.get(host, headers=agent)
        text = r.text.lower()
        day_marker = text.find('"day"')
    	while day_marker > 0:
            day = text[day_marker - 18: day_marker - 8]
            day = day[day.find("_") + 1: ]
            # find next airing or -1 if not played this month
            airs = text.find(name, day_marker)
            if airs < 0:
                print "Not this month."
                return None
            # find next day, or -1 if end of month
            day_marker = text.find('"day"', day_marker + 1)
            ep_marker = text.find('</a>', airs + 30)
            this_ep = text[ep_marker - 6: ep_marker]
            if airs > day_marker:
                if day_marker > 0:
                    continue
                else:
                    if this_ep >= episode:
                        print "last day of month", day, this_ep
                    else:
                        print "Not this month."
                    break
            else:
                if this_ep >= episode:
                    print "at", day, this_ep

if not len(sys.argv) > 1:
  print usage
  exit(0)
else:
  my_file_path = "WAZNE", "seriale", "last_seen"
  path = join(expanduser("~"), *my_file_path)
  if "list".startswith(sys.argv[1]):
    try:
      word_match = sys.argv[2].lower()
    except IndexError:
      word_match = ""
    do_work = list_me
    opts = word_match,

  elif "update".startswith(sys.argv[1]):
    try:
      word_match = sys.argv[2].lower()
    except IndexError:
      word_match = "\n"
    try:
      increase_count = int(sys.argv[3])
    except (IndexError, ValueError):
      increase_count = 1
    do_work = incr_me
    opts = word_match, increase_count

  elif "check".startswith(sys.argv[1]):
    import requests
    
    try:
      word_match = sys.argv[2].lower()
    except IndexError:
      word_match = "\n"
    do_work = seek_me
    opts = word_match,

  elif "when".startswith(sys.argv[1]):
    import requests
    import datetime

    try:
      word_match = sys.argv[2].lower()
    except IndexError:
      word_match = "\n"
    do_work = find_next_air
    opts = word_match,
  else:
    print(usage)
    exit(1)
  
  cnt = 0  
  with open(path, 'r') as file_:
    for line in file_:
      do_work(line.lower(), *opts)
      cnt += 1
  
  if "update".startswith(sys.argv[1]):
    with open(path, 'w') as file_:
      for line in grab:
        file_.write(line)    
    
  elif "list".startswith(sys.argv[1]):
    print("Saved: %d" % cnt)

