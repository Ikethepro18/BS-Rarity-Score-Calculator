@echo off
cd "%~dp0"
pyinstaller --onefile --windowed --icon=icon.ico --add-data "icon.ico;." --add-data "items.txt;." --add-data "scores.txt;." rarity_calc.pyw
