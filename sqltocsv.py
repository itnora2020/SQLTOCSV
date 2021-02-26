'''
auther:zyj
time:20210224
1、sql文件请放在sql文件夹中，sql文件夹与py脚本放在同一级目录下
2、csv导出至csv文件夹中
'''
import csv
import time
import os
import pyodbc


def getlocalpath(file, newpath=0, isdeletefile=0):
    current_path = os.path.abspath(file)
    # 获取当前文件的父目录
    father_path = os.path.abspath(
        os.path.dirname(current_path) + os.path.sep + ".")
    localpath = father_path
    if newpath != 0:
        localpath = father_path+'\\'+newpath+'\\'
    if not os.path.exists(localpath):  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(localpath)
    # 删除文件夹中文件
    if isdeletefile != 0:
        del_list = os.listdir(localpath)
        for f in del_list:
            file_path = os.path.join(localpath, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
    return localpath


# 或者给定路径文件夹中所有文件路径
def listdir(path, file_list_name):  # 传入存储的list
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, file_list_name)
        else:
            file_list_name.append(file_path)


# 获取文件名
def getsqlfilename(filepath):
    return filepath.split('\\')[-1]


sqlfile_list_name = []
sqlpath = getlocalpath(__file__)+'\\sql\\'
if not os.path.exists(sqlpath):
    print("sql目录不存在，请新建sql目录并将sql文件拷贝到脚本所在同级的sql目录下，脚本未正常执行！")
    exit()
listdir(sqlpath, sqlfile_list_name)

sqlserver_ip = '127.0.0.1'
username = 'sa'
password = '123456'
db = 'test'
try:
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+sqlserver_ip +
                          ';DATABASE='+db+';UID=' + username + ';PWD=' + password)
except pyodbc.Error:
    print("数据库连接失败，请检查数据库连接配置!")
    exit()
if not conn:
    print("数据库连接失败，请检查数据库连接配置!")
    exit()
else:
    print(sqlserver_ip+":数据库连接正常!")
    print("准备开始执行sql脚本...")
cur = conn.cursor()  # 定义一个游标用来执行DDL,DML,SELECT语句
# 定义一个list变量用来保存表头
for i in sqlfile_list_name:
    header = []
    sqlfilename = getsqlfilename(i)
    sql = open(i, 'r')
    sqltxt = sql.readlines()
    # 此时 sqltxt 为 list 类型
    # 读取之后关闭文件
    sql.close()
    # list 转 str
    
    #统计日期请修改@rq1 @rq2
    timesql = "DECLARE @rq1 DATETIME;\nDECLARE @rq2 DATETIME;\nSET @rq1 = '2020-11-01';\nSET @rq2 = '2020-12-01';\n"
    print("\n是否添加下面时间查询条件到sql中脚本中\n"+timesql)
    selectdate = input("是否启用时间范围搜索 (y/n) ?")
    if selectdate == 'y' or selectdate == 'Y':
        sql = timesql+"".join(sqltxt)
    else:
        sql = "".join(sqltxt)
    try:
        cur.execute(sql)
    except pyodbc.Error:
        print(sqlfilename+" 脚本执行错误，请检查sql脚本！")
        exit()
    for col_len in range(0, len(cur.description)):  # 循环遍历
        header.append(cur.description[col_len][0])  # 将表头添加到变量header
    cur.execute(sql)  # 执行SELECT
    print('开始导出:', sqlfilename, time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime()))
    csvpath = getlocalpath(__file__, 'csv')
    csvfilename = sqlfilename[:-4]+'.csv'
    # csvfile.txt改成csvfile.csv表示导出为excel 如果不加newline='' 每导出一行就有空的行
    with open(csvpath+csvfilename, 'w', newline='', encoding="utf-8")as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)  # 用来写表头
        writer.writeheader()  # 用来写表头
        # delimiter默认是’,‘ 如果delimiter=' ' 表示导出为tsv
        file = csv.writer(csvfile, delimiter=',')
        while True:
            rows = cur.fetchmany()  # 每次获取cur.arraysize行数据
            file.writerows(list(rows))
            # print(rows)
            if not rows:
                break  # 中断循环
    print('导出完成:', sqlfilename, time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime()))
cur.close()
conn.close()  # 关闭连接
print("sql脚本执行完毕，共导出%d张表！" % len(sqlfile_list_name))
