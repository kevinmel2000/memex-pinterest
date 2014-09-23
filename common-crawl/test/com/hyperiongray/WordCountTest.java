package com.hyperiongray;

import java.io.IOException;
import java.util.Map;

import org.junit.Test;

import com.hyperiongray.s3wordcount.WordCountMapper;

public class WordCountTest {

	private WordCountMapper instance = new WordCountMapper();
	private HttpConnector httpConnector = new HttpConnector();

	@Test
	public void matchContentTest() {

//		String url = "http://clclt.com/klepto/archives/2012/03/05/fashion-review-mode-noir-march-2";
//		String url = "http://ourhome2.net/vb/showthread.php?20399-Sweet-gfe-from-the-girl-next-door-MSOG-BBBJTCNQNS-LOW-SUMMER-RATES-NEWBIE-and-Biker-FRIENDLY";
//		String url = "http://comicbookdb.com/issue_storyarc.php?ID=87483";
//		String url = "http://cdm16694.contentdm.oclc.org/cdm/compoundobject/collection/YBM001/id/1084/rec/43";

/*		
		broward.org	{http://broward.org/Arts/Media/Pages/EventDescriptions.aspx=60}
			cdm16694.contentdm.oclc.org	{http://cdm16694.contentdm.oclc.org/cdm/compoundobject/collection/YBM001/id/1084/rec/43=400}
			community.babycenter.com	{http://community.babycenter.com/post/a41723461/fertility_after_cardiac_arrest_poss_trigger_pics_pg_2=25}
			dealnews.com	{http://dealnews.com/c196/Home-Garden/=60}
			docs.oracle.com	{http://docs.oracle.com/cd/E18283_01/appdev.112/e16760/toc.htm=125}
*/
		String url = "http://nymag.com/daily/intelligencer/2013/04/barry-diller-newsweek-was-a-mistake.html";
//		String url = "http://charlibella.rare-playmate.com/faq-32431-bbbjtcim.php";
			
		String content = httpConnector.getContent(url);
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
