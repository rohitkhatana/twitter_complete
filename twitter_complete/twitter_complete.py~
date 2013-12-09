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
_STATUS_UPDATE_URL = 'https://api.twitter.com/1.1/statuses/update.json'
_SAVED_SEARCH_SHOW_URL='https://api.twitter.com/1.1/saved_searches/show/:id.json'
_SAVED_SEARCH_LIST_URL = 'https://api.twitter.com/1.1/saved_searches/list.json'
_USER_FOLLOWERS_IDS_URL = 'https://api.twitter.com/1.1/followers/ids.json'
_USER_FRIENDS_IDS_URL = 'https://api.twitter.com/1.1/friends/ids.json'

_USER_SEARCH_URL  = "https://api.twitter.com/1.1/users/search.json"
_USER_LOOKUP_URL = 'https://api.twitter.com/1.1/users/lookup.json'

_USER_TIMELINE_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
_RETWEETS_OF_ME="https://api.twitter.com/1.1/statuses/retweets_of_me.json"
_MENTION_TIMELINE_URL='https://api.twitter.com/1.1/statuses/mentions_timeline.json'
_HOME_TIMELINE_URL = 'https://api.twitter.com/1.1/statuses/home_timeline.json'


_RETWEETERS_IDS_URL = 'https://api.twitter.com/1.1/statuses/retweeters/ids.json'
_RETWEETS_OF_ME="https://api.twitter.com/1.1/statuses/retweets_of_me.json"

RATE_LIMIT_URL ='https://api.twitter.com/1.1/application/rate_limit_status.json'

_SEARCH_TWEETS_URL = "https://api.twitter.com/1.1/search/tweets.json"

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
        


