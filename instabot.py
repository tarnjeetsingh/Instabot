import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
# Acess token of the user
app_access_token = '1552927974.120ce8d.08ca68409d6745a7867e181ceea6bb00'
# Base url for instagram API
base = 'https://api.instagram.com/v1/'

# Function  to get self info about the user
def self_info():
    # Creating request url for self info
    request_url = (base+'users/self/?access_token=%s') % (app_access_token)
    print 'GET request url : %s' % (request_url)
    # Hitting the url and using the json function to decode the object and storing it in user_info
    user_info = requests.get(request_url).json()

    # If the status code is 200 i.e sucess
    if user_info['meta']['code']==200:
        # Check if the data exists in the json object
        if len(user_info['data']):
            # Printing name of user, followers, following, number of posts
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        # If user_info object contains no data then printing the message
        else:
            print 'User does not exist!'
    # If the status code other than 200 is received then printing the appropriate message
    else:
        print 'Status code other than 200 received!'

# Function to get user id of a instagram user by passing the username of instagram user as the parameter
def get_user_id(insta_username):
  # Making the request url by using API and joining access token with it
  request_url = (base+'users/search?q=%s&access_token=%s') % (insta_username, app_access_token)
  # Printing the request url
  print 'GET request url : %s' % (request_url)
  # Hitting the url and using the json function to decode the object and storing it in user_info
  user_info = requests.get(request_url).json()
  # Checking if the status code is 200 i.e success
  if user_info['meta']['code'] == 200:
      # Checking if user_info object contains data
      if len(user_info['data']):
          return user_info['data'][0]['id']
      # Printing message if there is no data in json object
      else:
          print 'No user id found'
          return None
  # Printing an appropriate message if the status code other than 200 is received
  else:
      print 'Status code other than 200 received!'
      exit()

# Function to get information about a user by passing the username of the instagram user as a parameter
def get_user_info(insta_username):
    # Using get user id function to get the user of the user
    user_id = get_user_id(insta_username)
    # If no user id with such username exists then printing appropriate message
    if user_id == None:
        print 'User does not exist!'
        exit()
    # Otherwise formalise the request url using the instagram API and attaching the access token with it
    request_url = (base+ 'users/%s?access_token=%s') % (user_id, app_access_token)
    print 'GET request url : %s' % (request_url)
    # Hitting the url and using the json function to decode the object and storing it in user_info
    user_info = requests.get(request_url).json()
    # Checking if the status code is 200 i.e success
    if user_info['meta']['code'] == 200:
        # Check if the data exists in the json object
        if len(user_info['data']):
            # Printing name of user, followers, following, number of posts
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        # If user_info object contains no data then printing the message
        else:
            print 'There is no data for this user!'
    # Printing an appropriate message if the status code other than 200 is received
    else:
        print 'Status code other than 200 received!'

# Function to get the most recent post of user itself
def get_own_post():
  # Formalise the request url using the instagram API and attaching the access token with it
  request_url = (base+ 'users/self/media/recent/?access_token=%s') % (app_access_token)
  print 'GET request url : %s' % (request_url)
  # Hitting the url and using the json function to decode the object and storing it in own_media
  own_media = requests.get(request_url).json()
  # Checking if the status code is 200 i.e success
  if own_media['meta']['code'] == 200:
    # Check if the data exists in the json object
    if len(own_media['data']):
        # Using the urllib to download the most recent post
        image_name = own_media['data'][0]['id'] + '.jpeg'
        image_url = own_media['data'][0]['images']['standard_resolution']['url']
        urllib.urlretrieve(image_url, image_name)
        print 'Your image has been downloaded!'
    # If there is no recent post then printing the message
    else:
        print 'Post does not exist!'
  # Printing an appropriate message if the status code other than 200 is received
  else:
      print 'Status code other than 200 received!'
  return None

# Function to get the most recent post of the instagram user
def get_user_post(insta_username):
    # Using get user id function to get the user id of the user
    user_id = get_user_id(insta_username)
    # If no user id with such username exists then printing appropriate message
    if user_id == None:
        print 'User does not exist!'
    exit()
    # Otherwise formalise the request url using the instagram API and attaching the access token with it
    request_url = (base+ 'users/%s/media/recent/?access_token=%s') % (user_id, app_access_token)
    print 'GET request url : %s' % (request_url)
    # Hitting the url and using the json function to decode the object and storing it in user_info
    user_media = requests.get(request_url).json()
    # Checking if the status code is 200 i.e success
    if user_media['meta']['code'] == 200:
        # Check if the data exists in the json object
        if len(user_media['data']):
            # Using the urllib to download the most recent post
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        # If there is no recent post then printing the message
        else:
            print "There is no recent post!"
    # Printing an appropriate message if the status code other than 200 is received
    else:
        print "Status code other than 200 received!"
    return None

# Function to get the most recent liked pic
def get_own_likes():
    # Formalise the request url using the instagram API and attaching the access token with it
    request_url = (base + 'users/self/media/liked?access_token=%s') % (app_access_token)
    print 'GET request url : %s' % (request_url)
    # Hitting the url and using the json function to decode the object and storing it in own_media
    own_media = requests.get(request_url).json()
    # Checking if the status code is 200 i.e success
    if own_media['meta']['code'] == 200:
        # Check if the data exists in the json object
        if len(own_media['data']):
            # Printing the id of the most recently liked media
            print 'id '+own_media['data'][0]['user']['id']
            print 'url ' + own_media['data'][1]['images']['thumbnail']['url']
            # Using the urllib to download the most recent post
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        # If there is no recent post then printing the message
        else:
            print "There is no recent post!"
    # Printing an appropriate message if the status code other than 200 is received
    else:
        print "Status code other than 200 received!"

