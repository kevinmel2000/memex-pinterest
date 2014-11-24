package com.hyperiongray.ranker2;

/**
 * Created by mark on 11/19/14.
 */
import com.hyperiongray.ranker2.db.MongoDbOp;
import com.hyperiongray.ranker2.index.Indexer;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Options;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Ranker {
    private static final Logger logger = LoggerFactory.getLogger(Ranker.class);
    private static Options options;

    public static void main(String args[]) {
        formOptions();
        if (args.length == 0) {
            HelpFormatter formatter = new HelpFormatter();
            formatter.printHelp("Ranker - rank crawled pages in MongoDB for display, using Lucene search ranking", options);
            return;
        }
        // TODO parse and use options
        Ranker main = new Ranker();
        try {
            main.createIndex(args);
            main.readAndApplyIndex();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void formOptions() {
        options = new Options();
        options.addOption("k", "keywords", true, "Keywords file");
    }

    private void createIndex(String args[]) throws Exception {
        MongoDbOp.main(args);
    }
    private void readAndApplyIndex() throws Exception {
        Indexer indexer = new Indexer();
        indexer.setIndexLocation("output/index");
        indexer.readIndex();
    }
}
