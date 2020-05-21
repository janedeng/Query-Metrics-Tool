## Query metrics tool

This is a tool to analyze the Solr QueryMetrics data we collect. 

**Requirements**

Install python `xlsxwriter`: 

```
pip install --user XlsxWriter
```

**Instructions**

1. Run script collect_metrics_for_solr_issue.sh to collect a set of data. It resets the latency from QueryMetrics, runs ttop (sort by CPU),collects iostat for 10 minutes, turns on DEBUG against QueryComponent, then collects QueryMetrics, FilterCache metrics. At the end, it turns off DEBUG, and kills the nodetool sjk ttop process.

Command:

```
./collect_metrics_for_solr_issue.sh interval count solr_core
```
  
2. After collecting the querymetrics data from the collection script, retrieve the data by PHASE and attribute. For example, Count under COORDINATOR phase. If using "rate" mode, the graph is drawed by the rate of the data change. Otherwise, it's raw data.

Command:

```
python draw_solr_request_chart.py <xlsx output file> [RETRIEVE|COORDINATE|EXECUTE] <Attribute of the phase, for example, Count or 99thPercentile> [rate|false] <file path1> <file path2> ...
```  

The tool will create a xlsx file, retrieve the data and draw the chart to visualize it. 

Example:

$ python ~/myscripts/Query-Metrics-Tool/draw_solr_request_chart.py test2.xlsx COORDINATE Count false 10.1.1.28-querymetrics.out 10.1.1.29-querymetrics.out 


