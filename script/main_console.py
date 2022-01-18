#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : ARK Backup
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/ark_backup/
# ::Class    : CLS_Main_Console
#####################################################
from backup_main import CLS_BackupMain

from osif import CLS_OSIF
from botctrl import CLS_BotCtrl
from mydisp import CLS_MyDisp
from gval import gVal
#####################################################
class CLS_Main_Console() :
#####################################################
	#使用クラス実体化
	OBJ_BackupMain = ""

#####################################################
# 実行
#####################################################
	@classmethod
	def sRun(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Main_Console"
		wRes['Func']  = "sRun"
		
		#############################
		# botテスト、引数ロード
		#   テスト項目
		#     1.引数ロード
		#     2.データベースの取得
		#     3.ログの取得
		#     4.排他
		#     5.Twitterの取得
		#     6.Readme情報の取得
		#     7.Python情報の取得
		#     8.TESTログ記録
		wResTest = CLS_BotCtrl.sBotTest()
		if wResTest!=True :
			return	#問題あり
		
		# ※通常処理継続
		gVal.FLG_Console_Mode = True				#コンソールモード
		
		cls.OBJ_BackupMain = CLS_BackupMain()		#バックアップメイン
		wRes = cls.OBJ_BackupMain.Init()
		if wRes['Result']!=True :
			CLS_OSIF.sErr( wRes )
			return
		
		#############################
		# コンソールを表示
		while True :
			wCommand = cls().sViewMainConsole()
			
			if wCommand=="" :
				###未入力は再度入力
				continue
			
			if wCommand.find("\\q")>=0 or wCommand=="exit" :
				###終了
				break
			
			wResCmd = cls().sRunCommand( wCommand )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			
		return



#####################################################
# メインコンソール画面の表示
#####################################################
	@classmethod
	def sViewMainConsole(cls):
		
		#############################
		# メインコンソール画面
		wResDisp = CLS_MyDisp.sViewDisp( "MainConsole" )
		if wResDisp['Result']==False :
			return "\\q"	#失敗=強制終了
		
		wCommand = CLS_OSIF.sInp( "コマンド？=> " )
		return wCommand



#####################################################
# 実行
#####################################################
	@classmethod
	def sRunCommand( cls, inCommand ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Main_Console"
		wRes['Func']  = "sRunCommand"
		
		wCLS_work = ""
		wFlg = False
		
	#####################################################
		#############################
		# ARKデータ更新
		if inCommand=="\\g" :
			cls.OBJ_BackupMain.GetARKdate()
			wFlg = True
		
		#############################
		# 手動バックアップ
		if inCommand=="\\mb" :
			cls.OBJ_BackupMain.ManualBackup()
			wFlg = True
		
		#############################
		# 定期バックアップ
		if inCommand=="\\cb" :
			cls.OBJ_BackupMain.CircleBackup()
			wFlg = True
		
		#############################
		# システム情報の表示
		if inCommand=="\\v" :
			cls().sView_Sysinfo()
			wFlg = True
		
	#####################################################
		#############################
		# ないコマンド
		if wFlg!=True :
			wRes['Reason'] = "存在しないコマンド :" + str(inCommand)
		
		return wFlg



#####################################################
# システム情報の表示
#####################################################
	@classmethod
	def sView_Sysinfo(cls):
		
		#############################
		# 画面クリア
		CLS_OSIF.sDispClr()
		
		#############################
		# ヘッダ表示
		wStr = "--------------------" + '\n'
		wStr = wStr + " システム情報" + '\n'
		wStr = wStr + "--------------------" + '\n'
		
		#############################
		# 時間の取得
		wRes = CLS_OSIF.sGetTime()
		if wRes['Result']==True :
			wStr = wStr + wRes['TimeDate'] + '\n'
		
		#############################
		# 情報組み立て
		wStr = wStr + "Client Name = " + gVal.STR_SystemInfo['Client_Name'] + '\n'
		wStr = wStr + "Project Name= " + gVal.STR_SystemInfo['ProjectName'] + '\n'
		wStr = wStr + "github      = " + gVal.STR_SystemInfo['github'] + '\n'
		wStr = wStr + "Admin       = " + gVal.STR_SystemInfo['Admin'] + '\n'
		wStr = wStr + "Twitter URL = " + gVal.STR_SystemInfo['TwitterURL'] + '\n'
		wStr = wStr + "Update      = " + gVal.STR_SystemInfo['Update'] + '\n'
		wStr = wStr + "Version     = " + gVal.STR_SystemInfo['Version'] + '\n'
		
		wStr = wStr + "Python      = " + str( gVal.STR_SystemInfo['PythonVer'] )  + '\n'
###		wStr = wStr + "HostName    = " + gVal.STR_SystemInfo['HostName'] + '\n'
		
		#############################
		# コンソールに表示
		CLS_OSIF.sPrn( wStr )
		return



