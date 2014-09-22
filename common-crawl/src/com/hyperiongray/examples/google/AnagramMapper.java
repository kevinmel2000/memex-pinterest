package com.hyperiongray.examples.google;

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
import java.util.Arrays;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;

/**
 * The Anagram mapper class gets a word as a line from the HDFS input and sorts
 * the letters in the word and writes its back to the output collector as Key :
 * sorted word (letters in the word sorted) Value: the word itself as the value.
 * When the reducer runs then we can group anagrams togather based on the sorted
 * key.
 * 
 * @author subbu iyer
 * 
 */
public class AnagramMapper extends MapReduceBase implements Mapper<LongWritable, Text, Text, Text> {

	private Text sortedText = new Text();
	private Text orginalText = new Text();

	public void map(LongWritable key, Text value, OutputCollector<Text, Text> outputCollector, Reporter reporter) throws IOException {

		String word = value.toString();
		char[] wordChars = word.toCharArray();
		Arrays.sort(wordChars);
		String sortedWord = new String(wordChars);
		sortedText.set(sortedWord);
		orginalText.set(word);
		outputCollector.collect(sortedText, orginalText);
	}

}