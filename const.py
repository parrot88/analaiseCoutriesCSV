## coding: UTF-8

class const:

    country_csv_file = "countries.csv"
    dat_csv_file = "data/dat.csv"
    error_message_not_exist_csv = "google csvファイルがありません"
    export_csv_file = "./result"

    pattern_csv_os = "# 「プラットフォーム」に含まれる要素 [^\n]+\n"
    pattern_csv_os_delete = "# 「プラットフォーム」に含まれる要素 "

    pattern_csv_date = "# 開始日: [0-9]+\n"
    #pattern_csv_date_delete = "# 開始日: "

    pattern_csv_user_start = "国,ユーザー,新しいユーザー\n[^#]+#"
    pattern_csv_user_delete = "国,ユーザー,新しいユーザー\n"
