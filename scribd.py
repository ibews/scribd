#!/usr/bin/python3

import os
import shutil
import sys

from random import randint
from subprocess import call, DEVNULL
from urllib.request import Request, urlopen, urlretrieve


DESTINATION = "/tmp/scribd-%s" % randint(0,10000)

TITLE = "output.pdf"

def download_site(site):
	req = Request(site)
	req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36")
	response = urlopen(req)
	source = response.readall().decode("utf-8").split("\n")
	return source

def get_images(code):
	imageLines = []
	title = "default"
	for line in sourcecode:
		if "pageParams.contentUrl" in line:
			imageLines.append(line.replace("pages", "images").replace(".jsonp", ".jpg"))

	images = [line.split('"',2)[-2] for line in imageLines]
	return images

def download_images(images, destination):
	pageCount = 0
	if not os.path.exists(destination):
		os.makedirs(destination)

	for image in images:
		pageCount += 1;
		urlretrieve(image, os.path.join(destination, "page%03d.jpg" % pageCount))

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Too few Arguments\nusage: " + sys.argv[0] + " <target url> [output title]")
		sys.exit(1)
	else:
		url = sys.argv[1]
		if len(sys.argv) >= 3:
			TITLE = sys.argv[2]

	sourcecode = download_site(url)
	images = get_images(sourcecode)
	download_images(images, DESTINATION)
	command = ["convert", os.path.join(DESTINATION, "page*.jpg"), TITLE]
	proc = call(command, stdout=DEVNULL)
	shutil.rmtree(DESTINATION)