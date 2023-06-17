# msPyExcelSQL
Implementation of pyodbc module of mkleehammer to treat excel file as database

God created Man. Man created Excel.

!!! TO USE THIS MODULE MAKE SURE THAT YOU HAVE: EXCEL ODBC DRIVER, PYODBC MODULE. ODBC-bits have to match PYTHON-bits. x32 ODBC will never work with x64 python and vice versa.

Purpose of this module is to provide instrument for python to treat excel (.xlsx, .xlsb, .xlsm, .xls) as normal database:
    1. Direct manipulations with excel file. Insert, update and ofc select. Delete is not supported because excel file have static amount of rows and driver cant remove them.
    2. Create objects from DB entities (models) to manipulate DB via OOP-style.

For example, you have class Band and sheet "bands" in excel file. So this module let you create instances of Band from "bands" records or create new instance, setup it and save to "bands". Ofc this class can be inherit and get own behavior or tuf bussiness logic.

For better understanding check tests/Main

For quick stack use command
python -m msPyExcelSQL.deploy FILE_NAME_HERE (default just deployed.py)

# FAQ
Q: To use excel file as a database? It's a joke! I have MySQL, Postgre, MongoDB or SQLite3. Why do I need this crutches?<br>
A: Excel spreadsheet is a most common data transfer "joke" in companies worldwide. Most of bussiness stuff going on excel spreadsheets, especially analyses and reports.
Does your SQLite have spreadsheet features?

Q: What about performance?
A: On ryzen7 4800h and nvme ssd author got 1280 records (4 values: int, string, datetime and random float) inserted each second. If do same with open excelfile, unf, its drops to 20 records each second. Searching of random id (int) among 1_048_576 records took about 0.01~0.02s

Q: Why just dont use pandas.read_excel()?<br>
A: I tried it but on heavy files like 60MB pandas will read them around 5-6 minutes and in debug mode this time is trippled. So odbc driver is only way.

Q: I dont have ms odbc driver where can I get it?<br>
A: Download Microsoft Access Database Engine 2016 Redistributable from MS site

Q: I have odbc driver for x32(x86) but my python is x64 or vice versa. What should I do?<br>
A: Download and /quite setup of x64 Microsoft Access Database Engine 2016 Redistributable

Q: Can x32(x86) driver works with x64 python?<br>
A: No, newer its gonna happend. If you cant setup x64 driver you have to download x32 python or use x32 python venv. Sad, but true.

Q: My corporation is using x32 MS office, so driver is x32 and my python is x64. I cant change my software. What should I do?<br>
A: Learn Java with JDBC. Joke. If you cant ask your IT devision to setup software nothing you can do with this.

Q: I need pandas dataframe features to solve my task. Can I query data from excelfile and convert records to normal dataframe?<br>
A: Yes, you can. Use pandas.from_records(list[tuple,tuple], columns=[str,str]).
!!! pandas is not included to this module to keep dependency only on PYODBC

Q: Is there any requirements and conditions for excel sheet data structure?<br>
A: Yes, your excel sheet with data must looks like regular database table:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0. Sheetname cant have whitespace. So bands, albums, total_costs are okey and "my favorite bands" not.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. First column is header.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. No merged cells.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. All columns with data must be titled.<br>

Q: Should I create python class for each excel sheet? I have few sheets for some calcs and plots with charts.<br>
A: No, you dont need. Just create class for sheet that you need.

Q: Should I create ExcelColumn object for each column on sheet?<br>
A: Yes. If you have 10 columns with data you have 10 ExcelColumn instances.

Q: If my programm is running I cant open and edit excel file. It says: "excel file is locked for editing by another user" Whats going on?<br>
A: Its ODBC connection. If you want to edit your file in runtime, you need to open it first and then run programm. So you can see in real time how new rows appears and old rows updates, charts are updates and so on.

Q: I asked ExcelSheet to delete one row, then I asked ExcelSheet insert new data but its appears under deleted row. So I have empty row in my database, why its happend?<br>
A: Excel has 1.048.576 rows. Always. Excel ODBC driver cant delete row all, it can is just UPDATE it to NULL. Driver limits...

Q: CAN I USE FORMULAS ON EXCEL SHEET DATABASE, LIKE VLOOKUP OR IF?<br>
A: Yes, but keep in mind that DRIVER CANT UPDATING CELLS WHAT CONTAINS FORMULA. While selecting driver will returns only value of cell or NULL if cell is #N/A, not fomula like =VLOOKUP(). Inserting will insert only values, so if you need formula, better insert NULL and after data inserted, stretch formula.

Q: CAN PIVOT TABLE BE A DATABASE?<br>
A: YES, THANKS TO GOD! But... pivot header must be in first row and pivot must repeat row labels.

Q: Can another excel file be source for my excel database?<br>
A: Yes, it can. Also you can keep pivot tables with unchecked "Save source data with file" from different files. Its really gamechanger, when you have 3 files with size about 60MB each and one excel "joke" database file with three sheets with pivot tables, so 3*60MB turns into ~240kb which you can query and send to web interface.
Pivot table really can group up and agregate data so you dont even need pandas features.

Q: If pyodbc is lying in base of this module can I dinamicly switch datasource from excel file to, eg, MySQL?<br>
A: No, part of this module is to solve Excel dialect problem: like convert bandsSheet to [bands$] and take in [] column title if its has a whitespaces.

Q: Does this module let me parse website directly to excelfile?<br>
A: Well, yes, you need to:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. Create structure of awaited data in excel file (sheet and columns)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. Extend ExcelModelSheet and set ExcelColumns<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. Extend ExcelModel and put parsed data in constructor, then call .save() and it will insert new row in excelfile.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4. In parser login setup creating instances of ExcelModel each time when data has been successfully parsed.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4.1 If you need do some logic on parsed data, you can code up behaviour inside ExcelModel sibling. Eg, you have price and awaible stocks in shop but you want to calc total and also convert price to your local currency. There you can behold power of OOP. After your ExcelModel got requered data and instance has been created, you may ask your ExcelModel to calc_total() or convert_to_currency(). So your ExcelModel is not dumb datastructure anymore, it has own behaviour and purpose to use.
