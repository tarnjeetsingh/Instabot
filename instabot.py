import requests
app_access_token = '1552927974.120ce8d.08ca68409d6745a7867e181ceea6bb00'
base = 'https://api.instagram.com/v1/'

def self_info:
    request_url = (base+'users/self/?access_token=%s') % (app_access_token)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code']==200:
        if len(user_info['data']):