# Function to get the post id for a post by the instagram user
def get_post_id(insta_username):
    # Using get user id function to get the user id of the user
    user_id = get_user_id(insta_username)
    # Formalise the request url using the instagram API and attaching the access token with it
    request_url = (base + 'users/%s/media/recent/?access_token=%s') % (user_id, app_access_token)
    # Hitting the url and using the json function to decode the object and storing it in media variable
    media = requests.get(request_url).json()
    # Checking if the status code is 200 i.e success
    if media['meta']['code'] == 200:
        # Check if the data exists in the json object
        if len(media['data']):
            return media['data'][0]['id']
        # If media object contains no data then printing the message
        else:
            print 'There is no such post id!'
    # Printing an appropriate message if the status code other than 200 is received
    else:
        print'Status code other than 200 received'

# Function to post a like on the post of a intagram user
def like_a_post(insta_username):
    # Using get media id function to get the user of the user
    media_id = get_post_id(insta_username)
    # Formalise the request url using the instagram API
    request_url = (base+'media/%s/likes') %(media_id)
    # Making a payload variable to be attached with the url
    payload = {"access_token": app_access_token}
    print 'POST request url : %s' % (request_url)
    # Hitting the url and using the json function to decode the object and storing it in post_a_like object
    post_a_like = requests.post(request_url, payload).json()
    # Checking if the status code is 200 i.e success
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    # Printing an appropriate message if the status code other than 200 is received
    else:
        print 'Your like was unsuccessful. Try again!'

# Function to comments on the post of a intagram user
def get_comments_on_post(insta_username):
    # Using get media id function to get the user of the user
    media_id = get_post_id(insta_username)
    # Formalise the request url using the instagram API and attaching the access token with it
    request_url = (base + 'media/%s/comments/?access_token=%s') % (media_id, app_access_token)
    print ('GET request url: %s') % (request_url)
    # Hitting the url and using the json function to decode the object and storing it in comments_info object
    comments_info = requests.get(request_url).json()
    # Checking if the status code is 200 i.e success
    if comments_info['meta']['code'] == 200:
        # Check if the data exists in the json object
        if len(comments_info['data']):
            print 'All the comments have been properly fetched!'
            print 'Comments are as follows'
            # Using the for loop to print the comments on the post
            for index,val in enumerate(comments_info['data']):
                print comments_info['data'][index]['text']
            return comments_info
            # If media object contains no data then printing the message
        else:
            print 'There is no comments on the post'
    # Printing an appropriate message if the status code other than 200 is received
    else:
        print 'There was some error in fetching of the comments please try again!'

# Function to post a comment on the post of a intagram user
def post_a_comment(insta_username):
    # Using get media id function to get the user of the user
    media_id = get_post_id(insta_username)
    # Formalise the request url using the instagram API and attaching the access token with it
    request_url = (base+'media/%s/comments') %(media_id)
    # Making a payload variable to be attached with the url
    payload = {"access_token": app_access_token, "text": 'thanks'}
    print 'POST request url : %s' %(request_url)
    # Hitting the url and using the json function to decode the object and storing it in post_comment
    post_comment = requests.post(request_url,payload).json()
    # Checking if the status code is 200 i.e success
    if post_comment['meta']['code'] == 200:
        print 'Comment was successful!'
    # Printing an appropriate message if the status code other than 200 is received
    else:
        print 'Your comment was unsuccessful. Please try again!'

# Function to analyze the comments on the post os the instagram user and deleting the comment if it is in negative sentiment
def delete_negative_comment(insta_username):
    # Using get media id function to get the user of the user
    media_id = get_post_id(insta_username)
    # Formalise the request url using the instagram API and attaching the access token with it
    request_url = (base + 'media/%s/comments/?access_token=%s') % (media_id, app_access_token)
    print ('GET request url: %s') %(request_url)
    # Hitting the url and using the json function to decode the object and storing it in post_comment
    comments_info = requests.get(request_url).json()
    # Checking if the status code is 200 i.e success
    if comments_info['meta']['code'] == 200 :
        # Check if the data exists in the json object
        if len(comments_info['data']):
            # using the blob library to analyze the comment
            blob = TextBlob(comments_info['data'][0]['text'],analyzer=NaiveBayesAnalyzer())
            print blob.sentiment
            print blob.sentiment[0]
            # Checking if the blob sentiment is positive or negative
            if blob.sentiment[0] == 'neg':
                comment_id = comments_info['data'][0]['id']
                print comment_id
                # Formalising the url to delete the comment
                delete_url = (base+'media/%s/comments/%s?access_token=%s') %(media_id, comment_id, app_access_token)
                # Hitting the url to delete the comment and store them in the delete_comment json object
                delete_comment = requests.delete(delete_url).json()
                # Checking if the status code is 200 i.e success
                if delete_comment['meta']['code'] == 200:
                    print 'your comment was analyze to be negative and so has been deleted'
                # Printing an appropriate message if the status code other than 200 is received
                else:
                    print 'your comment is negative but it was not deleted. Please try again!'
        # If media object contains no data then printing the message
        else:
            print 'There are no existing comments on this post'
    # Printing an appropriate message if the status code other than 200 is received
    else:
        print 'Status code other than 200 received'

