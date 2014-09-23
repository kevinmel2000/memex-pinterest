package com.hyperiongray.s3wordcount;

import java.io.IOException;
import java.util.Map;
import java.util.regex.Pattern;

import org.apache.hadoop.thirdparty.guava.common.collect.Maps;

public class WeightedKeyword {

	// private static final String KEYWORDS =
	// "/home/tomas/Work/work/Proyecto/memex/git/memex-hackathon-1/common-crawl/src/com/hyperiongray/s3wordcount/data/keywords/keywords";
	private static Map<String, Integer> definedWeightedWords = Maps.newHashMap();
	Map<String, Pattern> keywordPattern = Maps.newHashMap();

	// private String keywordsFilename="";

	public WeightedKeyword(String filecontent) {
		String[] lines = filecontent.split("\n");
		definedWeightedWords = Maps.newHashMap();
		for (String line : lines) {
			String[] split = line.split(",");
			definedWeightedWords.put(split[0].trim(), Integer.valueOf(split[1]));
		}
		for (String keyword : getDefinedWeightedWords().keySet()) {
			String escapedKeyword = Pattern.quote(keyword);
			Pattern pattern = Pattern.compile("\\b" + escapedKeyword + "\\b", Pattern.CASE_INSENSITIVE);
			keywordPattern.put(keyword, pattern);
		}

	}

	public Map<String, Integer> getDefinedWeightedWords() {
		// throws IOException {
		// if (definedWeightedWords == null) {
		// File file = new File(keywordsFilename);
		// List<String> lines = FileUtils.readLines(file);
		// definedWeightedWords = Maps.newHashMap();
		// for (String line : lines) {
		// String[] split = line.split(",");
		// definedWeightedWords.put(split[0].trim(),
		// Integer.valueOf(split[1]));
		// }
		// }
		return definedWeightedWords;
	}

	public Map<String, Pattern> getKeywordPattern() throws IOException {
//		if (keywordPattern == null) {
//			for (String keyword : getDefinedWeightedWords().keySet()) {
//				String escapedKeyword = Pattern.quote(keyword);
//				Pattern pattern = Pattern.compile("\\b" + escapedKeyword + "\\b", Pattern.CASE_INSENSITIVE);
//				keywordPattern.put(keyword, pattern);
//			}
//		}
		return keywordPattern;
	}

}
