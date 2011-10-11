# -*- coding: cp1252 -*-
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


class appendscore:
    def __init__(self):
        f = open("highscores.txt", "rb")
        self.scores = pickle.load(f)
        f.close()
        
        self.new_score = 0
        self.new_score_pos = 0

        text_font = pygame.font.Font(None, 22)
        title_font = pygame.font.Font(None, 40)

        self.title = title_font.render("Game Over", 1, (0,0,0))
        self.body_text1 = text_font.render("You got " + str(self.new_score) + " points. Give your name/nick, please", 1, (0,0,0))

        self.done_button = button((225,380), (150,50), "Done")

        but_list0 = ["1","2","3","4","5","6","7","8","9","0"]
        but_list1 = ["q","w","e","r","t","y","u","i","o","p","å","^"]
        but_list2 = ["a","s","d","f","g","h","j","k","l","ö","ä","'"]
        but_list3 = ["z","x","c","v","b","n","m",",",".","-","_"]
        
        self.char_buttons = []
        x_pos = 130
        y_pos = 180
        for char in but_list0:
            self.char_buttons.append([button((x_pos, y_pos), (30,30), char), char])
            x_pos += 30

        x_pos = 145
        y_pos = 210
        for char in but_list1:
            self.char_buttons.append([button((x_pos, y_pos), (30,30), char), char])
            x_pos += 30

        x_pos = 160
        y_pos = 240
        for char in but_list2:
            self.char_buttons.append([button((x_pos, y_pos), (30,30), char), char])
            x_pos += 30

        x_pos = 175
        y_pos = 270
        for char in but_list3:
            self.char_buttons.append([button((x_pos, y_pos), (30,30), char), char])
            x_pos += 30

        self.space = button((225,310), (150,30), "")
        self.caps = button((100,240), (60,30), "Caps")
        self.backspace = button((430,180), (60,30), "<-")

        self.caps_state = False
        self.new_name = ""
        self.count = 0

        
    def upload_highscore(self, score):
        self.new_score = score
        text_font = pygame.font.Font(None, 22)
        self.body_text1 = text_font.render("You got " + str(self.new_score) + " points. Give your name/nick, please", 1, (0,0,0))
        self.new_name = ""

    def update(self, screen, cursor):
        screen.blit(self.title, (225,40))
        screen.blit(self.body_text1, (105,90))

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

        text_font = pygame.font.Font(None, 30)
        pleijah = text_font.render(self.new_name, 1, (0,0,0))
        pw = pleijah.get_width()
        screen.blit(pleijah, (295-pw/2,145))

        if self.count < 30:
            pygame.draw.line(screen, (0,0,0), (297+pw/2, 145), (297+pw/2, 163), 3)

        self.count += 1
        if self.count > 60:
            self.count = 0

        
        if self.done_button.update(screen, cursor, False):
            self.new_name = self.new_name.strip()
            if self.new_name == "":
                self.new_name = "Anonymous"
            self.save_to_scores(self.new_name, self.new_score)
            return "high_scores"
        return "append_score"

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
    def __init__(self, highlight, score_pos = 0):
        f = open("highscores.txt", "rb")
        score_list = pickle.load(f)
        f.close()
        self.score_pos = score_pos
        self.highlight = highlight

        list_len = len(score_list)

        text_font = pygame.font.Font(None, 22)
        title_font = pygame.font.Font(None, 40)

        self.title = title_font.render("High scores", 1, (0,0,0))
        self.scores = []

        self.dots = text_font.render("...", 1, (0,0,0))

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

        self.new_game_button = button((450,380), (150,50), "New Game")
        self.menu_button = button((225,380), (150,50), "Main Menu")

    def update(self, screen, cursor):
        screen.blit(self.title, (225,40))
        min_pos = 0
        max_pos = len(self.scores)

        if not self.highlight or (self.highlight and self.score_pos < 11):
            for i in range(0,11):
                if i < max_pos and i >= min_pos:
                    screen.blit(self.scores[i][0], (175,110+i*20))
                    screen.blit(self.scores[i][1], (215,110+i*20))
                    screen.blit(self.scores[i][2], (405,110+i*20))
                    
        elif self.highlight and self.score_pos > 10:
            for i in range(0,5):
                if i < max_pos and i >= min_pos:
                    screen.blit(self.scores[i][0], (175,110+i*20))
                    screen.blit(self.scores[i][1], (215,110+i*20))
                    screen.blit(self.scores[i][2], (405,110+i*20))
            screen.blit(self.dots, (215,110+5*20))
            count = 6
            for i in range(self.score_pos-3,self.score_pos+2):
                if i < max_pos and i >= min_pos:
                    screen.blit(self.scores[i][0], (175,110+count*20))
                    screen.blit(self.scores[i][1], (215,110+count*20))
                    screen.blit(self.scores[i][2], (405,110+count*20))
                count += 1

        if self.new_game_button.update(screen, cursor, False):
            self.score_pos = 0
            self.highlight = False
            return "new_game"
        
        if self.menu_button.update(screen, cursor, False):
            self.score_pos = 0
            self.highlight = False
            return "main_menu"

        return "high_scores"
        

class welcome:
    def __init__(self):
        text_font = pygame.font.Font(None, 22)
        title_font = pygame.font.Font(None, 40)
        
        self.title = title_font.render("DuckReHunt 3.0", 1, (0,0,0))
        self.lines = []
        self.lines.append(text_font.render("Duck hunt clone orginally developed by Michael Bachmann", 1, (0,0,0)))
        self.lines.append(text_font.render("and heavily modified by Hackerspace 5w, Tampere (5w.fi)", 1, (0,0,0)))
        self.lines.append(text_font.render("", 1, (0,0,0)))
        self.lines.append(text_font.render("-You have 30 seconds to shoot down as many ducks as you can", 1, (0,0,0)))
        self.lines.append(text_font.render("-Unlimited ammos, no reloads", 1, (0,0,0)))
        self.lines.append(text_font.render("-Every bullet fired decreases points by one", 1, (0,0,0)))
        self.lines.append(text_font.render("-For every duck killed you gain five points", 1, (0,0,0)))
        self.lines.append(text_font.render("-Use \"real\" sights as there is no virtual sight in the game", 1, (0,0,0)))

        self.new_game_button = button((450,380), (150,50), "New Game")
        self.high_scores_button = button((225,380), (150,50), "High Scores")

    def update(self, screen, cursor):
        screen.blit(self.title, (200,40))
        lpos = 110
        for line in self.lines:
            screen.blit(line, (45,lpos))
            lpos += 20

        #pygame.draw.circle(screen, (255,0,0), (200,200), 30)

        if self.new_game_button.update(screen, cursor, False):
            return "new_game"

        if self.high_scores_button.update(screen, cursor, False):
            return "high_scores"

        return "main_menu"
        

class button:
    def __init__(self, pos, size, text):
        self.pos = pos
        self.size = size
        font = pygame.font.SysFont(None, 22)
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
        
