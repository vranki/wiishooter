import pickle

seed = []
f = open("highscores.txt", "wb")
pickle.dump(seed, f)
f.close()
