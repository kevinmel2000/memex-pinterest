package com.hyperiongray.s3wordcount;

import java.util.Map;
import java.util.regex.Pattern;

import org.apache.hadoop.thirdparty.guava.common.collect.Maps;

public class WeightedKeyword {

	private static Map<String, Integer> definedWeightedWords = Maps.newHashMap();
	Map<String, Pattern> keywordPattern = Maps.newHashMap();

	public WeightedKeyword(String filecontent) {
		String[] lines = filecontent.split("\n");
		definedWeightedWords = Maps.newHashMap();
		for (String line : lines) {
			String[] split = line.split(",");
			definedWeightedWords.put(split[0].trim(), Integer.valueOf(split[1]));
			Pattern pattern = Pattern.compile("\\b" + Pattern.quote(split[0]) + "\\b", Pattern.CASE_INSENSITIVE);
			keywordPattern.put(split[0], pattern);
		}
//		for (String keyword : getDefinedWeightedWords().keySet()) {
//			String escapedKeyword = Pattern.quote(keyword);
//			Pattern pattern = Pattern.compile("\\b" + escapedKeyword + "\\b", Pattern.CASE_INSENSITIVE);
//			keywordPattern.put(keyword, pattern);
//		}

	}

	public Map<String, Integer> getDefinedWeightedWords(){
		return definedWeightedWords;
	}

	public Map<String, Pattern> getKeywordPattern(){
		return keywordPattern;
	}
}
