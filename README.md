# Transition01
スパコンMPIプログラム

このプログラムは、MPIでの計算プログラムです。

inputデータ（2014_09_uniq.csv）、outputデータ（durationデータ）は容量が大きいため、今回は省略しています。

●inputデータ（2014_09_uniq.csv）  
以下のgithubリンク内のcsv/test_uniq.csvと同じ形式です。  
https://github.com/smzn/Wifilogcsv01


●outputデータ  
・durationデータ(duration0.csv~duration23.csv)  
以下の形式で出力されます。
,clientid,duration,from,from_time,to,to_time  
0,b980646bf62c58c2e6d71fe781ddecc013f37b68,-1.0,1123,2014-09-01 00:00:00,590,2014-09-01 00:00:00  
1,b980646bf62c58c2e6d71fe781ddecc013f37b68,36967.0,590,2014-09-01 00:00:00,612,2014-09-01 10:16:07  
2,b980646bf62c58c2e6d71fe781ddecc013f37b68,7001.0,612,2014-09-01 10:16:07,590,2014-09-01 12:12:48  
3,b980646bf62c58c2e6d71fe781ddecc013f37b68,185.0,590,2014-09-01 12:12:48,612,2014-09-01 12:15:53  
4,b980646bf62c58c2e6d71fe781ddecc013f37b68,27.0,612,2014-09-01 12:15:53,596,2014-09-01 12:16:20  
5,b980646bf62c58c2e6d71fe781ddecc013f37b68,63.0,596,2014-09-01 12:16:20,612,2014-09-01 12:17:23  

・transitionデータ(transition0.csv~transition23.csv)
　アップロード済み
