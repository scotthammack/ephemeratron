#!/usr/local/bin/python
# coding: utf-8

import re, requests, sys, tweepy
from tweepy.streaming import StreamListener

from twitter_secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, SCREEN_NAME

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

class Listener(StreamListener):
	def on_status(self, status):
		return delete_old_tweet()
	
	def on_error(self, status):
		print status

def delete_old_tweet():
	for status in tweepy.Cursor(api.user_timeline, screen_name = SCREEN_NAME, count = 200, include_rts = True).items():
		if not "Verifying myself:" in status.text and not (status.favorited and not status.retweeted):
			oldest_tweet = status
	print "oldest: " + oldest_tweet.text

	confirmation = True

	if len(sys.argv) > 1 and sys.argv[1] == "debug":
		if raw_input("Destroy tweet? ").lower() != 'y':
			confirmation = False
			return False

	if confirmation:
		print "Destroying."
		api.destroy_status(oldest_tweet.id)
		return True

u = api.get_user(screen_name = SCREEN_NAME)
stream = tweepy.Stream(auth, Listener())
stream.filter(follow = [str(u.id)])
