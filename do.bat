@echo off
cd C:\project\free_area\24_analytics_csv
set /p URL=URL:
python3 do.py "%URL%"
rem python3 do.py "C:\project\free_area\24_analytics_csv\data\data-export_20201215.csv"
pause