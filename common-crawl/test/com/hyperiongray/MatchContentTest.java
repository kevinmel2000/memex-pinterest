package com.hyperiongray;

import java.io.IOException;
import java.util.Map;

import org.junit.Test;

import com.hyperiongray.s3wordcount.WordCountOnlyMapper;

public class MatchContentTest {

	private WordCountOnlyMapper instance = new WordCountOnlyMapper();

	@Test
	public void matchContentTest() {
		String content = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaagfeaaa bbbj gfe++aaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
				+ "bbbaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb";
		try {
			Map<String, Integer> matches = instance.matchContent(content);
			System.out.println(matches);
			int score = instance.score(matches);
			System.out.println(score);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
