import ak47
import time

mun_ak = ak47.Ak47()

count = 0
old_trig = False
mun_ak.load_calibration("calib.txt")

# calib_points = [[292.0, 473.5], [258.5, 690.0], [664.5, 751.5], [699.5, 537.0]]

for i in range(0,50):
	#print mun_ak.dist, mun_ak.ir_pos, len(mun_ak.ir_pos)
	pos, trig = mun_ak.get_pos()
	if trig and not old_trig and count < 4:
		mun_ak.calibrate(count)
		print "calibrated", count
		count += 1

	time.sleep(1)
	old_trig = trig
	print pos, trig

print mun_ak.calib_points
print mun_ak.maxmin
mun_ak.save_calibration("calib.txt")
