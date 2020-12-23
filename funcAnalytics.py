# coding: utf-8
"""
仕様：
AnalyticsのCSVを解析して国別の全ユーザー、定着、新ユーザーを出力、コピペ
"""
import const
from csv import reader
import sys
import re

class Functions:
    ## --------------------------------------------------------------------
    countryList = []    #国のリスト
    csv_file_path = ""  #csvファイルパス:コマンドライン引数から取得
    csv_file_string = ""    #csvファイル文字列

    data_date = ""
    data_os = ""
    data_score_user = {}
    export_string = ""

    ## --------------------------------------------------------------------

    def __init__(self):
        self.getCSVpath()           #パラメータからCSVパスを取得。なければエラーで終了
        self.readCountryFile()      #国のCSVファイルを読む
        self.readDataCSVFile()      #データCSVファイルを読む
        self.analyzeDataCSV()       #CSVファイルから必要な情報を抜き出し
        self.checkData()            #CSV国のリストを参照しながら、出力文字列を生成。リストにない国は別途リストに保管する
        self.addCountryIntoCSV()    #CSV国のリストになかった国リストをCSV国CSVファイルに追記する
        print("hello")
        pass

    #パラメータからCSVパスを取得。なければエラーで終了
    def getCSVpath(self):
        args = sys.argv
        if len(args) < 2:
            print(const.const.error_message_not_exist_csv)
            exit()
        #print(len(args))
        self.csv_file_path = args[1]
        print(self.csv_file_path)

    #国のCSVファイルを読む
    def readCountryFile(self):
        with open(const.const.country_csv_file, "r", encoding="utf-8_sig") as f:
            data = reader(f)
            for row in data:
                self.countryList.append(row)
                #print(row)
                pass
            pass
        print(self.countryList)

    #データCSVファイルを読む
    def readDataCSVFile(self):
        with open(self.csv_file_path, "r", encoding="utf-8_sig") as f:
            self.csv_file_string = f.read()
        #print(self.csv_file_string)

    #CSVファイルから必要な情報を抜き出し
    def analyzeDataCSV(self):
        self.getOS()            #「プラットフォーム」に含まれる要素 Android,iOS抽出
        self.getPlatform()      #開始日: 20201215,抽出
        self.getScore()         #「国,ユーザー,新しいユーザー」以下で国別集計抽出

    #「プラットフォーム」に含まれる要素 Android,iOS抽出
    def getOS(self):
        res = re.findall(const.const.pattern_csv_os, self.csv_file_string)
        self.data_os = res[0].replace(const.const.pattern_csv_os_delete,"")
        self.data_os = self.data_os.replace("\n","")
        print(self.data_os)

    #開始日抽出
    def getPlatform(self):
        res = re.findall(const.const.pattern_csv_date, self.csv_file_string)
        res2 = re.findall("[0-9]+",res[0])
        self.data_date = res2[0]
        print(self.data_date)

    #「国,ユーザー,新しいユーザー」文字列以下で国別集計抽出,定着ユーザーも計算し保管しておく
    def getScore(self):
        #対象文字列を抜き出し
        res = re.findall(const.const.pattern_csv_user_start, self.csv_file_string)
        res2 = res[0].replace(const.const.pattern_csv_user_delete,"")
        score_string = res2.replace("\n\n#","")
        #print(score_string)

        #改行で分けて、一つづつ国の集計をとっていく
        coutry_string_list = score_string.split("\n")
        for one_contry in coutry_string_list:
            coutry_scores = one_contry.split(",")
            print(coutry_scores)
            #定着ユーザーも計算して、文字列に変換
            stay_user = int(coutry_scores[1]) - int(coutry_scores[2])
            #辞書に追加していく
            score_list = (coutry_scores[1],coutry_scores[2],str(stay_user))
            self.data_score_user[coutry_scores[0]] = score_list
        #print(self.data_score_user)

    #CSV国のリストを参照しながら、出力文字列を生成。リストにない国は別途リストに保管する
    def checkData(self):
        for c_name in self.countryList:
            #print(type(c_name))
            #print(c_name[0])
            if (c_name[0] in self.data_score_user):
                self.export_string += c_name[0]+","+self.data_score_user[c_name[0]][0]+","+self.data_score_user[c_name[0]][1]+","+self.data_score_user[c_name[0]][2]+"\n"   #テスト版国名あり
                #self.export_string += self.data_score_user[c_name[0]][0]+","+self.data_score_user[c_name[0]][1]+","+self.data_score_user[c_name[0]][2]+"\n"   #本番国名なし
            else:
                #辞書になかった国のリストを作成する
                self.export_string += "0,0,0\n"
                print("come ")
                pass
            #CSV国のリストになかった国の処理
            
            pass
        print(self.export_string)
        pass

    #CSV国のリストになかった国リストをCSV国CSVファイルに追記する
    def addCountryIntoCSV(self):
        pass

