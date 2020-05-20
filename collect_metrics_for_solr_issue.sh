#!/bin/sh
  
if [ $# -ne 3 ]; then
    echo "Usage: $0 interval count solr_core"
    exit 1
fi

INTERVAL=$1
COUNT=$2
CORE=$3


echo "Removing old output files..."
rm -f /tmp/$(hostname -i)-*.out

#Reset mBeans
nodetool sjk mx -b "com.datastax.bdp:type=search,index=$CORE,name=QueryMetrics" -mc -op resetLatencies --quiet

echo "Run nodetool sjk ttop..."
nohup nodetool sjk ttop > /tmp/$(hostname -i)-ttop.out &

echo "Run iostat ..."
nohup iostat -c -x -d -t 1 600 > /tmp/$(hostname -i)-iostat.out &


echo "Turn on DEBUG..."
nodetool setlogginglevel org.apache.solr.handler.component.QueryComponent DEBUG

echo "Collecting data every $INTERVAL seconds for $COUNT iterations..."
for i in $(seq $COUNT); do
    echo "\n" >> /tmp/$(hostname -i)-querymetrics.out
    date '+%Y-%m-%d %H:%M:%S' >> /tmp/$(hostname -i)-querymetrics.out
    nodetool sjk mxdump -q "com.datastax.bdp:type=metrics,scope=search,index=$CORE,metricType=QueryMetrics,*" >> /tmp/$(hostname -i)-querymetrics.out
    date '+%Y-%m-%d %H:%M:%S' >> /tmp/$(hostname -i)-filtercache.out
    nodetool sjk mxdump -q "solr/$CORE:type=dseFilterCache,id=com.datastax.bdp.search.solr.FilterCacheMBean" >> /tmp/$(hostname -i)-filtercache.out
    echo "Sleeping for $INTERVAL..."
sleep $INTERVAL
done

echo "Turn off DEBUG..."
nodetool setlogginglevel org.apache.solr.handler.component.QueryComponent INFO

echo "Kill nodetool sjk ttop ..."
kill -9 $(ps -ef | grep "org.apache.cassandra.tools.NodeTool -p 7199 sjk ttop" | grep -v "grep" | awk '{print $2}')

