package com.hyperiongray.ranker2;

/**
 * Created by mark on 11/19/14.
 */
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Options;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static Options options;

    public static void main(String args[]) {
        formOptions();
        if (args.length == 0) {
            HelpFormatter formatter = new HelpFormatter();
            formatter.printHelp("XdbMeta - prepare vendor data for Xdb import", options);
            return;
        }
    }

    private static void formOptions() {
        options = new Options();
        options.addOption("k", "keywords", true, "Keywords file");
    }

}
