# このアプリについて
SUポータルにアクセスし、授業スケジュールのicsファイルを作成するCLIアプリです。  

# インストール方法
Releasesから最新版のwhlファイルをダウンロードし、
```
pip install *.whl
```
でインストールしてください。  
また、別途Google Chromeが必要です。  

# 使用方法
今年履修している授業スケジュールのicsファイルを作成するには
```
saidai-ical-generator -a -u USERID -p PASS -b out.ics
```
ただし、USERIDとPASSはSUポータルのログインIDとパスワードです。  
