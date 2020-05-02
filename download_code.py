#importing the necessary libraries
import requests as re
from bs4 import BeautifulSoup
from datetime import datetime
import os

# To calculate the time taken to run the code
start_time = datetime.now()
print('code started at '+str(start_time))

# Default url we'll be using to concat with download links 
# in the later part 
defaul_url = 'https://link.springer.com'

# opening the urls that I have saved in a txt file
#iterating them and appending to a list
urls_file = open('links.txt','rb')
urls = [x.decode('utf_8').split('\n')[0] for x in urls_file.readlines()]
urls_file.close()

def download_pdf(url):

	# get the html of the webpage
	resp = re.get(url)
	
	# read the HTML using BeautifulSoup
	# more documentation on BeautifulSoup - https://pypi.org/project/beautifulsoup4/
	soup = BeautifulSoup(resp.text,'html.parser')

	if len(soup.find_all('a',{'class':'test-bookpdf-link'},href=True))==0:
		return "no data"
	else:
		# Create a download link, the path in the webpage is a server path
		# this is the reason we are appending default_url variabl we have defined in the 
		# previous part
		download_link = defaul_url+str(soup.find_all('a',{'class':'test-bookpdf-link'},href=True)[0]['href'])
		book_name = soup.find('h1').text+'.pdf'

		resp = re.get(download_link)

		file = open('books/'+book_name.replace('/',' '),'wb')
		file.write(resp.content)
		file.close()

		return book_name

for i,url in enumerate(urls):
	start_loop = datetime.now()
	book_name = download_pdf(url)
  
  # escapes URLs which has books which needs purchase!
	if book_name == 'no data':
		print(str(i)+'. No Data, Buy book')
	else:
		file_size = round(os.stat('books/'+book_name.replace('/',' ')).st_size/(1024*1024),2)

		print(str(i)+'. '+book_name+' size of '+str(file_size)+' MB '+str(datetime.now() - start_loop).split('.')[0]+ ' S')

print('Code has completely run in '+str(datetime.now()-start_time))
