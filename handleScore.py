import json
import pygame, sys
import datetime as dt

pygame.init()

def getScore():
	with open("scores.txt","r") as f:
		f.seek(0)
		data = json.loads(f.read())
		f.close()
	return data

def saveScore(score):
	date = dt.datetime.now()
	with open("scores.txt","r") as f:
		f.seek(0)
		x = json.loads(f.read())
		f.close()

		x.append({"date":date.strftime("%d-%b %Y"), "score":score})
		x.sort(key = lambda i:i["score"], reverse=True)

		if len(x)>5:x=x[:5]
		
		y = json.dumps(x)

		f = open("scores.txt","w")
		f.write(y)
		f.close()
