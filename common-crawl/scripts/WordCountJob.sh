#!/bin/bash
hadoop jar target/common-crawler-0.1-SNAPSHOT-jar-with-dependencies.jar  \
com.hyperiongray.s3wordcount.WordCountJob  data/input output data/keywords/keywords 100

#com.hyperiongray.s3wordcount.WordCountJob s3n://darpa-memex/data/input/ s3n://darpa-memex/output s3n://darpa-memex/data/keywords/keywords.txt 1000000000


#hadoop jar target/common-crawler-0.1-SNAPSHOT-jar-with-dependencies.jar  \
#com.hyperiongray.s3wordcount.WordCountJob s3n://darpa-memex/data/input/ s3n://darpa-memex/output https://s3-us-west-2.amazonaws.com/darpa-#memex/data/keywords/keywords.txt 10



#s3://darpa-memex/jar/common-crawler-0.1-SNAPSHOT-jar-with-dependencies.jar

#com.hyperiongray.s3wordcount.WordCountJob s3://darpa-memex/data/input/ s3://darpa-memex/output https://s3-us-west-2.amazonaws.com/darpa-memex/data/keywords/keywords.txt 1000000000

#https://s3-us-west-2.amazonaws.com/darpa-memex/data/keywords/keywords.txt

