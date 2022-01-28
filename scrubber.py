import time
import yagmail
import requests
import urllib.parse
import urllib.request

receiver = "mkaufmanv2@gmail.com"

watchlist = ('GPU')



url = 'https://api.reddit.com/r/buildapcsales/new?limit=1'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-agent': user_agent}
values = { 'name': 'bot',
		   'location': 'ssd',
		   'language': 'beepboop' }
categoryStringStart = '"link_flair_text": "'
categoryStringEnd = '", "can_mod_post":'
titleStringStart = ', "title": "'
titleStringEnd = '", "link_flair_richtext"'
linkStringStart = ', "url": "'
linkStringEnd = '", "subreddit_'


def printIterate(iterate):
	if (iterate % 100 == 0):
		print('\n\nIteration # ' + str(iterate) + '\n\n')


iterate = 0
while (1 == 1):
	iterate = iterate + 1
	printIterate(iterate)

	data = urllib.parse.urlencode(values)
	data = data.encode('ascii')
	req = urllib.request.Request(url, data, headers)

	with urllib.request.urlopen(req) as response:
		nasty = response.read()

	contents = nasty.decode("utf-8")

	
	categoryStartLocation = contents.find(categoryStringStart)
	categoryEndLocation = contents.find(categoryStringEnd)

	category = contents[(categoryStartLocation + len(categoryStringStart)) : categoryEndLocation]
	print("Category = " + str(category) + "\n")


	titleStartLocation = contents.find(titleStringStart)
	titleEndLocation = contents.find(titleStringEnd)

	title = contents[(titleStartLocation + len(titleStringStart) + len(category) + 3) : titleEndLocation]


	linkStartLocation = contents.find(linkStringStart)
	linkEndLocation = contents.find(linkStringEnd)

	link = contents[(linkStartLocation + len(linkStringStart)) : linkEndLocation]


	isAmpLocation = link.find('&amp;')
	if (isAmpLocation != -1):
		link = link[0 : isAmpLocation]


	if (category in watchlist):
		print('\n\n' + str(category) + ' found!')
		summary = '--Title of post: \n' + str(title) + '\n--Link to product: \n' + str(link) + '\n\n'
		body = '-Title of post: \n' + str(title) + '\n\n\n-Link to product: \n' + str(link) + '\n'
		print(summary)
		yag = yagmail.SMTP("scrubberbot@gmail.com")
		yag.send (
			to = receiver,
			subject = "A " + category + " has been found on r/buildapcsales!",
			contents = body,
		)

		stop = 0
		while (stop == 0):
			time.sleep(30)

			data = urllib.parse.urlencode(values)
			data = data.encode('ascii')

			req = urllib.request.Request(url, data, headers)

			with urllib.request.urlopen(req) as response:
				newnasty = response.read()

			newcontents = newnasty.decode("utf-8")
			newtitleEndLocation = newcontents.find(titleStringEnd)

			if (newtitleEndLocation != titleEndLocation):
				print('stop = 1')
				stop = 1

			elif (newtitleEndLocation == titleEndLocation):
				categoryStartLocation = contents.find(categoryStringStart)
				categoryEndLocation = contents.find(categoryStringEnd)
				category = contents[(categoryStartLocation + len(categoryStringStart)) : categoryEndLocation]
				print('Category = ' + str(category) + '\n')
				iterate = iterate + 1
				printIterate(iterate)


	else:
		time.sleep(30)