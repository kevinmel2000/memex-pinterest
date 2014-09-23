package com.hyperiongray;

import java.io.IOException;
import java.util.Map;

import org.junit.Test;

import com.hyperiongray.s3wordcount.WordCountMapper;

public class MatchContentTest {

	private WordCountMapper instance = new WordCountMapper();

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
