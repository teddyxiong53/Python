#!/usr/bin/python

from PIL import Image
import sys
import os
import glob

"""


struct led_frame {
  unsigned char data[3*19];
};


struct led_scene {
	int id;
	int count;
	struct led_frame *frames;
};

//init function, alloc memory

struct led_scene LED_WAKE_UP_SCENE = {
	LED_WAKE_UP
	20,
	&LED_WAKE_UP_DATA,
};
struct led_frame LED_WAKE_UP_DATA[] = {
	255,0,0,//1
	
};
struct led_scene LED_ALARM_SCENE = {
	LED_ALARM,
	40,
	&LED_ALARM_DATA,
};
struct led_frame LED_ALARM_DATA[] = {
	255,0,0,//1
	
};
"""
little_circle_origin = [
	(177,177),
	(243,177),
	(211,239),
	(143,239),
	(112,177),#5
	(143,116),
	(211,116),
	(308,177),
	(283,239),
	(243,291),#10
	(177,300),
	(112,291),
	(71,239),
	(46,177),
	(71,116),#15
	(112,64),
	(177,54),
	(243,64),
	(283,116)
]

scene_lists = [
	"LED_NET_RECOVERY",
	"LED_NET_WAIT_CONNECT",
	"LED_NET_DO_CONNECT",
	"LED_NET_CONNECT_FAILED",
	"LED_NET_CONNECT_SUCCESS",
	"LED_NET_WAIT_LOGIN",
	"LED_NET_DO_LOGIN",
	"LED_NET_LOGIN_FAILED",
	"LED_NET_LOGIN_SUCCESS",

	"LED_WAKE_UP_DOA",
	"LED_WAKE_UP",
	"LED_SPEECH_PARSE",
	"LED_PLAY_TTS",
	"LED_PLAY_RESOURCE",

	"LED_BT_WAIT_PAIR",
	"LED_BT_DO_PAIR",
	"LED_BT_PAIR_FAILED",
	"LED_BT_PAIR_SUCCESS",
	"LED_BT_PLAY",
	"LED_BT_CLOSE",

	"LED_VOLUME",
	"LED_MUTE",

	"LED_DISABLE_MIC",

	"LED_ALARM",

	"LED_SLEEP_MODE",

	"LED_OTA_DOING",
	"LED_OTA_SUCCESS",

	"LED_CLOSE_A_LAYER",
]


pic_w = 0
pic_h = 0


	


scene_dirs = glob.glob("./LED_*")
scene_dirs.sort()



def get_rgb(dot, pix, i, j, cur_dir):
	x = dot[0]
	y = dot[1]
	r,g,b = pix[x,y]
	
	if cur_dir == './LED_NET_WAIT_CONNECT':
		#msg = str(r) + str(g) + str(b) + "\n"
		#sys.stderr.write(msg)
		if 50<r<55 and 40<g<48 and 40< b<45:
			r,g,b = (0,0,0)
	#print pix[x,y]
	print "\t\t\t" + str(r) + ", " + str(g) + ", " + str(b) + "," + "//" + str(i)
	

	
def print_files():
	msg = "==========================\n"
	msg += "the all files is as below:\n"
	msg += str(file_lists)
	msg += "\n"
	msg += "==========================\n"
	sys.stderr.write(msg)
	
def get_scene_dirs():
	msg = str(scene_dirs)
	msg += "\n"
	#print msg
	sys.stderr.write(msg)
	
def process_file(f, d):
	cur_dir = d
	global pic_w, pic_h
	im = Image.open(f)
	pix = im.load()
	pic_w = im.size[0]
	pic_h = im.size[1]
	if pic_w == 0 or pic_h == 0:
		msg = "pic witdh :" + str(pic_w) + "pic height :" + str(pic_h) + "\n"
		sys.stderr.write(msg)
		sys.exit(-1)
	i = 0
	j = 0
	for dot in little_circle_origin:
		i = i+1
		get_rgb(dot, pix, i, j, cur_dir)
		j = j+1
	
def process_dir():
	dir_idx = 0
	print """#include \"led_scene.h\""""
	var_file = open('led_scene_var.h', 'w')
	var_file.truncate(0)
	msg = """
#ifndef __LED_SCENES_VAR_H__
#define __LED_SCENES_VAR_H__

#ifdef __cplusplus
extern "C" {
#endif

"""
	var_file.write(msg)
	
	for d in scene_dirs:
		msg = "==============processing dir: "+  d + "================\n"
		sys.stderr.write(msg)
		jpg_filter = d + "/*.jpg"
		file_lists = glob.glob(jpg_filter)
		file_lists.sort()
		file_num = len(file_lists)
		scene_name = d[2:]
		msg = scene_name + "\n"
		sys.stderr.write(msg)
		
		file_idx = 0
		msg = "struct led_frame " + scene_name + "_DATA[] = {"
		print msg

		for f in file_lists:
			msg = ">> processing "+  f + "\n"
			sys.stderr.write(msg)
			print "\t[" + str(file_idx) + "]" + " = {"
			print "\t\t.data = {"
			process_file(f,d)
			print "\t\t},"
			print "\t}," 
			file_idx += 1
		print "};"
		msg = "struct led_scene " + scene_name + "_SCENE = {"
		print msg
		print "\t" + scene_name + ","
		print "\t" + str(file_num) + ","
		print "\t" +  scene_name + "_DATA" + ","
		print "};"
		msg = "extern struct led_scene " + scene_name + "_SCENE;\n"
		var_file.write(msg)
	msg = """
#ifdef __cplusplus
}
#endif

#endif
	"""
	var_file.write(msg)
	var_file.close()
def main():
	get_scene_dirs()
	process_dir()

	
if __name__ == '__main__':
	main()