#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : ARK Backup
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/ark_backup/
# ::Class    : CLS_BotCtrl
#####################################################

from osif import CLS_OSIF
from filectrl import CLS_File
from gval import gVal
#####################################################
class CLS_BotCtrl():
#####################################################

#####################################################
# Botテスト
#####################################################
	@classmethod
	def sBotTest(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_BotCtrl"
		wRes['Func']  = "sBotTest"
		
		#############################
		# 引数取得
		wArg = CLS_OSIF.sGetArg()
		if len(wArg)==2 :	#テストモード : test か
			if wArg[1]==gVal.DEF_TEST_MODE :
				gVal.FLG_Test_Mode = True
		
		gVal.STR_SystemInfo['RunMode'] = "Normal"
		
		#############################
		# ARKのローカルプロファイルの存在チェック
		if CLS_File.sExist( gVal.DEF_STR_FILE['ARKcheck_file'] )!=True :
			## ファイルがない
			wRes['Reason'] = "ARKのローカルプロファイルが確認できません: path=" + gVal.DEF_STR_FILE['ARKcheck_file']
			CLS_OSIF.sErr( wRes )
			return False
		
		#############################
		# ユーザフォルダの存在チェック
		if CLS_File.sExist( gVal.DEF_USERDATA_PATH )!=True :
			## フォルダがなければ作成する
			if CLS_File.sMkdir( gVal.DEF_USERDATA_PATH )!=True :
				wRes['Reason'] = "フォルダの作成に失敗しました: path=" + gVal.DEF_USERDATA_PATH
				CLS_OSIF.sErr( wRes )
				return False
		
		#############################
		# 時間を取得
		wTD = CLS_OSIF.sGetTime()
		if wTD['Result']!=True :
			###時間取得失敗  時計壊れた？
			wRes['Reason'] = "PC時間取得失敗"
			CLS_OSIF.sErr( wRes )
			return
		### wTD['TimeDate']
		gVal.STR_SystemInfo['APIrect'] = str(wTD['TimeDate'])
		
		#############################
		# アプリVersion
		wReadme = []
		if CLS_File.sReadFile( gVal.DEF_STR_FILE['Readme'], outLine=wReadme )!=True :
			wRes['Reason'] = "Readme.mdファイルが見つかりません: path=" + gVal.DEF_STR_FILE['Readme']
			CLS_OSIF.sErr( wRes )
			return False
		
		if len(wReadme)<=1 :
			wRes['Reason'] = "Readme.mdファイルが空です: path=" + gVal.DEF_STR_FILE['Readme']
			CLS_OSIF.sErr( wRes )
			return False
		
		for wLine in wReadme :
			#############################
			# 分解+要素数の確認
			wLine = wLine.strip()
			wGetLine = wLine.split("= ")
			if len(wGetLine) != 2 :
				continue
			
			wGetLine[0] = wGetLine[0].replace("::", "")
			#############################
			# キーがあるか確認
			if wGetLine[0] not in gVal.STR_SystemInfo :
				continue
			
			#############################
			# キーを設定
			gVal.STR_SystemInfo[wGetLine[0]] = wGetLine[1]
		
		#############################
		# システム情報の取得
		wCLS_work = CLS_OSIF()
		gVal.STR_SystemInfo['PythonVer'] = wCLS_work.Get_PythonVer()
###		gVal.STR_SystemInfo['HostName']  = wCLS_work.Get_HostName()
		
		#############################
		# テスト終了
		return True



