class pyssy:
    def __init__(self, init_pos):
        self.vel_vect = [0,0]
        self.pos = init_pos
        self.comp = 4

    def compensation(self, pos):
        vel_vect = [pos[0] - self.pos[0], pos[1] - self.pos[1]]
        self.pos = pos
        return [self.pos[0] + vel_vect[0]*self.comp, \
                self.pos[1] + vel_vect[1]*self.comp]

pos = [0,0]
ak = pyssy(pos)

for i in range(0,200,5):
    print ak.compensation([i,i]), [i,i]

i = 195
print ak.compensation([i,i]), [i,i]
