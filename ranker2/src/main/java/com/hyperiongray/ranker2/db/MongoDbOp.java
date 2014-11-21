package com.hyperiongray.ranker2.db;

/**
 * Created by mark on 11/20/14.
 */
import com.mongodb.BasicDBObject;
import com.mongodb.BulkWriteOperation;
import com.mongodb.BulkWriteResult;
import com.mongodb.Cursor;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBCursor;
import com.mongodb.DBObject;
import com.mongodb.MongoClient;
import com.mongodb.ParallelScanOptions;

import java.util.List;
import java.util.Set;

import static java.util.concurrent.TimeUnit.SECONDS;

public class MongoDbOp {
    public static void main(String [] args) throws Exception {
        // test the connnection
        MongoDbOp instance = new MongoDbOp();
        instance.testConnection();
    }
    private void testConnection() throws java.net.UnknownHostException {

// To directly connect to a single MongoDB server (note that this will not auto-discover the primary even
// if it's a member of a replica set:
        MongoClient mongoClient = new MongoClient();
// or
//        MongoClient mongoClient = new MongoClient( "localhost" );
// or
//        MongoClient mongoClient = new MongoClient( "localhost" , 27017 );
// or, to connect to a replica set, with auto-discovery of the primary, supply a seed list of members
//        MongoClient mongoClient = new MongoClient(Arrays.asList(new ServerAddress("localhost", 27017),
//                new ServerAddress("localhost", 27018),
//                new ServerAddress("localhost", 27019)));

        DB db = mongoClient.getDB( "mydb" );
        System.out.println("Connection to MongoDB established");
    }
}
