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
import java.util.Date;
import java.util.Map;
import java.util.Map.Entry;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.JobConf;
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

public class WordCountOnlyMapper extends MapReduceBase implements Mapper<Object, Text, NullWritable, Text> {

	private static final int LOWER_SCORE_THRESHOLD = 5;

	private static final Pattern pattern = Pattern.compile("<title>(.+?)</title>", Pattern.CASE_INSENSITIVE);
	private OutputParser outputParser = new OutputParser();
	private WeightedKeyword weightedKeyword;
	
	public void configure(JobConf job) {
		 String keywordsfileContent = job.get("keywordsFileContent");
		 weightedKeyword = new WeightedKeyword(keywordsfileContent);
	}

	public void map(Object key, Text value, OutputCollector<NullWritable, Text> outputCollector, Reporter reporter) throws IOException {

		// We're accessing a publicly available bucket so don't need to fill in
		// our credentials
		ArchiveReader ar;
		try {
			S3Service s3s = new RestS3Service(null);

			// Let's grab a file out of the CommonCrawl S3 bucket
			String fn = value.toString();
			System.out.println(fn);

			S3Object f = s3s.getObject("aws-publicdatasets", fn, null, null, null, null, null, null);

			// The file name identifies the ArchiveReader and indicates if it
			// should be decompressed
			ar = WARCReaderFactory.get(fn, f.getDataInputStream(), true);

		} catch (S3ServiceException e) {
			e.printStackTrace();
			throw new RuntimeException(e);
		}

		// Once we have an ArchiveReader, we can work through each of the
		// records it contains
		int i = 0;
		System.out.println("Started" + new Date());
		for (ArchiveRecord r : ar) {

			try {
				// The header file contains information such as the type of
				// record, size, creation time, and URL
				String url = r.getHeader().getUrl();
				String crawledDate = r.getHeader().getDate();
				if (url == null)
					continue;

				// If we want to read the contents of the record, we can use the
				// ArchiveRecord as an InputStream
				// Create a byte array that is as long as all the record's
				// stated length
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
				// Note: potential optimization would be to have a large buffer
				// only allocated once

				// Why don't we convert it to a string and print the start of
				// it?
				String content = new String(os.toString());

				Map<String, Integer> matches = this.matchContent(content);
				int score = score(matches);

				if (score > LOWER_SCORE_THRESHOLD) {
					System.out.println("****************************************");
					System.out.println("URL: " + url + " Score: " + score + " Detail: " + matches);
					// outputCollector.collect(new IntWritable(score), new Text(url));
					outputCollector.collect(NullWritable.get(),
							new Text(outputParser.parse(this.getTitle(content), url, crawledDate, score, matches)));
				}
				System.out.println(i);
				if (i++ > 1000000) {
					System.out.println("Finished " + new Date());
					break;
				}

			} catch (Exception e) {
				System.out.println(e);
			}
		}

	}

	public Map<String, Integer> matchContent(String content) throws IOException {
		Map<String, Integer> matches = Maps.newHashMap();
		if (!content.isEmpty() && content.length() > 50) {
			for (Entry<String, Pattern> entry : weightedKeyword.getKeywordPattern().entrySet()) {
				Matcher matcher = entry.getValue().matcher(content);
				if (matcher.find())
					matches.put(entry.getKey(), 1);
			}
		}
		return matches;
	}

	// public for testing purposes
	public int score(Map<String, Integer> matches) throws IOException {
		int score = 1;
		for (Entry<String, Integer> entry : matches.entrySet()) {
			score *= weightedKeyword.getDefinedWeightedWords().get(entry.getKey()) * entry.getValue();
		}
		return score;
	}

	public String getTitle(String content) {
		Matcher matcher = pattern.matcher(content);
		String result;
		if (matcher.find()) {
			result = matcher.group(1);
		} else {
			result = "";
		}
		return result;
	}

}