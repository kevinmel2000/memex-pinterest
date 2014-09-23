package com.hyperiongray.s3wordcount;

import java.io.File;
import java.net.URI;

import org.apache.commons.io.FileUtils;
import org.apache.hadoop.filecache.DistributedCache;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.FileInputFormat;
import org.apache.hadoop.mapred.FileOutputFormat;
import org.apache.hadoop.mapred.JobClient;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.TextInputFormat;
import org.apache.hadoop.mapred.TextOutputFormat;

public class WordCountJob {

	/*
	 * inputs:
	 * 0) the input file
	 * 1) the output folder
	 * 2) the keywords file
	 */
	public static void main(String[] args) throws Exception {

		
		
		File file = new File(args[1]);
		FileUtils.deleteQuietly(file);
		
		JobConf conf = new JobConf();
		conf.setJobName("s3wordcount");

		conf.setMapperClass(WordCountOnlyMapper.class);
		conf.setNumMapTasks(1);

//		conf.setReducerClass(WordCountReducer.class);
//		conf.setNumReduceTasks(1);

		conf.setInputFormat(TextInputFormat.class);
		conf.setOutputFormat(TextOutputFormat.class);
		
		conf.setOutputKeyClass(NullWritable.class);
		conf.setOutputValueClass(Text.class);

		FileInputFormat.setInputPaths(conf, new Path(args[0]));
		FileOutputFormat.setOutputPath(conf, new Path(args[1]));

		String keywordsFileContent = FileUtils.readFileToString(new File(args[2]), "UTF-8");
		conf.set("keywordsFileContent", keywordsFileContent);
		
//		URI uri = new URI(args[2]);
//		DistributedCache.addCacheFile(uri, conf);
		
//		WeightedKeyword weightedKeyword = new WeightedKeyword(fileContent);
//		conf.set("weightKeywords", weightedKeyword.getDefinedWeightedWords());
		
		
		JobClient.runJob(conf);
	}

}
