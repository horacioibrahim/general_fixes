"""
Check if python files has first line with PEP-0263 in compliance ;)
"""

# TODO: if script to keep call #!/...
# TODO: Report files changed
# TODO: deeply directories 

import os
import re
import doctest
import tempfile
import sys

CODING = "UTF-8"

def get_pyfiles(abs_dir):
	r"""
	List files .py in directory and its subdirectories

	>>> tempdir = tempfile.mkdtemp()
	>>> test_py = os.path.join(tempdir, 'test.py')
	>>> f = open(test_py, 'w')
	>>> f.write('loren ipsum line\n')
	>>> f.write('loren ipsum line\n')
	>>> f.close()
	>>> type(get_pyfiles(tempdir))
	<type 'list'>
	>>> os.remove(test_py)
	>>> os.rmdir(tempdir)
	"""
	
	if not os.path.isabs(abs_dir):
		raise TypeError("Path must be absolute.")

	lists = []
	
	for path, dirname, files_names in os.walk(abs_dir):
		folders = path.split('/')
		if folders[-1] == 'migrations': # Remove files of type migrations
			continue
		for f in files_names:
			if f.endswith('.py'):
				lists.append(os.path.join(path, f))

	return lists

def check_file(filename):
	r"""
	Checks if first line of a file has compliance with PEP-0263
	
	>>> checker = True
	>>> tempdir = tempfile.mkdtemp()
	>>> test_py = os.path.join(tempdir, 'test.py')
	>>> f = open(test_py, 'w')
	>>> f.write('loren ipsum line 1\n')
	>>> f.write('loren ipsum line 2\n')
	>>> f.close()
	>>> list_files = get_pyfiles(tempdir)
	>>> check_file(list_files[0]) 	
	False
	>>> os.remove(test_py)
	>>> f = open(test_py, 'w')
	>>> f.write("# -*- coding: utf-8 -*-\n")
	>>> f.write("continua na segunda linha\n")
	>>> f.close()
	>>> list_files = get_pyfiles(tempdir)
	>>> check_file(list_files[0])
	True
	>>> os.remove(test_py)
	>>> # Test with script shell
	>>> f = open(test_py, 'w')
	>>> f.write('#!/usr/bin/env python\n')
	>>> f.write('# -*- coding: UTF-8 -*-\n')
	>>> f.close()
	>>> check_file(test_py)
	True
	>>> os.remove(test_py)
	>>> os.rmdir(tempdir)
	"""
	rex = re.compile(r'^#.*coding[=|:].*[\w]+-[\d]+') 
	with open(filename, 'r') as arq:
		lines = arq.readlines()
		arq.close()

		if lines:
			if len(lines) > 1:
				if rex.match(lines[0]) or rex.match(lines[1]):
					return True
			else:
				if rex.match(lines[0]):
					return True
	
	return False 

def change_file(filename):
	r"""
	Add comments for PEP-0263 with utf-8

	>>> tempdir = tempfile.mkdtemp()
	>>> test_py = os.path.join(tempdir, 'test.py')
	>>> f = open(test_py, 'w')
	>>> f.write('loren ipsum line\n')
	>>> f.write('loren ipsum line\n')
	>>> f.close()	 
	>>> change_file(test_py)
	0
	>>> check_file(test_py)
	True
	>>> os.remove(test_py)
	>>> f = open(test_py, 'w')
	>>> f.write('#!/bin/bash/python\n')
	>>> f.write('# -*- coding: utf-8 -*-\n')
	>>> f.close()
	>>> check_file(test_py)
	True
	>>> os.remove(test_py)
	>>> f = open(test_py, 'w')
	>>> f.write('#!/bin/bash/python\n')
	>>> f.write('import re\n')
	>>> f.close()
	>>> check_file(test_py)
	False
	>>> change_file(test_py)
	0
	>>> os.remove(test_py)
	>>> os.rmdir(tempdir)
	"""

	# Is command line script?
	is_script = re.compile(r'^#!').match

	# bkp filename
	bkp = filename + '.checker'

	# make recovery
	if os.path.isfile(bkp):
		print "Backup file found: %s \n" % bkp
		print "Start recovering file... %s to %s \n" % (bkp, filename)
		original_file = open(filename, 'w')
		bkp_file = open(bkp, 'r')
		original_file.writelines(bkp_file.readlines())
		original_file.close()
		bkp_file.close()
		print "Recovered with success! \n"

	if not check_file(filename):
		try:
			f_read = open(filename, 'r')
			content = f_read.readlines()
		except IOError, e:
			raise

		# creates a backup files as 'file.py.checker' before write
		bkpd = open(bkp, 'w')
		bkpd.writelines(content)

		# Coding strint 
		coding = "# -*- coding: {} -*-\n".format(CODING)

		with open(filename, 'w') as f:
			if is_script(content[0]):
				f.write(content[0]) # write PEP263 in second line
			f.write(coding)
			f.writelines(content[1:]) # skip first line already insert
		
		f.close()
		# if all occured fine. Remove bkp
		os.remove(bkp)

		return 0

def checker(path):
	files = get_pyfiles(path)

	for f in files:
		change_file(f)

if __name__ == '__main__':
	doctest.testmod()

	try:
		abs_dir = sys.argv[1]
		checker(abs_dir)
	except IndexError, e:
		print("Warnings: No arguments with absolute path.")
		
		

		
