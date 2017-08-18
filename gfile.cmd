@IF EXIST "%~dp0\≈¿≥Ê≈‰÷√\%1" (
	@echo "∏¥÷∆Œƒº˛"
) ELSE (
	@mkdir  ".\≈¿≥Ê≈‰÷√\%1" 
	@echo "≥…π¶¥¥Ω®%1Œƒº˛º–")
@copy .\≈¿≥Ê≈‰÷√\default\default.json  .\≈¿≥Ê≈‰÷√\%1\%1.json
@copy .\≈¿≥Ê≈‰÷√\default\default.xlsx  .\≈¿≥Ê≈‰÷√\%1\%1.xlsx
@copy .\≈¿≥Ê≈‰÷√\default\default.txt  .\≈¿≥Ê≈‰÷√\%1\%1.txt
@copy .\≈¿≥Ê≈‰÷√\default\default.xml  .\≈¿≥Ê≈‰÷√\%1\%1.xml
@python project.py %1
pause
