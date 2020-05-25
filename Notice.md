# 1.pymysql使用报错
- 项目主目录下的__init__.py文件中如下编辑  
    `import pymysql`  
    `pymysql.install_as_MySQLdb()`
- ../Lib/site-packages/django/db/backends/mysql/base.py 中注释掉36-37行：  
    `if version < (1, 3, 13):`  
&emsp;  `raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)`
 