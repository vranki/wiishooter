# -*- coding: utf-8 -*-
import pygame
import pickle
import string

class menu:
    def __init__(self):
        self.state = "main_menu"
        screen_size = (640,480)
        
        self.background = pygame.Surface(screen_size)
        self.background.blit(pygame.image.load("Background.gif"), (0,0))

        self.text_area = pygame.Surface((screen_size[0]-50, screen_size[1]-50))
        self.text_area.fill((255,255,255))
        self.text_area.set_alpha(200)

        self.append_screen = appendscore()
        self.welcome_screen = welcome()
        self.highscore_screen = highscores(False, 0)


    def update(self, screen, cursor):
        screen.blit(self.background, (0,0))
        screen.blit(self.text_area, (25,25))
        if self.state == "main_menu":
            self.state = self.welcome_screen.update(screen, cursor)
        if self.state == "append_score":
            self.state = self.append_screen.update(screen, cursor)
            if self.state == "high_scores":
                self.highscore_screen = highscores(True, self.append_screen.score_pos())
        if self.state == "new_game":
            pass
        if self.state == "high_scores":
            self.state = self.highscore_screen.update(screen, cursor)

        return self.state

    def new_score(self, score):
        self.append_screen.upload_highscore(score)
        self.state = "append_score"

class textarea:
    def __init__(self, screen_size):
        self.text_area = pygame.Surface((screen_size[0]-100, screen_size[1]-100))
        self.text_area.fill((255,255,255))
        self.text_area.set_alpha(200)

    def update(self, screen, cursor):
        screen.blit(self.text_area, (50,50))


class appendscore:
    def __init__(self):
	self.scores = []
	try:
	        f = open("highscores.txt", "rb")
        	self.scores = pickle.load(f)
        	f.close()
	except IOError:
		print 'No highscores yet'
        
        self.new_score = 0
        self.new_score_pos = 0

        text_font = pygame.font.Font(None, 35)
        title_font = pygame.font.Font(None, 80)

        self.title = title_font.render("Game Over", 1, (0,0,0))
        self.body_text1 = text_font.render("You got " + str(self.new_score) + " points. Give your name/nick, please", 1, (0,0,0))

        self.done_button = button((450,590), (300,80), "Done")

        but_list0 = ["1","2","3","4","5","6","7","8","9","0"]
        but_list1 = ["q","w","e","r","t","y","u","i","o","p","å","^"]
        but_list2 = ["a","s","d","f","g","h","j","k","l","ö","ä","'"]
        but_list3 = ["z","x","c","v","b","n","m",",",".","-","_"]
        
        self.char_buttons = []
        x_pos = 320
        y_pos = 300
        for char in but_list0:
            self.char_buttons.append([button((x_pos, y_pos), (45,45), char), char])
            x_pos += 45

        x_pos = 350
        y_pos = 345
        for char in but_list1:
            self.char_buttons.append([button((x_pos, y_pos), (45,45), char), char])
            x_pos += 45

        x_pos = 370
        y_pos = 390
        for char in but_list2:
            self.char_buttons.append([button((x_pos, y_pos), (45,45), char), char])
            x_pos += 45

        x_pos = 400
        y_pos = 435
        for char in but_list3:
            self.char_buttons.append([button((x_pos, y_pos), (45,45), char), char])
            x_pos += 45

        self.space = button((450,500), (300,45), "")
        self.caps = button((280,390), (90,45), "Caps")
        self.backspace = button((770,300), (90,45), "<-")

        self.caps_state = False
        self.new_name = ""
        self.count = 0

        
    def upload_highscore(self, score):
        self.new_score = score
        text_font = pygame.font.Font(None, 35)
        self.body_text1 = text_font.render("You got " + str(self.new_score) + " points. Give your name/nick, please", 1, (0,0,0))
        self.new_name = ""

    def update(self, screen, cursor):
        screen.blit(self.title, (450,80))
        screen.blit(self.body_text1, (270,180))

        if self.caps.update(screen, cursor, self.caps_state):
            if self.caps_state:
                self.caps_state = False
            else:
                self.caps_state = True

        if self.backspace.update(screen, cursor, False) and len(self.new_name) > 0:
            self.new_name = self.new_name[0:-1]

        if self.space.update(screen, cursor, False):
            self.new_name += " "            

        for but in self.char_buttons:
            if but[0].update(screen, cursor, False):
                if self.caps_state:
                    self.new_name += string.upper(but[1])
                else:
                    self.new_name += but[1]

        text_font = pygame.font.Font(None, 50)
        pleijah = text_font.render(self.new_name, 1, (0,0,0))
        pw = pleijah.get_width()
        screen.blit(pleijah, (590-pw/2,230))

        if self.count < 30:
            pygame.draw.line(screen, (0,0,0), (590+pw/2, 270), (610+pw/2, 270), 3)

        self.count += 1
        if self.count > 60:
            self.count = 0

        
        if self.done_button.update(screen, cursor, False):
            self.new_name = self.new_name.strip()
            if self.new_name == "":
                self.new_name = "Anonymous"
            self.save_to_scores(self.new_name, self.new_score)
            return "highscores"
        return "appendscore"

    def save_to_scores(self, name, score):

        score_added = False
        for i in range(0,len(self.scores)):
            if self.scores[i][1] <= score:
                score_added = True
                self.scores.insert(i, [name, score])
                self.new_score_pos = i+1
                break

        if not score_added:
            self.scores.append([name, score])
            self.new_score_pos = len(self.scores)
            
        f = open("highscores.txt", "wb")
        pickle.dump(self.scores, f)
        f.close()

    def score_pos(self):
        return self.new_score_pos


