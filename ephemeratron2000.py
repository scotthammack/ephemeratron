#!/usr/local/bin/python
# coding: utf-8

import re, requests, sys, tweepy
from tweepy.streaming import StreamListener

from twitter_secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, SCREEN_NAME

DEBUG = ( len(sys.argv) > 1 and sys.argv[1] == "debug" )

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

class Listener(StreamListener):
	def on_status(self, status):
		if status.user.screen_name != SCREEN_NAME or api.get_user(screen_name = SCREEN_NAME).statuses_count <= 69:
			return False
		delete_old_tweet()
		return True
	
	def on_error(self, status):
		print status

def delete_old_tweet():
	oldest_tweet = None

	for status in tweepy.Cursor(api.user_timeline, screen_name = SCREEN_NAME, count = 200, include_rts = True).items():
		if not (status.favorited and not status.retweeted) and not status.text.startswith("Verifying myself:"):
			oldest_tweet = status

	if not oldest_tweet:
		print "Couldn't find an oldest tweet. :("
		return False

	print "Oldest tweet: " + oldest_tweet.text

	if DEBUG and not raw_input("Destroy tweet? ").lower().startswith('y'):
		return False

	print "Destroying."
	api.destroy_status(oldest_tweet.id)
	return True

u = api.get_user(screen_name = SCREEN_NAME)
stream = tweepy.Stream(auth, Listener())
stream.filter(follow = [str(u.id)])
