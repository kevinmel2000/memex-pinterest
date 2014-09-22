package com.hyperiongray.mapred;

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

	public static void main(String[] args) throws Exception {

		File file = new File("/home/tomas/Work/work/Proyecto/memex/git/cc-warc-examples/src/com/hyperiongray/mapred/output");
		FileUtils.deleteQuietly(file);
		
		JobConf conf = new JobConf(AnagramJob.class);
		conf.setJobName("wordcount");

		conf.setOutputKeyClass(Text.class);
		conf.setOutputValueClass(IntWritable.class);

		conf.setMapperClass(WordCountMapper.class);
		conf.setReducerClass(WordCountReducer.class);

		conf.setInputFormat(TextInputFormat.class);
//		conf.setInputFormat(CombineFileInputFormat.class);
		conf.setOutputFormat(TextOutputFormat.class);

		FileInputFormat.setInputPaths(conf, new Path(args[0]));
		FileOutputFormat.setOutputPath(conf, new Path(args[1]));

		JobClient.runJob(conf);
	}

}
