#!/usr/local/bin/python
# coding: utf-8

import re, requests, sys, tweepy
from tweepy.streaming import StreamListener

from twitter_secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

class Listener(StreamListener):
	def on_status(self, status):
		delete_old_tweet()
		return True
	
	def on_error(self, status):
		print status

def delete_old_tweet():
	#tweets = api.user_timeline(screen_name = 'czircon',count=200)
#	for status in tweepy.Cursor(api.user_timeline(screen_name = 'czircon', count=200)).items():
	for status in tweepy.Cursor(api.user_timeline, screen_name = 'czircon', count=200, include_rts=True).items():
		if not "Verifying myself:" in status.text and not status.favorited:
			oldest_tweet = status
	print "oldest: " + oldest_tweet.text

	confirmation = True

	if len(sys.argv) > 1 and sys.argv[1] == "debug":
		if raw_input("Destroy tweet? ").lower() != 'y':
			confirmation = False

	if confirmation:
		print "Destroying."
		api.destroy_status(oldest_tweet.id)
# post the tweet
u = api.get_user(screen_name = 'czircon' )
stream = tweepy.Stream(auth, Listener())
stream.filter(follow=[str(u.id)])
#tweets = api.user_timeline(screen_name = 'czircon',count=200)

#delete_old_tweet()
