package com.hyperiongray.s3wordcount;

import java.io.File;

import org.apache.commons.io.FileUtils;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.FileInputFormat;
import org.apache.hadoop.mapred.FileOutputFormat;
import org.apache.hadoop.mapred.JobClient;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.TextInputFormat;
import org.apache.hadoop.mapred.TextOutputFormat;

import com.hyperiongray.examples.google.AnagramJob;

public class WordCountJob {

	private static final String OUTPUT_DIR = "/home/tomas/Work/work/Proyecto/memex/git/memex-hackathon-1/common-crawl/src/com/hyperiongray/s3wordcount/data/output";

	public static void main(String[] args) throws Exception {

		File file = new File(OUTPUT_DIR);
		FileUtils.deleteQuietly(file);
		
		JobConf conf = new JobConf();
		conf.setJobName("s3wordcount");

		conf.setMapperClass(WordCountOnlyMapper.class);
		conf.setNumMapTasks(10);

//		conf.setReducerClass(WordCountReducer.class);
//		conf.setNumReduceTasks(1);

		conf.setInputFormat(TextInputFormat.class);
		conf.setOutputFormat(TextOutputFormat.class);
		
		conf.setOutputKeyClass(Text.class);
		conf.setOutputValueClass(IntWritable.class);

		FileInputFormat.setInputPaths(conf, new Path(args[0]));
		FileOutputFormat.setOutputPath(conf, new Path(args[1]));

		JobClient.runJob(conf);
	}

}
