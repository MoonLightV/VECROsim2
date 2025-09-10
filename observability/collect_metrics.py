from prometheus_api_client import PrometheusConnect
from prometheus_api_client.utils import parse_datetime
import string
import csv
import pandas as pd

prometheus_host_url = "http://192.168.49.2:30445"
start_time = parse_datetime("2025-09-09 07:10:00")
end_time = parse_datetime("2025-09-09 08:05:00")
step = "1s"
filepath = "vecro2_2/cpu-hog"

prom = PrometheusConnect(url=prometheus_host_url, disable_ssl=True)

target = [
    "social-follow-user",
    "social-recommender",
    "social-unique-id",
    "social-url-shorten",
    "social-video",
    "social-image",
    "social-text",
    "social-user-tag",
    "social-favorite",
    "social-search",
    "social-ads",
    "social-read-post",
    "social-login",
    "social-compose-post",
    "social-blocked-users",
    "social-read-timeline",
    "social-user-info",
    "social-posts-storage",
    "social-write-timeline",
    "social-write-graph",
    "social-read-timeline-db",
    "social-user-info-db",
    "social-posts-storage-db",
    "social-write-timeline-db",
    "social-write-graph-db"
]

# now 10s
metrics = {
    "latency_avg": 'rate(vecro_base_social_latency_counter{service="$SVC_NAME$"}[15s]) / rate(vecro_base_social_request_count{service="$SVC_NAME$"}[15s])',
    "latency_p95": 'histogram_quantile(0.95, rate(vecro_base_social_latency_histogram_bucket{service="$SVC_NAME$"}[1m]))',
    "throughput": 'rate(vecro_base_social_throughput{service="$SVC_NAME$"}[10s])',
    "cpu_usage": 'sum by (pod) (rate(container_cpu_usage_seconds_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]) * 100)',
    "cpu_system_usage": 'sum by (pod) (rate(container_cpu_system_seconds_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]) * 100)',
    "cpu_user_usage": 'sum by (pod) (rate(container_cpu_user_seconds_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]) * 100)',
    "memory_usage_bytes": 'sum by (pod) (container_memory_usage_bytes{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"})',
    "memory_working_set_bytes": 'sum by (pod) (container_memory_working_set_bytes{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"})',
    "memory_rss_bytes": 'sum by (pod) (container_memory_rss{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"})',
    "memory_mapped_file_bytes": 'sum by (pod) (container_memory_mapped_file{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"})',
    "memory_cache_bytes": 'sum by (pod) (container_memory_cache{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"})',
    "memory_failures_total": 'sum by (pod) (increase(container_memory_failures_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]))',
    "network_receive_packets_total": 'sum by (pod) (rate(container_network_receive_packets_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]))',
    "network_transmit_packets_total": 'sum by (pod) (rate(container_network_transmit_packets_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]))',
    "network_receive_bytes_total": 'sum by (pod) (rate(container_network_receive_bytes_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]))',
    "network_transmit_bytes_total": 'sum by (pod) (rate(container_network_transmit_bytes_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]))',
    "network_receive_errors_total": 'sum by (pod) (rate(container_network_receive_errors_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]))',
    "network_transmit_errors_total": 'sum by (pod) (rate(container_network_transmit_errors_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]))',
    "network_receive_packets_dropped_total": 'sum by (pod) (rate(container_network_receive_packets_dropped_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]))',
    "network_transmit_packets_dropped_total": 'sum by (pod) (rate(container_network_transmit_packets_dropped_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]))',
    "fs_io_current": 'sum by (pod) (container_fs_io_current{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"})',
    "fs_io_seconds_total": 'sum by (pod) (rate(container_fs_io_time_seconds_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]))',
    "fs_read_seconds": 'sum by (pod) (rate(container_fs_read_seconds_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]))',
    "fs_read_bytes": 'sum by (pod) (rate(container_fs_reads_bytes_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]))',
    "fs_read_total": 'sum by (pod) (rate(container_fs_reads_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]))',
    "fs_read_merged_total": 'sum by (pod) (rate(container_fs_reads_merged_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]))',
    "fs_write_seconds": 'sum by (pod) (rate(container_fs_write_seconds_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]))',
    "fs_write_bytes": 'sum by (pod) (rate(container_fs_writes_bytes_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]))',
    "fs_write_total": 'sum by (pod) (rate(container_fs_writes_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]))',
    "fs_write_merged_total": 'sum by (pod) (rate(container_fs_writes_merged_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]))',
    "fs_sector_reads_total": 'sum by (pod) (rate(container_fs_sector_reads_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]))',
    "fs_sector_writes_total": 'sum by (pod) (rate(container_fs_sector_writes_total{name=~".+", namespace="social", job="kubelet", pod=~"$SVC_NAME$-[a-z0-9]*-[a-z0-9]*"}[1m]))'
}



def target_to_metrics_name(target, m):
    service_name = target
    container_name = target[7:]
    if target.endswith("-db"):
        if m in ["latency_avg", "latency_p95", "throughput"]:
            container_name = f"{container_name}-agent"
        else:
            container_name = f"{container_name}-mongodb"
    query = metrics[m].replace("$SVC_NAME$", target)#.replace("$CONTAINER_NAME$", container_name)
    print(f"{target}, {m}: {query}")
    return query


for m in metrics.keys():
    rows = {}
    for t in target:
        # query metrics
        #if t not in ["social-compose-post"]:
        #    continue
        query_result_list = prom.custom_query_range(
            target_to_metrics_name(t, m),  # this is the metric name and label config
            start_time=start_time,
            end_time=end_time,
            step=step
        )
        if len(query_result_list) < 1:
            continue
        # get metrics values
        metrics_list = query_result_list[0]['values']

        # extract metrics
        row = [m[1] for m in metrics_list]
        series = pd.Series(row)
        rows[t] = series

    # write out csv
    df = pd.DataFrame(rows)
    df.to_csv(f"{filepath}/{m}.csv")
    print(f"saved {filepath}/{m}.csv")
