DATE=`date +%Y-%m-%d-%H-%M-%S`
echo "Dumping database..."
cp -r memex-pinterest memex-pinterest-staging
echo "Removing .git before taring"
rm -rf memex-pinterest-staging/.git
mongodump -d MemexHack -o memex-pinterest-db-$DATE
echo "Tarring your stuff up"
tar -zcvf memex-pinterest-${DATE}.tar.gz memex-pinterest-db-$DATE memex-pinterest-staging
rm -rf memex-pinterest-staging
