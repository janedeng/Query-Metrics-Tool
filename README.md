# Query-Metrics-Tool
This is a tool to analyze the Solr QueryMetrics data we collect.

Requirements

Install python xlsxwriter:

pip install --user XlsxWriter

Instructions

    Run script collect_metrics_for_solr_issue.sh to collect a set of data. It resets the latency from QueryMetrics, runs ttop (sort by CPU),collects iostat for 10 minutes, turns on DEBUG against QueryComponent, then collects QueryMetrics, FilterCache metrics. At the end, it turns off DEBUG, and kills the nodetool sjk ttop process.

Note: the collect_metrics_for_solr_issue_pre51.sh is for earlier 5.1 releases that might not have the SJK bundled in nodetool

Command:

./collect_metrics_for_solr_issue.sh interval count solr_core

    After collecting the querymetrics data from the collection script, retrieve the data by PHASE and attribute. For example, Count under COORDINATOR phase.

Command:

python draw_solr_request_chart.py <output.xlsx> [RETRIEVE|COORDINATE|EXECUTE] <Attribute of the phase, for example, Count or 99thPercentile> <file path1> <file path2> ...

The tool will create a xlsx file, retrieve the data and draw the chart to visualize it.