'''
all data is return by this api is in unicode format

so u need to convert it into ASCII
so for this u need to to use
import unicodedata
for i in user_timeline:
    print i['text'].encode('ascii','ignore')

'''
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
      #accept list of resources
    #application/rate_limit =180        
    def rate_limit(self,resources=None):
        if resources:
            resources=",".join(resources)
            url = RATE_LIMIT_URL + "?resources=" + resources 
        else:    
            url = RATE_LIMIT_URL #+ "?resources=account,application,search,statuses"
        print url
        res,content = self.client.request(url,'GET')

        if res['status'] != '200':
            raise TwitterError(res['status'], content)
        else:
            #parse rate limit json
            data = json.loads(content)
            print data

    def __util(self,url=None,arg_dict=None,METHOD=None):
          
        # parse args
        if METHOD==None:
            METHOD = 'GET'

        url_param_list = []

        for (key, item) in arg_dict.iteritems():
            if item != None:
                if isinstance(item, list):
                    lis=""
                    for i in item:
                        lis += str(i)
                        if i!= item[(len(item)-1):][0]:
                            lis += ','
                    url_param_list.append(key + '=' + lis)
                else:
                    url_param_list.append(key + '=' + str(item))

        # create URL. append querry to a URL
        param = '&'.join(url_param_list)
        if param:
            url = url + '?' + param
        
        print url
        # GET request to Twitter
        res, content = self.client.request(url, METHOD)


        if res['status'] != '200':
            raise TwitterError(res['status'], content)
        else:
            # parse JSON
            #print content
            data = json.loads(content)
            
            '''for d in data:
                print "name: " + d['user']['name']
                print "location: " + d['user']['location']
                print "tweet id: " + str(d['id'])
                print "tweet text: " + d['text']'''

            return data       
   
         





    '''return 20 most recent tweets ,upto 800 and return tweet with mention of username
    rate_limit = 15/user'''

    def get_mentions_timeline(self, since_id=None, max_id=None,count=None, page=None):
        arg_dict = { 'since_id':since_id, 'max_id':max_id,
                    'count':count}
        return self.__util(_MENTION_TIMELINE_URL,arg_dict)
        
         

    #can return only upto  3200 of a user's most recent tweets
    #rate_limit = 180/user
    '''
        usage:
        data=  api.get_user_timeline(screen_name='nike')
        for i in data:
            print i['text']
    '''
    def get_user_timeline(self, user_id=None, screen_name=None, since_id=None, max_id=None,
                             count=None, page=None):

       
        # parse args
        arg_dict = {'user_id':user_id , 'screen_name':screen_name,'since_id':since_id, 'max_id':max_id,
                    'count':count}
        return self.__util(_USER_TIMELINE_URL,arg_dict)


              
    #can return upto 800,return tweet posted by user and followers
    #rate_limit 15/user
    def get_home_timeline(self, since_id=None, max_id=None,
                             count=None):
        
        # parse args
        arg_dict = { 'since_id':since_id, 'max_id':max_id,
                    'count':count}
        return self.__util(_HOME_TIMELINE_URL,arg_dict)
       

  
    #return most recent tweets authoured by user that have been retweeted by others
    #rate_limit = 15
    def get_retweets_of_me(self,since_id=None,max_id=None,
                           count=None):
          arg_dict = {'since_id':since_id, 'max_id':max_id,
                    'count':count}
          return self.__util(_RETWEETS_OF_ME,arg_dict)


    
    '''
        return first 1000 matching result of user account,try querying by topical interest
        ,full name,company name,location etc
        rate limit = 180/user
    '''

    def get_user_search(self,q,page=None,count=None):
        arg_dict = {'q':q,'page':page,'count':count}
        return self.__util(_USER_SEARCH_URL,arg_dict)

    
    '''
        return fully-hydrated user object for upto 100 user per request

        this method is especially useful when used in cunjuction with collection
        of user IDs returned from GET friends/ids and GET followers/ids

        Get users/show is used to retrieve a single user object
        rate limit 180/user,60/app
    '''

    def get_user_lookup(self,screen_name=None,user_id=None,include_entities=None):
        arg_dict = {'screen_name':screen_name,'user_id':user_id,"include_entities":include_entities}
        return self.__util(_USER_LOOKUP_URL,arg_dict,METHOD="POST")
    
    #now search
    '''
        rate limit =180/user

        d=api.get_search('rohit',count=5)
        for x in d['statuses']:
        #print x['statuses']
        print x['text']
    '''
    def get_search(self,q,geocode=None,lang=None,
                   count=None,since_id=None,max_id=None):
        arg_dict={'q':q,'geocode':geocode,'lang':lang,'count':count,
                  'since_id':since_id,"max_id":max_id}
        return self.__util(_SEARCH_TWEETS_URL,arg_dict)


    '''
        return cursor of user_ids of those user whom the current user is following
        rate limit 15/user,15/app
        
    '''
    #return list of user_id
    #list of user_id should be less then 101 otherwise 403 staus_code will return from twitter
    def get_user_friends_ids(self,user_id=None,screen_name=None,cursor=None,stringify_ids=None,count=None):
        arg_dict = {'user_id':user_id, 'screen_name':screen_name,'cursor':cursor,'stringify_ids':stringify_ids,'count':count}
        data= self.__util(_USER_FRIENDS_IDS_URL,arg_dict)
        return data['ids']


    #return collection of userid who are following the specified user
    #return 5000 userids and mulitple 'pages'o fo result
    #rate limit 15/user,15/app
    #this method return list of ids
    def get_user_followers_ids(self,user_id=None,screen_name=None,cursor=None,stringify_ids=None,count=None):
        arg_dict = {'user_id':user_id, 'screen_name':screen_name,'cursor':cursor,'stringify_ids':stringify_ids,'count':count}
        data= self.__util(_USER_FOLLOWERS_IDS_URL,arg_dict)
        return data['ids']
    

        
    #return collection of up to 100 user IDS belonging to users who have retweeted the tweet specified by the id parameter
    #rate_limit = 15/user, 60/app
    def get_retweeters_id(self,id,cursor=None,stringify_ids=None):
        arg_dict={'id':id,'cursor':cursor,"stringify":stringify_ids}
        return self.__util(_RETWEETS_IDS_URL,arg_dict)
        

    '''
        returns the authenticated user' saved search queries
        reate limit = 15/user
        
    '''
    def get_saved_search_list(self):
        return self.__util(_SAVED_SEARCH_LIST_URL,{})

    def get_saved_search_show_id(self,id):
        arg_dict = {'id':id}
        return self.__util(_SAVED_SEARCH_SHOW_URL,arg_dict)


    def status_update(self,status,in_reply_to_status_id=None,lat=None,source=None,place_id=None):
        arg_dict = {'status':status,'in_reply_to_status_id':in_reply_to_status_id,
                    'lat':lat,'place_id':place_id}        
        return self.__util(_STATUS_UPDATE_URL,arg_dict,METHOD='POST')
        



    


    
'''
if __name__=="__main__":
    consumer_key=********
    consumer_secret=******
    get = GetOauth(consumer_key ,consumer_secret)
    
    get.get_oauth()
      Request Token:
        - oauth_token        = ***
        - oauth_token_secret = ***
      Go to the following link in your browser
      http://twitter.com/oauth/authorize?oauth_token=***
      
      What is the PIN? ***
      Access Token:
        - oauth_token        = ***
        - oauth_token_secret = ***
   
    
    api = Api(consumer_key, consumer_secret,
              oauth_token, oauth_token_secret)
    print api.get_retweets_of_me(327473909412814850)
    print api.get_user_timeline(count=2)
    print api.get_home_timeline(count=2)
    print api.get_retweets_of_me(count=1)
    print api.get_search('rahul',count=2)
    print api.rate_limit(['search','application','statuses'])

'''
