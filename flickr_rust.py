import flickrapi, urllib,os


api_key = 'cffcba86d99501fa08d82992dbbe5c4a'
api_secret = 'Y844c0b8df51c39a9'

flickr = flickrapi.FlickrAPI(api_key, api_secret, cache=True)
outputPath = os.getcwd() + '/output'

def validatePath(directoryPath):
	if not os.path.exists(directoryPath):
		os.makedirs(directoryPath)

def flickr_walk(keyword, limit):
	count = 0
	photos = flickr.walk(text=keyword,
							 tag_mode='all',
							 tags=keyword,
							 extras='url_c',
							 per_page=20)
	for photo in photos:
		print(photo)
		try:
			url = photo.get('url_c')
			writePath = outputPath + '/search/' + str(keyword)
			validatePath(writePath)
			urllib.request.urlretrieve(url, writePath +"/"+ str(keyword)+'_'+ str(count) + ".jpg")
			count += 1
			if count > limit:
				break
		except Exception as e:
			print(e)
			print('failed to download image')

def flickr_group(keyword, limit,group_id):
	count = 0
	photos = flickr.walk(text=keyword,
							 tag_mode='all',
							 tags=keyword,
							 extras='url_c',
							 per_page=20,
						 	group_id=group_id)
	for photo in photos:
		print(photo)
		try:
			url = photo.get('url_c')
			writePath = outputPath+'/groups/'+str(group_id)
			validatePath(writePath)
			urllib.request.urlretrieve(url,writePath+ "/"+str(count) + ".jpg")
			count += 1
			if count > limit:
				break
		except Exception as e:
			print(e)
			print('failed to download image')

def flickr_set(set_id, limit):
	count = 0
	photos = flickr.walk_set(photoset_id=set_id,
						 tag_mode='all',
						 extras='url_c',
						 per_page=20)
	for photo in photos:
		print(photo)
		try:
			url = photo.get('url_c')
			writePath = outputPath + '/photosets/' + str(set_id)
			validatePath(writePath)
			urllib.request.urlretrieve(url, writePath + "/" + str(count) + ".jpg")
			count += 1
			if count > limit:
				break
		except Exception as e:
			print(e)
			print('failed to download image')
