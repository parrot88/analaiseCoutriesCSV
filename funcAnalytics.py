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
    countryList = []        #国のリスト
    non_countryList = []    #csvになかった国のリスト
    csv_file_path = ""  #csvファイルパス:コマンドライン引数から取得
    csv_file_string = ""    #csvファイル文字列

    data_date = ""
    data_os = ""
    data_score_user = {}
    export_string = ""
    export_string_title = ""

    ## --------------------------------------------------------------------

    def __init__(self):
        self.getCSVpath()           #パラメータからCSVパスを取得。なければエラーで終了
        self.readCountryFile()      #国のCSVファイルを読む
        self.readDataCSVFile()      #データCSVファイルを読む
        self.analyzeDataCSV()       #CSVファイルから必要な情報を抜き出し
        self.checkData()            #CSV国のリストを参照しながら、出力文字列を生成。リストにない国は別途リストに保管する
        self.addCountryIntoCSV()    #CSV国のリストになかった国リストをCSV国CSVファイルに追記する
        self.exportData()           #結果CSVデータを出力する
        print("fin")

    #パラメータからCSVパスを取得。なければエラーで終了
    def getCSVpath(self):
        args = sys.argv
        if len(args) < 2:
            print(const.const.error_message_not_exist_csv)
            exit()
        #self.csv_file_path = args[1]
        self.csv_file_path = ""
        for i in range(1,len(args)):
            self.csv_file_path += args[i]
        print(self.csv_file_path)

    #国のCSVファイルを読む
    def readCountryFile(self):
        with open(const.const.country_csv_file, "r", encoding="utf-8_sig") as f:
            data = reader(f)
            for row in data:
                if len(row) > 0:
                    self.countryList.append(row[0])
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
        res = re.findall(const.const.pattern_csv_user_start, self.csv_file_string, re.DOTALL)
        res2 = res[0].replace(const.const.pattern_csv_user_delete,"")
        score_string = res2.replace("\n\n#","")
        #print(score_string)

        #改行で分けて、一つづつ国の集計をとっていく
        coutry_string_list = score_string.split("\n")
        for one_contry in coutry_string_list:
            coutry_scores = one_contry.split(",")
            #print(coutry_scores)
            #定着ユーザーも計算して、文字列に変換
            stay_user = int(coutry_scores[1]) - int(coutry_scores[2])
            #辞書に追加していく
            score_list = (coutry_scores[1],coutry_scores[2],str(stay_user))
            self.data_score_user[coutry_scores[0]] = score_list
        #print(self.data_score_user)

    #CSV国のリストを参照しながら、出力文字列を生成。リストにない国は別途リストに保管する
    def checkData(self):
        #CSV国のリスト順にデータ辞書から取り出し
        for c_name in self.countryList:
            #print(type(c_name))
            #print(c_name[0])

            self.export_string_title += c_name+",,,"
            if (c_name in self.data_score_user):
            #if (c_name[0] in self.data_score_user):
                self.export_string += self.data_score_user[c_name][0]+","+self.data_score_user[c_name][1]+","+self.data_score_user[c_name][2]+","   #本番国名なし、カンマつなぎ
                #self.export_string += c_name+","+self.data_score_user[c_name][0]+","+self.data_score_user[c_name][1]+","+self.data_score_user[c_name][2]+"\n"   #テスト版国名あり
            else:
                #辞書になかった国のリストを作成する
                self.export_string += "0,0,0,"
                #print("not exist country in data csv:"+c_name)

        #CSV国のリストになかった国の処理、リストになければ国、スコア追加。なかった国のリストに追加しておく
        for c_key in self.data_score_user:
            if c_key not in self.countryList:
                print("add new country "+c_key)
                self.export_string += self.data_score_user[c_key][0]+","+self.data_score_user[c_key][1]+","+self.data_score_user[c_key][2]+","   #本番、国名なし
                #self.export_string += c_key+","+self.data_score_user[c_key][0]+","+self.data_score_user[c_key][1]+","+self.data_score_user[c_key][2]+"\n"   #テスト版国名あり
                self.non_countryList.append(c_key)  #なかった国のリストに追加しておく
                self.export_string_title += c_key+",,,"

        #print(self.export_string_title)
        #print(self.export_string)
        #print(self.non_countryList)

    #CSV国のリストになかった国リストをCSV国CSVファイルに追記する
    def addCountryIntoCSV(self):
        if len(self.non_countryList) < 1:
            return
        addCountryTxt = "\n".join(self.non_countryList)
        addCountryTxt = addCountryTxt.strip()
        #addCountryTxt = "\n"+"\n".join(self.non_countryList)
        with open(const.const.country_csv_file, "a", encoding="utf-8_sig") as f:
            print(addCountryTxt.strip(), file=f)    #最後の改行１つを削除して追記

    #結果CSVデータを出力する
    def exportData(self):
        with open(const.const.export_csv_file+"_"+self.data_os+"_"+self.data_date+".csv", "w", encoding="utf-8_sig") as f:
            print(self.export_string_title+"\n"+self.export_string, file=f)
