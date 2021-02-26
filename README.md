# SQLTOCSV
数据库：sqlserver
pyodbc解决中文乱码问题
1、请创建sql文件夹
2、sql文件请放置在py脚本同级的sql文件夹中，sql文件夹中sql文件会批量执行，文件夹中请勿放置除sql以外的其他文件，否则会当成sql文件执行并出错
3、如果要使用时间范围搜索可以在脚本中引入between @rq1 and @rq2进行日期范围搜索,日期修改请在代码中直接修改@rq1 @rq2 的值
4、sql文件名即csv文件保存名字，要修改csv保存文件名请直接修改sql文件名字
