package com.hyperiongray.s3wordcount;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.regex.Pattern;

import org.apache.commons.io.FileUtils;
import org.apache.hadoop.thirdparty.guava.common.collect.Maps;

public class WeightedKeyword {

	private static final String KEYWORDS = "/home/tomas/Work/work/Proyecto/memex/git/memex-hackathon-1/common-crawl/src/com/hyperiongray/s3wordcount/data/keywords/keywords";
	private static Map<String, Integer> definedWeightedWords;

	public static synchronized Map<String, Integer> getDefinedWeightedWords2() {
		if (definedWeightedWords == null) {
			definedWeightedWords = Maps.newHashMap();
			definedWeightedWords.put("alejandro", 1);
			definedWeightedWords.put("amanda", 1);
			definedWeightedWords.put("mikhail", 1);
			definedWeightedWords.put("tomas", 1);
			definedWeightedWords.put("king", 1);
			definedWeightedWords.put("the", 10);
			definedWeightedWords.put("twitter", 10);
			definedWeightedWords.put("blog", 10);
		}
		return definedWeightedWords;
	}

	public static Map<String, Integer> getDefinedWeightedWords()
			throws IOException {
		if (definedWeightedWords == null) {
			File file = new File(KEYWORDS);
			List<String> lines = FileUtils.readLines(file);
			definedWeightedWords = Maps.newHashMap();
			for (String line : lines) {
				String[] split = line.split(",");
				// definedWeightedWords.put(split[0].trim().replaceAll("+",
				// "\\+"), Integer.valueOf(split[1]));
				definedWeightedWords.put(split[0].trim(),
						Integer.valueOf(split[1]));
			}
		}
		return definedWeightedWords;
	}

	public static Map<String, Pattern> getKeywordPattern() throws IOException {
		Map<String, Pattern> keywordPattern = Maps.newHashMap();
		for (String keyword : getDefinedWeightedWords().keySet()) {
			String escapedKeyword = Pattern.quote(keyword);
			Pattern pattern = Pattern.compile("\\b" + escapedKeyword + "\\b",
					Pattern.CASE_INSENSITIVE);
			keywordPattern.put(keyword, pattern);
		}
		return keywordPattern;
	}

}