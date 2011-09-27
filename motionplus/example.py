import cwiid
wm = cwiid.Wiimote()
wm.enable(cwiid.FLAG_MOTIONPLUS)
wm.rpt_mode = cwiid.RPT_ACC | cwiid.RPT_MOTIONPLUS
print wm.state
wm.disable(cwiid.FLAG_MOTIONPLUS)
print wm.state
