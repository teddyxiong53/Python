#!/usr/bin/python
# -*- coding: utf-8 -*-

from aip import AipSpeech
import os, sys, os.path

APP_ID = '11234074'
API_KEY = 'wNqEyF2KysMTiOcSt3HEZYhcvb0hjriX'
SECRET_KEY = '97UrqLeyNXhjtLeqL5XNPxYvAEQsGb7S'


client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

sentence_dict = {
# "link_start_first.mp3" : "你好，我是小度，你的语音助理，请下载并打开国美智能APP，扫描音箱说明书上的二维码，按照提示设置吧",
# "re_link.mp3" : "正在为你联网，请稍后",
# "link_start.mp3" : "已进入配网模式",
# "net_config_timeout.mp3" : "请下载并打开国美智能APP，扫描音箱说明书上的二维码，按照提示设置吧",
# "link_success.mp3" : "配置成功，现在可以对我说小度小度开始体验啦",
# "link_failed_ip.mp3" : "联网失败了，请检查你的网络密码，并重新启动配网",
# "link_failed_ping.mp3" : "网络配置失败，建议长按音箱底部RST 5秒，恢复出厂设置",
# "unbound.mp3" : "联网失败了，请通过app设置您的账号",
# "gome/recovery_hint.mp3" : "即将恢复出厂设置", #"即将恢复出厂设置， 咚咚咚"
# "gome/low_battery_hint.mp3" : "电量不足，请及时充电",
# "network_connect_failed.mp3" : "联网失败了，请检查你的网络",
# "network_slow.mp3" : "网络有点慢，请稍等",
# "open_bluetooth.mp3" : "蓝牙已打开",
# "close_bluetooth.mp3" : "蓝牙已关闭",
# "bt_connect.mp3" : "蓝牙已连接",
# "bt_disconnect.mp3" : "蓝牙已断开",
# "gome/response_ai.mp3" : "哎",
# "gome/response_en.mp3" : "嗯",
# "gome/response_wozai.mp3" : "我在",
# "gome/response_zai.mp3" : "在",
# "gome/sleep_mode.mp3" : "好的,已休眠",
# "bt_pair_success.mp3" : "蓝牙已连接",
# "link_exit.mp3" : "联网已取消",
# "server_connect_failed.mp3" : "联网失败了，请检查你的网络",
# "server_connecting.mp3" : "正在为你联网，请稍后",
# "link_connecting.mp3" : "正在为你联网，请稍后",
# "shutdown.mp3": "正在关机",
# "re_link_success.mp3": "联网成功",
# "mic_disable.mp3": "麦克风已禁用",
#"re_link_failed.mp3": "联网失败了，请检查你的网络",
# "low_battery_operate.mp3":"电量过低，请充电后再进行操作",
# "mic_enable.mp3": "麦克风已开启",
# "update_hint.mp3": "正在升级",
# "begin_download.mp3": "开始下载升级包",
# "download_ok.mp3": "升级包下载完成",
# "download_fail.mp3": "升级包下载出错，请重新下载",
# "mic_disable_suffix.mp3" : "你可以双击音箱顶部触摸键来打开麦克风",
# "link_restart.mp3" : "联网失败了，重新进入配网模式，请确认网络密码后重试",
# "music_play_error.mp3": "播放遇到一点小状况，请稍后再试",
# "update_ok.mp3": "升级成功",
# "update_fail.mp3": "升级失败",


"10抱歉，没找到您需要的内容，换一个话题吧。.mp3" :  "Sorry, I haven't find what you need. Please change your topic.",
"11没听清，请再说一次。.mp3" : "Pardon?",
"12这个问题我还没有学会.mp3" : "Sorry, I don't know.",
"13主人，好像您没有说话.mp3" : "Please tell me your question",
"14主人，您和我交流，您需要安装一个专用APP.mp3" : "You need to install the companion APP to communicate with me",
"15主人，您手机的专用APP还没有打开，请打开一下吧.mp3" : "Please open the companion APP firstly",
"16主人，我的电量快用完了.mp3" : "My battery is running out.",
"5正在连接蓝牙设备.mp3" : "Now is connecting to the bluetooth device",
"6连接成功.mp3" : "Connection succeeded",
"7未找到蓝牙设备，请再试一次.mp3" : "Can not find the bluetooth device, please try again",
"8Hi，欢迎回来.mp3" : "Hi, welcome back",
"9正在帮你搜索，请稍候.mp3" : "Now is searching device, please wait a moment",
}

for (k,v) in sentence_dict.items():
	
	if len(sys.argv)< 2:
		print "./gen_tts number"
		print "发音人选择, 0为女声， 1为男声，3为情感合成-度逍遥， 4为情感合成-度丫丫，默认为普通女"
		sys.exit(1)
	person = sys.argv[1]
	dir = sys.argv[2]
	filename = './' + dir + k
	spd = sys.argv[3]
	pit = sys.argv[4]
	
	if True: #not os.access(filename, os.F_OK):
		result  = client.synthesis(v, 'zh', 1, {
			'vol': 7,
			'per': int(person),
			'spd': int(spd),
			'pit': int(pit)
		})
		if not isinstance(result, dict):
			with open(filename, 'wb') as f:
				print "write to " + filename
				f.write(result)
	else:
		#print filename + "already exists"
		pass