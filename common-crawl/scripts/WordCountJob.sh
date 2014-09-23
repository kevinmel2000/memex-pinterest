#!/bin/bash
hadoop jar target/common-crawler-0.1-SNAPSHOT-jar-with-dependencies.jar  \
com.hyperiongray.s3wordcount.WordCountJob  data/input output data/keywords/keywords