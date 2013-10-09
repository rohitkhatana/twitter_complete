#! /usr/bin/env python
# coding:utf-8

'''
A module that provide a Python interface to the Twitter API
'''

# to use OAuth
import oauth2 as oauth

# import urllib for using urllib.urlencode when using 'POST' method 
import urllib



# to use datetime.datetime, datetime.timedelta class
import datetime

# next modules are used in GetOauth class
import webbrowser
import urlparse


#mine
import json
from pprint import pprint
# Tiwtter Api URL

_USER_TIMELINE_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
RATE_LIMIT_URL ='https://api.twitter.com/1.1/application/rate_limit_status.json'

# these constants are used in the GetOuath class.
_REQUEST_TOKEN_URL = 'https://twitter.com/oauth/request_token'
_ACCESS_TOKEN_URL = 'https://twitter.com/oauth/access_token'
_AUTHORIZE_URL = 'https://twitter.com/oauth/authorize'





class GetOauth:
    '''
    A class for getting consumer_key and consumer_secret.
    '''

    def __init__(self, consumer_key, consumer_secret):
        '''
        GetOauth initializer.
        '''
       
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    # for python2.5
    def _parse_qsl(self, url):
        '''
        Parse_qsl method.

        for python 2.5
        '''
        param = {}
        for i in url.split('&'):
            p = i.split('=')
            param.update({p[0]:p[1]})
        return param
    
    def get_oauth(self):
        '''
        Get consumer_key and consumer_secret.

        How to use:
        
        >>> import twitter_oauth
        >>> consumer_key = '***'
        >>> consumer_secret = '***'
        >>> get_oauth_obj = twitter_oauth.GetOauht(consumer_key, consumer_secret)
        >>> get_oauth_obj.get_oauth()
        '''
        signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
        consumer = oauth.Consumer(key=self.consumer_key,secret=self.consumer_secret)
        client = oauth.Client(consumer)
        print client,consumer
        #Step1: Get a request token.
        resp, content = client.request(_REQUEST_TOKEN_URL, 'POST', body="oauth_callback=oob")
        if resp['status'] != '200':
            raise Exception('Invalid response %s' % resp['status'])
    
        request_token = dict(self._parse_qsl(content))
        
        print "Request Token:"
        print "  - oauth_token        = %s" % request_token['oauth_token']
        print "  - oauth_token_secret = %s" % request_token['oauth_token_secret']
    
    
        #step2 Redirect to the provider
    
        print "Go to the following link in your browser"
        print '%s?oauth_token=%s' % (_AUTHORIZE_URL, request_token['oauth_token'])
        print 
    
        webbrowser.open('%s?oauth_token=%s' % (_AUTHORIZE_URL, request_token['oauth_token']))
    
        # accepted = 'n'
        # while accepted != 'y':
        #     accepted = raw_input('Have you authorized me? (y/n) ')
    
        oauth_verifier = raw_input('What is the PIN? ')
    
        #step3
        token = oauth.Token(request_token['oauth_token'], 
                            request_token['oauth_token_secret'])
        token.set_verifier(oauth_verifier)
        client = oauth.Client(consumer, token)
    
        resp, content = client.request(_ACCESS_TOKEN_URL, "POST")
        access_token = dict(self._parse_qsl(content))

        oauth_token = access_token['oauth_token']
        oauth_token_secret = access_token['oauth_token_secret']
        
        print "Access Token:"
        print "  - oauth_token        = %s" % oauth_token
        print "  - oauth_token_secret = %s" % oauth_token_secret
        print
        print "You may now access protected resources using the access token above"
        print
     
        return {'consumer_key':self.consumer_key, 
                'consumer_secret':self.consumer_secret, 
                'oauth_token':oauth_token, 
                'oauth_token_secret':oauth_token_secret}


    
class TwitterError(Exception):
    '''
    A class representing twitter error.

    A TwitterError is raised when a status code is not 200 returned from Twitter.
    '''
    
    def __init__(self, status=None, content=None):
        '''
        res : status code
        content : JSON
        '''
        Exception.__init__(self)
        
        self.status = status
        self.content = content

    def get_response(self):
        '''
        Return status code
        '''

        return self.status
		
    def get_content(self):
        '''
        Return JSON
        '''

    def __str__(self):
        return 'status_code:%s' % self.status
        



class Api:
    '''
    A Python interface to the Twitter API

    How To Use:

    First, you shold have two keys, 
    'consumer key', 'consumer secret'.

    If you don't have 'consumer key' and 'consumer secret', 
    you cat get these keys to register your application to Twitter.
    You cat register your application at next URL.

    http://twitter.com/apps



    Second, you shold get two keys,
    'oauth_token', and 'oauth_token_secret'

    To get these keys, you use GetOauth class in this module.

    >>> import twitter_complete

    >>> # write your key and secret
    >>> consumer_key = '***'
    >>> consumer_secret = '***'

    >>> get_oauth_obj = twitter_oauth.GetOauth(consumer_key, consumer_secret)


    Then, you get 'oauth_token' and 'oauth_token_secret' by using get_oauth method.
    This method returns a dictionary that contain 'consumer key', 'consumer secret',
    'oauth_token' and 'oauth_token_secret'


    >>> get_oauth_obj.get_oauth()
      Request Token:
        - oauth_token        = ***
        - oauth_token_secret = ***
      Go to the following link in your browser
      http://twitter.com/oauth/authorize?oauth_token=***
      
      What is the PIN? ***
      Access Token:
        - oauth_token        = ***
        - oauth_token_secret = ***
      
      You may now access protected resources using the access token above'''
     




    def __init__(self,
                 consumer_key, consumer_secret,
                 oauth_token, oauth_token_secret):
        '''
        The Api class initializer.
        '''

        self.client = oauth.Client(oauth.Consumer(consumer_key, consumer_secret),
                              oauth.Token(oauth_token, oauth_token_secret))

     

    def rate_limit(self):
        url = RATE_LIMIT_URL
        print url
        res,content = self.client.request(url,'GET')

        if res['status'] != '200':
            raise TwitterError(res['status'], content)
        else:
            #parse rate limit json
            data = json.loads(content)
            print data
            
        
        
    
    def get_user_timeline(self, id=None, since_id=None, max_id=None,
                             count=None, page=None):
        
        # parse args
        arg_dict = {'id':id , 'since_id':since_id, 'max_id':max_id,
                    'count':count, 'page':page}

        url_param_list = []

        for (key, item) in arg_dict.iteritems():
            if item != None:
                url_param_list.append(key + '=' + str(item))

        # create URL. append querry to a URL
        param = '&'.join(url_param_list)
        if param:
            url = _USER_TIMELINE_URL + '?' + param
        else:
            url = _USER_TIMELINE_URL
    
        print url
        # GET request to Twitter
        res, content = self.client.request(url, 'GET')


        if res['status'] != '200':
            raise TwitterError(res['status'], content)
        else:
            # parse JSON
            #print content
            data = json.loads(content)
            
            for d in data:
                print "name: " + d['user']['name']
                print "location: " + d['user']['location']
                print "tweet id: " + str(d['id'])
                print "tweet text: " + d['text']
            #doc = minidom.parseString(content)
            #return self.xml_parser.create_status_object_list(doc.getElementsByTagName('status'))
         
        






