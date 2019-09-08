# docker_mysql_jupyter

## 首次執行

1. 將資料從git hub 抓下來

``` bash=
cd ~
git clone https://github.com/edward79519/docker_mysql_jupyter/
cd docker_mysql_jupyter
```
2. 執行 docker-compose

``` bash=
docker-compose up -d
```

3. 開啟瀏覽器，進入網頁 http://yourip:8888/ 
4. 開啟 project 資料夾
5. "第一次" 請先開啟 "filetomtsql_alc.ipynb"，點選工具列 "Kernel" -> "Restart & Run all"
6. 開啟 "daily_kd_alc_v1.ipynb"，點選工具列 "Kernel" -> "Restart & Run all"

## Change Log
### v 1.0
1. container 起來後自動新增 database 以及 table。
2. plotly 輸出圖片套件 orca 執行成功。 
