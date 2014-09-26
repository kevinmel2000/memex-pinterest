package com.hyperiongray;

import java.io.File;
import java.io.IOException;
import java.util.Map;

import org.apache.commons.io.FileUtils;
import org.junit.Before;
import org.junit.Test;

import com.hyperiongray.s3wordcount.ContentMatcher;
import com.hyperiongray.s3wordcount.CustomHttpConnector;
import com.hyperiongray.s3wordcount.WordCountOnlyMapper;

public class MatchContentTest {

//	private WordCountOnlyMapper instance = new WordCountOnlyMapper();
	private static final String path = "/home/tomas/Work/work/Proyecto/memex/git/memex-hackathon-1/common-crawl/data/keywords/keywords";
	private ContentMatcher instance ;

	private CustomHttpConnector httpConnector = new CustomHttpConnector();

	@Before
	public void before(){
		String keywordsFileContent;
		try {
			keywordsFileContent = FileUtils.readFileToString(new File(path), "UTF-8");
			instance = new ContentMatcher(keywordsFileContent);
		} catch (IOException e) {
			e.printStackTrace();
		}

	}
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
	@Test
	public void crawlingMatchContentTest() {
//		String url = "http://charlibella.rare-playmate.com/faq.php";
		String url = "http://charlibella.rare-playmate.com/faq-32431-bbbjtcim.php";
//		String url ="https://s3-us-west-2.amazonaws.com/darpa-memex/data/keywords/keywords.txt";
		
		String content = httpConnector.getContent(url);
		System.out.println(content);
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
