import cwiid
from math import *
import copy
import pickle

class Ak47:
    def __init__(self):
        self.ir_pos = []
        self.dist = 0 #distance to sensobar in cm
        self.cpoint = [0,0]
        self.calib_points = []
        self.maxmin = []
        self.fire_button = False
        self.dist_values = []

	fov_scale = 1.33
        self.x_pix = fov_scale*33/1024.0 #[deg/pixel]
        self.y_pix = fov_scale*23/768.0  #[deg/pixel]
        
        self.wiimote = cwiid.Wiimote()
	led = 0
        led ^= cwiid.LED1_ON
        self.wiimote.led = led

        self.wiimote.mesg_callback = self.callback

	rpt_mode = 0
        rpt_mode ^= cwiid.RPT_IR
        self.wiimote.rpt_mode = rpt_mode
        rpt_mode ^= cwiid.RPT_BTN
        self.wiimote.rpt_mode = rpt_mode

        self.wiimote.enable(cwiid.FLAG_MESG_IFC)

    def close(self):
        self.wiimote.close()

    def save_calibration(self, file_name):
        f = open(file_name, "w+")
        pickle.dump(self.maxmin, f)
        f.close()

    def load_calibration(self, file_name):
        f = open(file_name)
        self.maxmin = pickle.load(f)
        f.close()

    def is_calibrated(self):
        return len(self.maxmin) > 0

    def decalibrate(self):
        self.minmax = []
        self.calib_points = []

    def get_pos(self):
        self.calc_distance()
        self.center_point()

        if not self.is_calibrated():
            ret_x = self.cpoint[0] / 1024.0
            ret_y = self.cpoint[1] / 768.0
            return [ret_x, ret_y], self.fire_button

        x = self.dist * tan(self.x_pix*self.cpoint[0]*pi/180)
        y = self.dist * tan(self.y_pix*self.cpoint[1]*pi/180)

        x_scale = 1.0/(self.maxmin[0] - self.maxmin[1])
        y_scale = 1.0/(self.maxmin[2] - self.maxmin[3])

        x_scaled = x_scale*(self.maxmin[0] - x)
        y_scaled = y_scale*(self.maxmin[2] - y)

        #print x,y,x_scale,y_scale,x_scaled,y_scaled

        ret_x = max([0.0, x_scaled])
        ret_x = min([1.0, ret_x])

        ret_y = max([0.0, y_scaled])
        ret_y = min([1.0, ret_y])

        return [ret_x, ret_y], self.fire_button 
        

    def calibrate(self, calib_index):
        self.calc_distance()
        self.center_point()
        temp_pos = copy.deepcopy(self.cpoint)
        
        if calib_index < 3:
            self.calib_points.append(temp_pos)            
            return
        else:
            self.calib_points.append(temp_pos)

        calib_min_x1 = self.dist * tan(self.x_pix*self.calib_points[0][0]*pi/180)
        calib_min_x2 = self.dist * tan(self.x_pix*self.calib_points[1][0]*pi/180)

        calib_min_y1 = self.dist * tan(self.y_pix*self.calib_points[0][1]*pi/180)
        calib_min_y2 = self.dist * tan(self.y_pix*self.calib_points[3][1]*pi/180)

        calib_max_x1 = self.dist * tan(self.x_pix*self.calib_points[2][0]*pi/180)
        calib_max_x2 = self.dist * tan(self.x_pix*self.calib_points[3][0]*pi/180)

        calib_max_y1 = self.dist * tan(self.y_pix*self.calib_points[1][1]*pi/180)
        calib_max_y2 = self.dist * tan(self.y_pix*self.calib_points[2][1]*pi/180)

        if abs(calib_min_x1 - calib_min_x2) > 25:
            print "calib error #1", calib_min_x1, calib_min_x2

        if abs(calib_max_x1 - calib_max_x2) > 25:
            print "calib error #2", calib_max_x1, calib_max_x2

        if abs(calib_min_y1 - calib_min_y2) > 25:
            print "calib error #3", calib_min_y1, calib_min_y2

        if abs(calib_max_y1 - calib_max_y2) > 25:
            print "calib error #4", calib_max_y1, calib_max_y2

        self.maxmin = [ (calib_min_x1 + calib_min_x2) / 2.0, \
                        (calib_max_x1 + calib_max_x2) / 2.0, \
                        (calib_min_y1 + calib_min_y2) / 2.0, \
                        (calib_max_y1 + calib_max_y2) / 2.0 ]
	
	print "calib points", self.calib_points
	print "calib points2", calib_min_x1, calib_min_x2, calib_max_x1, calib_max_x2, \
                              calib_min_y1, calib_min_y2, calib_max_y1, calib_max_y2
	print "minmax", self.maxmin


    def valid_value(self):
	if len(self.ir_pos) != 4:
	    return False 

        if self.ir_pos[0] == None or self.ir_pos[1] == None or \
           self.ir_pos[2] != None or self.ir_pos[3] != None:
            return False
	
	return True

      
    def center_point(self):
	
        if not self.valid_value():
            return

	led1 = self.ir_pos[0]["pos"]
	led2 = self.ir_pos[1]["pos"]

        self.cpoint[0] = 1024 - (led1[0] + led2[0]) / 2.0
        self.cpoint[1] = (led1[1] + led2[1]) / 2.0

    #distance to screen [cm]
    def calc_distance(self):
        ir_sensor_width = 19    #[cm]

        pix = (self.x_pix + self.y_pix) / 2.0

        if not self.valid_value():
            return

	led1 = self.ir_pos[0]["pos"]
	led2 = self.ir_pos[1]["pos"]

        # angle between ir-blobs
        alfa = sqrt( (led1[0] - led2[0]) ** 2 + (led1[1] - led2[1]) ** 2 ) * pix

        
        local_dist = ir_sensor_width / tan(alfa*pi/180)
        #self.dist = tan(alfa*pi/180)


        # mean value filtering (low pass filter)
        self.dist_values.append(local_dist)

        if len(self.dist_values) > 10:
            self.dist_values.pop(0)

        self.dist = 0

        for dist in self.dist_values:
            self.dist += dist 

        self.dist = self.dist/len(self.dist_values)


    def callback(self, mesg_list, time):
        for mesg in mesg_list:      
            if mesg[0] == cwiid.MESG_BTN:
		if mesg[1]==4:
                    self.fire_button = True
		if mesg[1]==0:
                    self.fire_button = False
		
            elif mesg[0] == cwiid.MESG_IR:
                self.ir_pos = mesg[1]
 
            elif mesg[0] ==  cwiid.MESG_ERROR:
                print "Wiimote: Error message received"
                self.wiimote.close()
                exit(-1)
            else:
                print "Wiimote: Unknown Report"

##print ""
##mote = Ak47()
##mote.ir_pos = [[521,400], [600,400]]
##mote.calc_distance()
##print mote.dist
##
##print ""
##print mote.is_calibrated()
##print mote.get_pos()
##
##print ""
##mote.ir_pos = [[800,750], [1000,750]]
##mote.calibrate(0)
##mote.ir_pos = [[800,50], [1000,50]]
##mote.calibrate(1)
##mote.ir_pos = [[50,50], [250,50]]
##mote.calibrate(2)
##mote.ir_pos = [[50,750], [250,750]]
##mote.calibrate(3)
##print mote.maxmin
##print ""
##print mote.is_calibrated()
##
##print ""
##mote.ir_pos = [[100,700], [300,700]]
##print mote.get_pos()
##mote.ir_pos = [[700,20], [900,20]]
##print mote.get_pos()




        

