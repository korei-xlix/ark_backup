#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : ARK Backup
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/ark_backup/
# ::Class    : CLS_BackupMain
#####################################################
from osif import CLS_OSIF
from filectrl import CLS_File
from mydisp import CLS_MyDisp
from gval import gVal
#####################################################
class CLS_BackupMain():
#####################################################

###	CHR_ARK_LastDate = "1901-01-01 00:00:00"		#ARK側 更新日時

	ARR_CircleFileList = {}							#定期バックアップファイル一覧
###	CHR_Circle_LastDate = "1901-01-01 00:00:00"		#定期バックアップ 最新日時
	CHR_Circle_LastFile = ""						#定期バックアップ 最新ファイル名



#####################################################
# Init
#####################################################
	def __init__(self):
###		self.OBJ_BackupMan = CLS_BackupMan( parentObj=self )
		return



#####################################################
# 初期化
#####################################################
	def Init(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_BackupMain"
		wRes['Func']  = "Init"
		
		#############################
		# ARK最終更新日 取得
		self.GetARKdate()
		
		#############################
		# 手動バックアップ 最終更新日 取得
		self.UpdateManualDate()
		
		#############################
		# 定期バックアップ一覧の取得
		self.GetCircleBackupList()
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# ARK最終更新日 取得
#####################################################
	def GetARKdate(self):
		wDate = CLS_File.sGetTimedate( gVal.DEF_STR_FILE['ARKcheck_file'] )
		if wDate=="" :
			gVal.FLG_ARK_Setted = False
			return False
		
###		self.CHR_ARK_LastDate = wDate
		gVal.CHR_ARK_LastDate = wDate
		gVal.FLG_ARK_Setted = True
		return True



#####################################################
# ARK最終更新日 チェック
#####################################################
	def CheckARKdate(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_BackupMain"
		wRes['Func']  = "CheckARKdate"
		
		wRes['Responce'] = False
		#############################
		# 最終更新日を取得
		wDate = CLS_File.sGetTimedate( gVal.DEF_STR_FILE['ARKcheck_file'] )
		if wDate=="" :
			wRes['Reason'] = "Get ARK Data is failed: file=" + gVal.DEF_STR_FILE['ARKcheck_file']
			return wRes
		
		if gVal.FLG_ARK_Setted==False :
			###元々取得に失敗していれば取得済 and 更新ありとする
			gVal.CHR_ARK_LastDate = wDate
			gVal.FLG_ARK_Setted = True
			wRes['Responce'] = True
			wRes['Result']   = True
			return wRes
		
		#############################
		# チェック判定
		if gVal.CHR_ARK_LastDate!=wDate :
			###変わっていれば更新あり
			wRes['Responce'] = True
		
		wRes['Result'] = True
		return wRes



#####################################################
# 手動バックアップ 最新日時更新
#####################################################
	def UpdateManualDate(self):
		wDate = CLS_File.sGetTimedate( gVal.DEF_STR_FILE['BackupMan_file'] )
		if wDate=="" :
			gVal.FLG_Manual_Setted = False
			return False
		
		gVal.CHR_Manual_LastDate = wDate
		gVal.FLG_Manual_Setted = True
		return True



#####################################################
# 定期バックアップ 最新日時更新
#####################################################
	def UpdateCircleDate( self, inFile, inDate ):
		if gVal.CHR_Circle_LastDate < inDate :
			gVal.CHR_Circle_LastDate = inDate
			self.CHR_Circle_LastFile = inFile
			gVal.FLG_Circle_Setted   = True
		return



#####################################################
# 定期バックアップ一覧 取得
#####################################################
	def GetCircleBackupList(self):
		
		self.ARR_CircleFileList = {}
		#############################
		# バックアップ一覧の作成
		wList = CLS_File.sFs( gVal.DEF_USERDATA_PATH, "circle_*.zip" )
		wIndex = 0
		for wFile in wList :
			wDate = CLS_File.sGetTimedate( gVal.DEF_USERDATA_PATH + wFile )
			if wDate=="" :
				continue
			
			wCell = {}
			wCell.update({ "File" : wFile })
			wCell.update({ "Date" : wDate })
			self.ARR_CircleFileList.update({ wIndex : wCell })
			wIndex += 1
			
			###最新更新日の更新
			self.UpdateCircleDate( wFile, wDate )
		
		#############################
		# 日時の降順に並べなおす(上が最新)
		### 退避領域の作成
		wCell = {}
		wCell.update({ "File" : None })
		wCell.update({ "Date" : "1901-01-01 00:00:00" })
		
		wLen = len( self.ARR_CircleFileList )
		for wIndex1 in range(wLen) :
			for wIndex2 in range(wLen) :
				if wIndex1==wIndex2 or wIndex1>wIndex2 :
					###同じキーか、ソート済みはスキップ
					continue
				
				if self.ARR_CircleFileList[wIndex1]['Date']>=self.ARR_CircleFileList[wIndex2]['Date'] :
					###上と同じ日時か最新ならスキップ
					continue
				
				### self.ARR_CircleFileList[wIndex1]['Date'] < self.ARR_CircleFileList[wIndex2]['Date']
				
				###入れ替え
				wCell['File'] = self.ARR_CircleFileList[wIndex1]['File']
				wCell['Date'] = self.ARR_CircleFileList[wIndex1]['Date']
				self.ARR_CircleFileList[wIndex1]['File'] = self.ARR_CircleFileList[wIndex2]['File']
				self.ARR_CircleFileList[wIndex1]['Date'] = self.ARR_CircleFileList[wIndex2]['Date']
				self.ARR_CircleFileList[wIndex2]['File'] = wCell['File']
				self.ARR_CircleFileList[wIndex2]['Date'] = wCell['Date']
		
		return



#####################################################
# 手動バックアップ
#####################################################
	def ManualBackup(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_BackupMain"
		wRes['Func']  = "ManualBackup"
		
		#############################
		# ARKのローカルプロファイルの存在チェック
		if CLS_File.sExist( gVal.DEF_STR_FILE['ARKcheck_file'] )!=True :
			## ファイルがない
			wRes['Reason'] = "ARKのローカルプロファイルが確認できません: path=" + gVal.DEF_STR_FILE['ARKcheck_file']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# ユーザフォルダの存在チェック
		if CLS_File.sExist( gVal.DEF_USERDATA_PATH )!=True :
			## フォルダがない
			wRes['Reason'] = "フォルダがありません: path=" + gVal.DEF_USERDATA_PATH
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# 画面クリア(=通常モード時)
		if gVal.FLG_Test_Mode==False :
			CLS_OSIF.sDispClr()
		
		#############################
		# ヘッダ表示
		wStr = "--------------------" + '\n'
		wStr = wStr + " 手動バックアップ" + '\n'
		wStr = wStr + "--------------------" + '\n'
		wStr = wStr + '\n'
		wStr = wStr + "手動バックアップを開始します......" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 処理開始
		wStr = "バックアップファイル退避中......" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 前回バックアップしていればファイルを退避する
		wFLG_Escape = False
		if CLS_File.sExist( gVal.DEF_STR_FILE['BackupMan_file'] )==True :
			wFLG_Escape = True
			## 退避コピー
			if CLS_File.sCopy( gVal.DEF_STR_FILE['BackupMan_file'], gVal.DEF_STR_FILE['BackupMan_befour_file'] )!=True :
				## 失敗
				wRes['Reason'] = "ファイルの退避コピーに失敗しました: path=" + gVal.DEF_STR_FILE['BackupMan_file']
				CLS_OSIF.sErr( wRes )
				return wRes
			
			## 前回バックアップ削除
			if CLS_File.sRemove( gVal.DEF_STR_FILE['BackupMan_file'] )!=True :
				## 失敗
				wRes['Reason'] = "前回バックアップの削除に失敗しました: path=" + gVal.DEF_STR_FILE['BackupMan_file']
				CLS_OSIF.sErr( wRes )
				return wRes
		
		#############################
		# アーカイブリストの取得
		wStr = "アーカイブ中......" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 作業フォルダ変更
		wSrcCurr = CLS_File.sGetCurrentPath()
		wArcPath = wSrcCurr + "/" + gVal.DEF_STR_FILE['BackupMan_file']
		CLS_File.sChgFolder( gVal.DEF_STR_FILE['ARKsave_path'] )
		
		#############################
		# アーカイブリストの作成
		wArcList = self.__get_ArcList()
		if len(wArcList)==0 :
			## 失敗
			wRes['Reason'] = "アーカイブリストの取得 list=0"
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# バックアップ(savedアーカイブ)
		if CLS_File.sFolderArcive( wArcPath, wArcList )!=True :
			## 失敗
			wRes['Reason'] = "アーカイブに失敗しました: path=" + gVal.DEF_STR_FILE['ARKsave_path'] + "/" + gVal.DEF_STR_FILE['ARKsave_folder']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# フォルダを戻す
		CLS_File.sChgFolder( wSrcCurr )
		
		#############################
		# 退避ファイルの削除
		if wFLG_Escape==True :
			if CLS_File.sRemove( gVal.DEF_STR_FILE['BackupMan_befour_file'] )!=True :
				## 失敗
				wRes['Reason'] = "退避ファイルの削除に失敗しました: path=" + gVal.DEF_STR_FILE['BackupMan_befour_file']
				CLS_OSIF.sErr( wRes )
				return wRes
		
		#############################
		# ARK最終更新日 取得
		# 手動バックアップ 最終更新日 取得
		self.GetARKdate()
		self.UpdateManualDate()
		
		#############################
		# 完了
		wStr = "バックアップが完了しました。"
		CLS_OSIF.sPrn( wStr )
		
		wRes['Result'] = True
		return wRes



#####################################################
# 定期バックアップ
#####################################################
	def CircleBackup(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_BackupMain"
		wRes['Func']  = "CircleBackup"
		
		#############################
		# ARKのローカルプロファイルの存在チェック
		if CLS_File.sExist( gVal.DEF_STR_FILE['ARKcheck_file'] )!=True :
			## ファイルがない
			wRes['Reason'] = "ARKのローカルプロファイルが確認できません: path=" + gVal.DEF_STR_FILE['ARKcheck_file']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# ユーザフォルダの存在チェック
		if CLS_File.sExist( gVal.DEF_USERDATA_PATH )!=True :
			## フォルダがない
			wRes['Reason'] = "フォルダがありません: path=" + gVal.DEF_USERDATA_PATH
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# 画面クリア(=通常モード時)
		if gVal.FLG_Test_Mode==False :
			CLS_OSIF.sDispClr()
		
		#############################
		# 定期処理実行
		while True :
			#############################
			# 定期バックアップ コンソール画面
			wResDisp = CLS_MyDisp.sViewDisp( "CircleConsole" )
			if wResDisp['Result']==False :
				wRes['Reason'] = "sViewDisp is failed: " + CLS_OSIF.sCatErr( wResDisp )
				CLS_OSIF.sErr( wRes )
				return wRes
			
			#############################
			# ウェイト
			CLS_OSIF.sPrn( "次の処理実行まで待機します。CTRL+Cで中止できます。" )
			
			if gVal.FLG_Test_Mode==False :
				wSecond = gVal.DEF_STR_TLNUM['circleBackupTime'] * 60
			else:
				###テストモード時
				wSecond = 10

			wResStop = CLS_OSIF.sPrnWAIT( wSecond )
			if wResStop==False :
				CLS_OSIF.sPrn( '\n' + '\n' + "定期処理を中止しました。" + '\n' )
				break	#ウェイト中止
			
			#############################
			# 定期バックアップ 実行
			wStr = '\n' + '\n' + '\n' + "定期処理を実行します！！！ 今はキャンセルできません！！！" + '\n'
			wStr = wStr + "処理完了までお待ちください。。。" + '\n'
			CLS_OSIF.sPrn( wStr )
			
			wResRun = self.__circleBackupRun()
			if wResRun['Result']==False :
				wRes['Reason'] = "self__circleBackupRun is failed: " + CLS_OSIF.sCatErr( wResRun )
				CLS_OSIF.sErr( wRes )
				return wRes
			
			#############################
			# 周回処理 再開待ち  ※結果を映して見せるためのウェイト
			CLS_OSIF.sPrn( '\n' + '\n' + "次の定期処理の準備をしています......" )
			CLS_OSIF.sSleep( 5 )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# 定期バックアップ 実行
#####################################################
	def __circleBackupRun(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_BackupMain"
		wRes['Func']  = "__circleBackupRun"
		
		#############################
		# ARK最終更新日 チェック
		wResCheck = self.CheckARKdate()
		if wResCheck['Result']!=True :
			wRes['Reason'] = "CheckARKdate is failed: " + CLS_OSIF.sCatErr( wResCheck )
			return wRes
		
		if wResCheck['Responce']==False :
			###更新されていないのでバックアップしない 正常終了
			CLS_OSIF.sPrn( "ARKデータは更新されていないため、この周回はバックアップしません。" )
			wRes['Result'] = True
			return wRes
		
		# ※ここからバックアップ処理実行
		#############################
		# バックアップ開始
		wStr = "アーカイブ中......" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 時間を取得
		wTD = CLS_OSIF.sGetTime()
		if wTD['Result']!=True :
			###時間取得失敗  時計壊れた？
			wRes['Reason'] = "PC時間の取得に失敗しました"
			return wRes
		### wTD['TimeDate']
		
		#############################
		# ファイル名の作成
		wSrcCurr = CLS_File.sGetCurrentPath()
		wTD = str(wTD['TimeDate'])
		wTD = wTD.split(" ")
		wCHR_Date = wTD[0].replace( "-", "" )
		wCHR_Time = wTD[1].replace( ":", "" )
		wCHR_File = "circle_" + wCHR_Date + "_" + wCHR_Time
		wArcPath = wSrcCurr + "/" + gVal.DEF_USERDATA_PATH + wCHR_File + ".zip"
		
		#############################
		# 作業フォルダ変更
		CLS_File.sChgFolder( gVal.DEF_STR_FILE['ARKsave_path'] )
		
		#############################
		# アーカイブリストの作成
		wArcList = self.__get_ArcList()
		if len(wArcList)==0 :
			## 失敗
			wRes['Reason'] = "アーカイブリストの取得 list=0"
			return wRes
		
		#############################
		# バックアップ(savedアーカイブ)
		if CLS_File.sFolderArcive( wArcPath, wArcList )!=True :
			## 失敗
			wRes['Reason'] = "アーカイブに失敗しました: path=" + gVal.DEF_STR_FILE['ARKsave_path'] + "/" + gVal.DEF_STR_FILE['ARKsave_folder']
			return wRes
		
		#############################
		# フォルダを戻す
		CLS_File.sChgFolder( wSrcCurr )
		
		#############################
		# 定期バックアップ一覧の再取得
		self.GetCircleBackupList()
		
		#############################
		# 古いファイルの削除
		wNum = len( self.ARR_CircleFileList )
		if gVal.DEF_STR_TLNUM['circleBackupNum']<wNum :
			wStr = "古いアーカイブの削除中......" + '\n'
			CLS_OSIF.sPrn( wStr )
			
			wCount = 0
			wKeylist = list( self.ARR_CircleFileList.keys() )
			for wIndex in wKeylist :
				wCount += 1
				if gVal.DEF_STR_TLNUM['circleBackupNum']>=wCount :
					continue
				
				### circleBackupNum 個数以降を処理する
				wFile = gVal.DEF_USERDATA_PATH + self.ARR_CircleFileList[wIndex]['File']
				if CLS_File.sRemove( wFile )!=True :
					wRes['Reason'] = "ファイルの削除に失敗しました: path=" + wFile
					return wRes
			
			### 再取得
			self.GetCircleBackupList()
		
		#############################
		# ARK最終更新日 取得
		# 手動バックアップ 最終更新日 取得
		self.GetARKdate()
		self.UpdateManualDate()
		
		#############################
		# 完了
		wStr = "バックアップが完了しました。"
		CLS_OSIF.sPrn( wStr )
		
		wRes['Result'] = True
		return wRes



#####################################################
# アーカイブリスト作成
#####################################################
	def __get_ArcList(self):
		wArcList = []
		
		### Saved以下のリスト
		wCurrList = CLS_File.sLs( gVal.DEF_STR_FILE['ARKsave_folder'] )
		if len(wCurrList)==0 :
			## 失敗
			return wArcList
		
		for wCurrFolder in wCurrList :
			### Config以下
			if wCurrFolder=="Config" :
				wCurrPath = gVal.DEF_STR_FILE['ARKsave_folder'] + wCurrFolder
				wArcList.append( wCurrPath )
				
				### サブフォルダ
				wSubList = CLS_File.sLs( gVal.DEF_STR_FILE['ARKsave_folder'] + wCurrFolder )
				for wFile in wSubList :
					wSubPath = gVal.DEF_STR_FILE['ARKsave_folder'] + wCurrFolder + "/" + wFile
					wArcList.append( wSubPath )
					
					### フォルダ内のファイル
					wInFiles = CLS_File.sFs( wSubPath + "/" )
					for wFile in wInFiles :
						wFilePath = wSubPath + "/" + wFile
						wArcList.append( wFilePath )
			
			### それ以外
			else:
				### フォルダ
				wCurrPath = gVal.DEF_STR_FILE['ARKsave_folder'] + wCurrFolder
				wArcList.append( wCurrPath )
				
				### フォルダ内のファイル
				wInFiles = CLS_File.sFs( wCurrPath + "/" )
				for wFile in wInFiles :
					wFilePath = wCurrPath + "/" + wFile
					wArcList.append( wFilePath )
		
		return wArcList



