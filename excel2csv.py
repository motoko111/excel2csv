import re
import sys
import os
import openpyxl

DELIMITER_STR = ","
LINE_STR = "\n"
INPUT_DIR = "input"
OUTPUT_DIR = "output"

class DataTable:
    '''
    1シート分のデータ構造情報
    '''
    def __init__(self, name):
        self.name = name
        self.fields = []
        self.records = []
        self.fieldNameRow = -1
        self.typeRow = -1
        self.infoRow = -1
        self.startRow = -1
        self.endRow = -1

    def add_field(self,field):
        '''
        フィールド情報追加
        '''
        self.fields.append(field)

    def add_record(self, record):
        '''
        レコード追加
        '''
        self.records.append(record)

    def find_record(self, field, value):
        for record in self.records:
            if record.get_value(field) == value:
               return record
        return None

class DataField:
    '''
    1列分のデータ構造情報
    '''
    def __init__(self):
        self.type = ''
        self.name = ''
        self.info = ''
        self.column = -1

class DataRecord:
    '''
    1行分のデータ
    '''
    def __init__(self):
        self.data = {}

    def set_value(self, field, value):
        self.data[field] = value

    def get_value(self, field):
        return self.data[field]
    
    def get_export_str(self, field):
        v = self.get_value(field)
        if v is None:
            return ""
        elif type(v) is str:
            return '"' + v + '"'
        return str(v)

def load_excel( filepath ):
    '''
    xls/xlsmを読み込む
    '''
    wb = openpyxl.load_workbook(filepath, keep_vba=True)
    return wb

def load_and_analys(filepath, sheetName) -> DataTable:
    '''
    指定シートをデータテーブル化
    '''
    wb = load_excel(filepath)
    ws = wb[sheetName]
    table = analys_sheet(ws)
    return table

def load_and_analys_all(filepath):
    '''
    '''
    wb = load_excel(filepath)
    tables = analys_sheet_all(wb)
    return tables

def analys_sheet_all(wb):
    '''
    各sheetを読み込む
    '''
    tables = []
    for sheetName in wb.sheetnames:
        ws = wb[sheetName]
        tables.append(analys_sheet(ws))
    return tables

def analys_sheet(ws) -> DataTable:
    '''
    1つのsheetを読み込む
    '''
    table = DataTable( ws.title )

    # 1列目を読み込み どの行になんの項目があるかを確認
    for iRow in range(1, ws.max_row + 1):
        cell = ws.cell(iRow, 1)
        #print(u"1行目解析:" + str(cell.value))
        if cell.value == "FieldName":
            table.fieldNameRow = iRow
        elif cell.value == "Type":
            table.typeRow = iRow
        elif cell.value == "Info":
            table.infoRow = iRow
        if table.fieldNameRow != -1 and table.typeRow != -1 and table.infoRow  != -1:
            table.startRow = iRow + 1
            table.endRow = ws.max_row
            break
    
    # 各項目を登録
    for iCol in range(2, ws.max_column + 1):
        cell = ws.cell(1, iCol)
        if cell.value == "#":
            continue
        field = DataField()
        field.column = iCol
        if table.fieldNameRow != -1:
            field.name = ws.cell(table.fieldNameRow, iCol).value
        if table.typeRow != -1:
            field.type = ws.cell(table.typeRow, iCol).value
        if table.infoRow != -1:
            field.info = ws.cell(table.infoRow, iCol).value
        if field.name == None:
            continue
        print(u"項目:" + str(field.name))
        table.add_field(field)

    print(u"データ範囲:" + str(table.startRow) + "～" + str(table.endRow))
    # 各レコードを登録
    for iRow in range(table.startRow, table.endRow + 1):
        if ws.cell(iRow, 1).value == "#":
            continue
        record = DataRecord()
        for field in table.fields:
            #print("" + str(ws.cell(iRow, field.column).value))
            value = ws.cell(iRow, field.column).value
            record.set_value(field.name, value)
        table.add_record(record)

    return table

def export_csv(table : DataTable):
    '''
    DataTableをcsvに出力
    '''
    txt = ""
    for i in range(len(table.fields)):
        field = table.fields[i]
        if ( i >= 1):
            txt += DELIMITER_STR
        txt += field.name
    txt += LINE_STR
    for record in table.records:
        for i in range(len(table.fields)):
            field = table.fields[i]
            if ( i >= 1):
                txt += DELIMITER_STR
            value_str = record.get_export_str(field.name)
            txt += value_str
            #print(u"レコード追加:" + str(field.name) + "," + str(field.type) + "," + value_str)
        txt += LINE_STR
    
    output_file = OUTPUT_DIR + "/" + table.name + ".csv"
    with open(output_file,'w',encoding='utf_8_sig', newline="") as f:
        f.write(txt)

def export_ue4_data_table(table : DataTable, setting : DataTable, path_setting : DataTable):
    '''
    DataTableをUE4のC++ファイルとして出力
    '''
    replace_field_map = {}
    for record in setting.records:
        type_str = record.get_value("Type")
        code_type_str = record.get_value("CodeTypeName_UE")
        replace_field_map[type_str] = code_type_str

    txt_fields = ""
    for i in range(len(table.fields)):
        field = table.fields[i]
        txt_fields += get_ue4_field_str(field, replace_field_map)
    
    replace_map = {
        "DATA_NAME":table.name,
        "FIELDS":txt_fields
    }

    ue_record = path_setting.find_record("Platform", "UE")
    output_dir = ue_record.get_value("CodeOutputPath")
    template_file = ue_record.get_value("TemplatePath")
    output_file = output_dir + "/" + table.name + "Manager" + ".h"
    export_from_template(template_file, output_file, replace_map)

def get_ue4_field_str(field : DataField, replace_field_map):
    '''
    Field1つ分のテキストを作成
    '''
    txt = ""
    txt += "	" + "UPROPERTY(EditAnywhere)" + LINE_STR
    if field.type in replace_field_map:
        txt += "	" + replace_field_map[field.type]
    else:
        txt += "	" + field.type
    txt += " " + field.name + ";"
    txt += LINE_STR
    return txt

def export_unity_data_table(table : DataTable):
    '''
    DataTableをUnityのC#ファイルとして出力
    '''
    # TODO:
    pass

def export_from_template(template_file, output_file, replaceMap):
    '''
    templateファイルをコピーして文字列置換したものを出力.
    '''
    txt = ""
    with open(template_file, 'r') as f:
        txt = f.read()

    for key in replaceMap:
        txt = re.sub('\\${' + key + '}', replaceMap[key], txt)
    
    with open(output_file,'w',encoding='UTF-8') as f:
        f.write(txt)

def get_input_files():
    '''
    input配下のファイルを全て取得
    '''
    files = os.listdir(INPUT_DIR)
    files_file = [f for f in files if os.path.isfile(os.path.join(INPUT_DIR, f))]
    return files_file

def main():
    print("=================" + "load setting" + " start" "=================")
    setting = load_and_analys("Setting.xlsx", "Setting")
    path_setting = load_and_analys("Setting.xlsx", "PathSetting")
    print("=================" + "load setting" + " end" "=================")

    files = get_input_files()
    for file_path in files:
        print("=================" + file_path + " start" "=================")
        tables = load_and_analys_all(file_path)
        for table in tables:
            export_csv(table)
            export_ue4_data_table(table, setting, path_setting)
        print("=================" + file_path + " end" "=================")

main()