import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
app_access_token = '1552927974.120ce8d.08ca68409d6745a7867e181ceea6bb00'
base = 'https://api.instagram.com/v1/'

def self_info():
    request_url = (base+'users/self/?access_token=%s') % (app_access_token)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code']==200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'

def get_user_id(insta_username):
  request_url = (base+'users/search?q=%s&access_token=%s') % (insta_username, app_access_token)
  print 'GET request url : %s' % (request_url)
  user_info = requests.get(request_url).json()
  if user_info['meta']['code'] == 200:
      if len(user_info['data']):
          return user_info['data'][0]['id']
      else:
          return None
  else:
      print 'Status code other than 200 received!'
      exit()

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (base+ 'users/%s?access_token=%s') % (user_id, app_access_token)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'

def get_own_post():
  request_url = (base+ 'users/self/media/recent/?access_token=%s') % (app_access_token)
  print 'GET request url : %s' % (request_url)
  own_media = requests.get(request_url).json()
  if own_media['meta']['code'] == 200:
    if len(own_media['data']):
        image_name = own_media['data'][0]['id'] + '.jpeg'
        image_url = own_media['data'][0]['images']['standard_resolution']['url']
        urllib.urlretrieve(image_url, image_name)
        print 'Your image has been downloaded!'
    else:
        print 'Post does not exist!'
  else:
      print 'Status code other than 200 received!'
  return None

def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
    exit()
    request_url = (base+ 'users/%s/media/recent/?access_token=%s') % (user_id, app_access_token)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print "There is no recent post!"
    else:
        print "Status code other than 200 received!"
    return None

def get_own_likes():
    request_url = (base + 'users/self/media/liked?access_token=%s') % (app_access_token)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()
    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            print 'id '+own_media['data'][0]['user']['id']
            print 'id ' + own_media['data'][1]['images']['thumbnail']['url']
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'


def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    request_url = (base + 'users/%s/media/recent/?access_token=%s') % (user_id, app_access_token)
    media = requests.get(request_url).json()
    if media['meta']['code'] == 200:
        if len(media['data']):
            return media['data'][0]['id']
    else:
        print'Status code other than 200 received'

def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (base+'media/%s/likes') %(media_id)
    payload = {"access_token": app_access_token}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'

def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (base+'media/%s/comments') %(media_id)
    payload = {"access_token": app_access_token, "text": 'bad one'}
    print 'POST request url : %s' %(request_url)
    post_comment = requests.post(request_url,payload).json()
    if post_comment['meta']['code'] == 200:
        print 'Comment was successful!'
    else:
        print 'Your comment was unsuccessful. Please try again!'

def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (base + 'media/%s/comments/?access_token=%s') % (media_id, app_access_token)
    print ('GET request url: %s') %(request_url)
    comments_info = requests.get(request_url).json()
    if comments_info['meta']['code'] == 200 :
        if len(comments_info['data']):
            blob = TextBlob(comments_info['data'][0]['text'],analyzer=NaiveBayesAnalyzer())
            print blob.sentiment
            print blob.sentiment[0]
            if blob.sentiment[0] == 'neg':
                comment_id = comments_info['data'][0]['id']
                print comment_id
                delete_url = (base+'media/%s/comments/%s?access_token=%s') %(media_id, comment_id, app_access_token)
                delete_comment = requests.delete(delete_url).json()
                if delete_comment['meta']['code'] == 200:
                    print 'your comment was analyze to be negative and so has been deleted'
                else:
                    print 'your comment is negative but it was not deleted. Please try again!'
        else:
            print 'There are no existing comments on this post'
    else:
        print 'Status code other than 200 received'

