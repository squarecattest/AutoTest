# AutoTest
自動測試測資，輸出為一個紀錄檔和一個個別資料輸出的資料夾。

目前可測試AC/WA/TLE/RE。MLE不會被偵測。由於使用python實作，測試時間會稍大於實際時間。
## 參數
`file`: 用於測試的執行檔位置，默認為`.\a.exe`。

`sin`(sample input): 測資檔案資料夾位置，默認為`.\sin\`。

`sout`(sample output)：測資解答資料夾位置，默認為`.\sout\`。若資料夾不存在，將會丟出一個`Warning`。

`outs`：測試輸出資料夾位置，默認為`.\outputs\`。

`log`：測試結果文字檔位置，默認為`.\log.txt`。

`timeout`：以毫秒為單位的超時時間，默認為`2000 ms`。

## 指令
`$ py .\auto-test.py`
`$ python .\auto-test.py`

以下所有參數皆可選。

- `-f <檔案位置>`：設定`file`
- `-sin <資料夾位置>`：設定`sin`
- `-sout <資料夾位置>`：設定`sout`
- `-o <資料夾位置>`：設定`outs`
- `-l <檔案位置>`：設定`log`
- `-t <整數>`：設定`timeout`，單位為毫秒
