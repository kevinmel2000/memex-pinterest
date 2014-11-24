package com.hyperiongray.ranker2.index;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.search.*;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;
import org.apache.lucene.queryparser.classic.QueryParser;

import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.List;


import org.apache.lucene.document.Document;

/**
 * Created by mark on 11/23/14.
 * TODO update to newer Lucene API
 */
public class Indexer {
    private String indexLocation;
    private List<String> keyPhrases;

    private static StandardAnalyzer analyzer = new StandardAnalyzer(Version.LUCENE_40);

    private IndexWriter writer;

    public void openIndexForWrite() throws IOException {
        FSDirectory dir = FSDirectory.open(new File(indexLocation));
        IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_40, analyzer);
        writer = new IndexWriter(dir, config);
    }

    public void addTextToIndex(String text) throws IOException {
        Document doc = new Document();
        doc.add(new TextField("contents", text, Field.Store.YES));
        writer.addDocument(doc);
    }

    public void closeIndex() throws IOException {
        writer.commit();
        writer.close();
    }

    public String getIndexLocation() {
        return indexLocation;
    }

    public void setIndexLocation(String indexLocation) {
        this.indexLocation = indexLocation;
    }

    public void readIndex() throws Exception {
        for (String query : keyPhrases) {
            IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(indexLocation)));
            IndexSearcher searcher = new IndexSearcher(reader);
            // TODO think through the max
            int MAX_DOC = 1000;
            TopScoreDocCollector collector = TopScoreDocCollector.create(MAX_DOC, true);
            Query q = new QueryParser(Version.LUCENE_40, "contents", analyzer).parse(query);
            searcher.search(q, collector);
            TopDocs topDocs = searcher.search(q, Math.max(1, collector.getTotalHits()));
            ScoreDoc[] hits = collector.topDocs().scoreDocs;
        }
    }

    public List<String> getKeyPhrases() {
        return keyPhrases;
    }

    public void setKeyPhrases(List<String> keyPhrases) {
        this.keyPhrases = keyPhrases;
    }
}
