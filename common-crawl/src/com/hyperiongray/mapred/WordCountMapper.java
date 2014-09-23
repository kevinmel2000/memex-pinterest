package com.hyperiongray.mapred;

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

import java.io.IOException;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;
import org.apache.hadoop.thirdparty.guava.common.collect.Maps;

public class WordCountMapper extends MapReduceBase implements Mapper<Object, Text, Text, IntWritable> {

//	private Text word = new Text();
	private Map<String, Integer> definedWeightedWords;

	public Map<String, Integer> getDefinedWeightedWords() {
		if (definedWeightedWords == null) {
			definedWeightedWords = Maps.newHashMap();
			definedWeightedWords.put("alejandro", 1);
			definedWeightedWords.put("amanda", 2);
			definedWeightedWords.put("mikhail", 3);
			definedWeightedWords.put("tomas", 4);
		}
		return definedWeightedWords;
	}

	public void map(Object key, Text value, OutputCollector<Text, IntWritable> outputCollector, Reporter reporter) throws IOException {

		System.out.println("mapping:" + value);
		for (String keyword : getDefinedWeightedWords().keySet()) {
			Pattern pattern = Pattern.compile(keyword, Pattern.CASE_INSENSITIVE);
			Matcher matcher = pattern.matcher(value.toString());
			int counter = 0;
			while (matcher.find()) {
				counter++;
			}
			if(counter>0)
				outputCollector.collect(new Text(keyword), new IntWritable((Integer)(this.getDefinedWeightedWords().get(keyword))*counter));
		}
	}

	public void map2(Object key, Text value, OutputCollector<Text, IntWritable> outputCollector, Reporter reporter) throws IOException {

		System.out.println("mapping:" + value);
		for (String keyword : getDefinedWeightedWords().keySet()) {
			Pattern pattern = Pattern.compile(keyword, Pattern.CASE_INSENSITIVE);
			Matcher matcher = pattern.matcher(value.toString());
			int counter = 0;
			while (matcher.find()) {
				counter++;
			}
			if(counter>0)
				outputCollector.collect(new Text(keyword), new IntWritable((Integer)(this.getDefinedWeightedWords().get(keyword))*counter));
		}
	}

}