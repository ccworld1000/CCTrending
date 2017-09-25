#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  CCTrending.py
#  
#  Created by CC on 2017/09/24.
#  Copyright 2017 youhua deng (deng you hua | CC) <ccworld1000@gmail.com>
#  https://github.com/ccworld1000/CCTrending
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import os
import re
import time
import pygal
import tarfile
import yagmail
import requests

from pygal import Config
from pygal.style import DarkColorizedStyle


def languages_list (names) :
	if names :
		names = names.replace("Perl 6", "Perl%206")
		names = names.replace("#", "%23")
		names = re.sub ('(and|\.| |\n)', '', names, flags = re.S)
		
		real_list = names.split(",")
		return real_list
	else:
		return []
		

def languages_show (llist) :
	index = 1
	for l in  sorted(llist) :
		print ("[languages %d]\t" % (index) + l)
		index += 1

def languages_tar(srcPath, dstname) :
	tar = tarfile.open(dstname, "w:gz")
	for dirpath, dirs, files in os.walk(srcPath) :
		for filename in files :
			tar.add (os.path.join(dirpath, filename))
			print (filename + " tar OK")
	
	tar.close()
	

def languages_trending (llist, isStars) :
	llen = len(llist)
	print (llen)
	if llen :
		keys= 'stars'
		if not isStars :
			keys = 'forks'
			
		seq = 1
		headers = {
		"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
		'Accept': 'application/json, text/javascript'
			}
		
		time_title = time.strftime("%Y%m%d%H%M%S", time.localtime()) 
		prefix = 'CCTrending'
		
		dir_name = prefix + time_title
		
		os.mkdir (dir_name)
		
		for ll in sorted(llist):
			url = 'https://api.github.com/search/repositories?q=language:' + ll + '&sort=' + keys
			print (url)
			
			#if seq >= 2:
				#continue
			
			values = "mars" + str(seq)
			cookies = {"name" : values}
			req = requests.get (url, headers = headers, cookies = cookies)
			status_code = req.status_code
			if status_code != 200 :
				print ("req return " + str (status_code))
				continue
			
			response_dict = req.json()
			litems = response_dict['items']
			
			names = []
			counts = []
			
			for li in litems :
				name = li['name']
				full_name	=	li['full_name']
				language	= 	li['language']
				description = 	li['description']
				
				html_url 	= 	li ['html_url']
				
				if isStars :
					stargazers_count = li['stargazers_count']
					counts.append(stargazers_count)
				else:
					forks_count = li['forks_count']
					counts.append(forks_count)
				
				names.append(name)
				
				print (str(seq) + "> "+ language + ': ' + name + ' '+ html_url)
				
			file_name = ll
			#chart = pygal.Bar()
			#chart = pygal.Bar(fill=True, interpolate='cubic', style=DarkColorizedStyle, x_label_rotation = 45, width=1000)
			
			chart = pygal.Bar(interpolate='cubic', width=1000)
			
			config = Config()
			config.show_legend = False
			config.human_readable = True
			config.fill = True
			config.style=DarkColorizedStyle
			config.label_font_size = 36
			config.x_label_rotation = 45
			
			chart.config = config

			chart.title = file_name + " [" + time_title + "]"
			chart.x_labels = names;
			chart.add(prefix, counts)
			
			
			#save_name = dir_name + "/" + file_name + ".svg"
			#save_name = os.path.join(dir_name, file_name + ".svg") 
			save_name = os.path.join(dir_name, file_name + ".png")
			
			#chart.render_to_file (save_name)
			chart.render_to_png (save_name)
			
			seq += 1
			time.sleep(5)
			print ("\n")
	
		languages_tar(dir_name, dir_name + ".tag.gz")
	