class highscores:
    def __init__(self):
        title_font = pygame.font.Font(None, 75)
        self.title = title_font.render("High scores", 1, (0,0,0))
        self.scores = []

        self.new_game_button = button((900,590), (300,80), "New Game")
        self.menu_button = button((450,590), (300,80), "Main Menu")


    def reload_scores(self, highlight, score_pos = 0):
	score_list = []
	try:
	        f = open("highscores.txt", "rb")
        	score_list = pickle.load(f)
        	f.close()
	except IOError:
		print 'No highscores yet'

        self.score_pos = score_pos
        self.highlight = highlight

	#print 'hs', self.highlight, self.score_pos

        list_len = len(score_list)

        text_font = pygame.font.Font(None, 30)

        self.dots = text_font.render("...", 1, (0,0,0))

        self.scores = []

        counter = 1
        for score in score_list:
            name = score[0]

            if len(name) > 20:
                name = name[0:20]

            if score_pos == counter and highlight:
                colour = (200,0,0)
            else:
                colour = (0,0,0)

            one_score = []
            one_score.append(text_font.render(str(counter)+".", 1, colour))
            one_score.append(text_font.render(name, 1, colour))
            one_score.append(text_font.render(str(score[1]), 1, colour))
            
            self.scores.append(one_score)
            counter += 1



    def update(self, screen, cursor):
        screen.blit(self.title, (450,80))
        min_pos = 0
        max_pos = len(self.scores)

	#print 'hs2', self.highlight, self.score_pos

        if not self.highlight or (self.highlight and self.score_pos < 11):
            for i in range(0,11):
                if i < max_pos and i >= min_pos:
                    screen.blit(self.scores[i][0], (350,210+i*30))
                    screen.blit(self.scores[i][1], (530,210+i*30))
                    screen.blit(self.scores[i][2], (905,210+i*30))
                    
        elif self.highlight and self.score_pos > 10:
            for i in range(0,5):

                if i < max_pos and i >= min_pos:
                    screen.blit(self.scores[i][0], (350,210+i*30))
                    screen.blit(self.scores[i][1], (530,210+i*30))
                    screen.blit(self.scores[i][2], (905,210+i*30))
            screen.blit(self.dots, (360,210+5*30))
            count = 6
            for i in range(self.score_pos-3,self.score_pos+2):
                if i < max_pos and i >= min_pos:
                    screen.blit(self.scores[i][0], (350,210+count*30))
                    screen.blit(self.scores[i][1], (530,210+count*30))
                    screen.blit(self.scores[i][2], (905,210+count*30))
                count += 1

        if self.new_game_button.update(screen, cursor, False):
            self.score_pos = 0
            self.highlight = False
            return "play"
        
        if self.menu_button.update(screen, cursor, False):
            self.score_pos = 0
            self.highlight = False
            return "welcome"

        return "highscores"
        

class welcome:
    def __init__(self):
        text_font = pygame.font.Font(None, 35)
        title_font = pygame.font.Font(None, 70)
        
        self.title = title_font.render("AK47 World Tour 1984", 1, (0,0,0))
        self.lines = []
        self.lines.append(text_font.render("The game is created by Hackerspace 5w, Tampere (5w.fi)", 1, (0,0,0)))
	self.lines.append(text_font.render("", 1, (0,0,0)))
        self.lines.append(text_font.render("-Use \"real\" sights as there is no virtual sight in the game", 1, (0,0,0)))
	self.lines.append(text_font.render("-You have 30 rounds in one magazine, after that reload is needed", 1, (0,0,0)))
	self.lines.append(text_font.render("-Make your motherland proud!", 1, (0,0,0)))

        self.new_game_button = button((900,590), (300,80), "New Game")
        self.high_scores_button = button((450,590), (300,80), "High Scores")

    def update(self, screen, cursor):
        screen.blit(self.title, (400,80))
        lpos = 220
        for line in self.lines:
            screen.blit(line, (150,lpos))
            lpos += 40

        #pygame.draw.circle(screen, (255,0,0), (200,200), 30)

        if self.new_game_button.update(screen, cursor, False):
            return "play"

        if self.high_scores_button.update(screen, cursor, False):
            return "highscores"

        return "welcome"
        

class button:
    def __init__(self, pos, size, text):
        self.pos = pos
        self.size = size
        font = pygame.font.SysFont(None, 35)
        font.set_bold(True)
        self.text = font.render(text, 1, (0,0,0))
        tsize = self.text.get_size()
        self.bpos = [self.size[0]/2 - tsize[0]/2 + self.pos[0], self.size[1]/2 - tsize[1]/2 + self.pos[1]]
        self.old_mouse = [0,0]
        self.trigger = True

    def update(self, screen, cursor, green):
        pushed = False
        trigger_change = False

        # trigger was activated
        if not self.trigger and cursor[2] == True : 
            trigger_change = True
            self.trigger = True
        elif self.trigger and cursor[2] == False:
            self.trigger = False


        # cursor is over the button
        if (cursor[0] > self.pos[0] and cursor[0] < self.pos[0] + self.size[0] and \
           cursor[1] > self.pos[1] and cursor[1] < self.pos[1] + self.size[1]) and trigger_change:
            pushed = True

        # background of the button
        if green:
            pygame.draw.rect(screen, (0,255,0), [self.pos, self.size], 0)
        else:
            pygame.draw.rect(screen, (150,150,150), [self.pos, self.size], 0)

        # border
        pygame.draw.rect(screen, (0,0,0), [self.pos, self.size], 1)

        # button text    
        screen.blit(self.text, self.bpos)

        return pushed     
        
