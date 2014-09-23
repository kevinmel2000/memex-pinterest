package com.hyperiongray.s3wordcount;

/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
//package com.hadoop.examples.anagrams;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.util.Map;
import java.util.Map.Entry;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;
import org.apache.hadoop.thirdparty.guava.common.collect.Maps;
import org.archive.io.ArchiveReader;
import org.archive.io.ArchiveRecord;
import org.archive.io.warc.WARCReaderFactory;
import org.jets3t.service.S3Service;
import org.jets3t.service.S3ServiceException;
import org.jets3t.service.impl.rest.httpclient.RestS3Service;
import org.jets3t.service.model.S3Object;

public class WordCountMapper extends MapReduceBase implements Mapper<Object, Text, Text, IntWritable> {


	private static final int LOWER_SCORE_THRESHOLD = 5;

	public void map(Object key, Text value, OutputCollector<Text, IntWritable> outputCollector, Reporter reporter) throws IOException {

		// We're accessing a publicly available bucket so don't need to fill in our credentials
		S3Service s3s;
		try {
			s3s = new RestS3Service(null);

			// Let's grab a file out of the CommonCrawl S3 bucket
			//			String fn = "common-crawl/crawl-data/CC-MAIN-2013-48/segments/1386163035819/warc/CC-MAIN-20131204131715-00000-ip-10-33-133-15.ec2.internal.warc.gz";
			String fn = value.toString();
			System.out.println(fn);

			S3Object f = s3s.getObject("aws-publicdatasets", fn, null, null, null, null, null, null);

			// The file name identifies the ArchiveReader and indicates if it should be decompressed
			ArchiveReader ar = WARCReaderFactory.get(fn, f.getDataInputStream(), true);

			// Once we have an ArchiveReader, we can work through each of the records it contains
			int i = 0;
			for (ArchiveRecord r : ar) {
				// The header file contains information such as the type of record, size, creation time, and URL
				//				System.out.println("Header: " + r.getHeader());
				String url = r.getHeader().getUrl();
				if (url == null)
					continue;

				// If we want to read the contents of the record, we can use the ArchiveRecord as an InputStream
				// Create a byte array that is as long as all the record's stated length

				OutputStream os = new ByteArrayOutputStream();
				try {
					r.dump(os);
				} finally {
					try {
						if (r != null)
							r.close();
					} catch (Exception e) {
						System.out.println(e);
					}
				}

				//Note: potential optimization would be to have a large buffer only allocated once

				// Why don't we convert it to a string and print the start of it?
				// Let's hope it's text!
				String content = new String(os.toString());
				//				System.out.println(content);

				// Pretty printing to make the output more readable
//				System.out.println("=-=-=-=-=-=-=-=-=");

				Map<String, Integer> matchedContents = this.matchContent(content);
				int score = score(matchedContents);
//				System.out.print(".");

				if(score> LOWER_SCORE_THRESHOLD){
//					System.out.print("");
					System.out.println("URL: " + url + " Score: " + score +" Detail: " + matchedContents);
					System.out.println("****************************************");
					outputCollector.collect(new Text(url), new IntWritable(score));
				}
				//				Map<Text,Text> map = Maps.newHashMap();
				//				map.put(new Text("score"), new Text(String.valueOf(score)));
				//				outputCollector.collect(new Text(url), map);

				if (i++ > 10000)
					break;
			}
		} catch (S3ServiceException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	/*
	//public for testing purposes
	public Map<String, Integer> matchContent(String content) throws IOException {
		Map<String, Integer> matches = Maps.newHashMap();
		for (String keyword : WeightedKeyword.getDefinedWeightedWords().keySet()) {
//			 String escapedKeyword = java.util.regex.Matcher.quoteReplacement(keyword);
			String escapedKeyword = Pattern.quote(keyword);
			
			Pattern pattern = Pattern.compile("\\b" + escapedKeyword +"\\b", Pattern.CASE_INSENSITIVE);
			Matcher matcher = pattern.matcher(content);
//			int counter = 0;
//			while (matcher.find()) {
//				counter++;
//			}
//			if (counter > 0)
//				matches.put(keyword, counter);
			if (matcher.find())
				matches.put(keyword, 1);
		}
		return matches;
	}
	*/
	public Map<String, Integer> matchContent(String content) throws IOException {
		Map<String, Integer> matches = Maps.newHashMap();
		if(!content.isEmpty() && content.length()>50){
			for (Entry<String,Pattern> entry: WeightedKeyword.getKeywordPattern().entrySet()) {
				Matcher matcher = entry.getValue().matcher(content);
				if (matcher.find())
					matches.put(entry.getKey(), 1);
			}
			
		}
		return matches;
	}

	//public for testing purposes
	public int score(Map<String, Integer> matches) throws IOException {
		int score = 1;
		for (Entry<String, Integer> entry : matches.entrySet()) {
			score *= WeightedKeyword.getDefinedWeightedWords().get(entry.getKey()) * entry.getValue();
		}
		return score;
	}
}