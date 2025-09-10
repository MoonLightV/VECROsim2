import os
import pandas as pd

# 文件夹路径和输出文件名
input_folder = './vecro2_2/cpu-hog'  # 替换为CSV文件所在的文件夹路径
output_file = './vecro2_2/cpu-hog-all.csv'

# 创建一个空的DataFrame来存储合并后的数据
merged_df = pd.DataFrame()

# 获取文件列表并按文件名排序
file_list = sorted([f for f in os.listdir(input_folder) if f.endswith('.csv')])

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
'''
target = [
    "social-unique-id",
    "social-url-shorten",
    "social-video",
    "social-image",
    "social-text",
    "social-user-tag",
    "social-compose-post"
]'''

'''
target = [
    "social-read-timeline",
    "social-read-post"         
]
'''

file_list = [ 'latency_avg.csv', 'latency_p95.csv', 'throughput.csv', 'cpu_usage.csv', 'cpu_system_usage.csv', 'cpu_user_usage.csv', 'memory_usage_bytes.csv', 'memory_working_set_bytes.csv', 'memory_rss_bytes.csv', 
            'memory_mapped_file_bytes.csv', 'memory_cache_bytes.csv', 'memory_failures_total.csv', 'network_receive_packets_total.csv', 'network_transmit_packets_total.csv',
            'network_receive_bytes_total.csv', 'network_transmit_bytes_total.csv', 'network_receive_errors_total.csv', 'network_transmit_errors_total.csv', 
            'network_receive_packets_dropped_total.csv', 'network_transmit_packets_dropped_total.csv', 'fs_io_current.csv', 'fs_io_seconds_total.csv', 'fs_read_seconds.csv',
            'fs_read_bytes.csv', 'fs_read_total.csv', 'fs_read_merged_total.csv', 'fs_write_seconds.csv', 'fs_write_bytes.csv', 'fs_write_total.csv', 
            'fs_write_merged_total.csv', 'fs_sector_reads_total.csv', 'fs_sector_writes_total.csv'
           ]
target_file = ['memory_usage_bytes.csv', 'memory_working_set_bytes.csv', 'memory_rss_bytes.csv', 
            'memory_mapped_file_bytes.csv', 'memory_cache_bytes.csv', 'memory_failures_total.csv', 'network_receive_bytes_total.csv', 'network_transmit_bytes_total.csv', 'fs_sector_writes_total.csv']

except_file = ['memory_mapped_file_bytes.csv', 'memory_cache_bytes.csv', 'network_receive_packets_dropped_total.csv', 'network_transmit_packets_dropped_total.csv', 'fs_io_current.csv',
               'network_receive_errors_total.csv', 'network_transmit_errors_total.csv', 'fs_read_merged_total.csv', 'fs_read_seconds.csv','fs_read_bytes.csv','fs_write_bytes.csv'
           ]

def convert_bytes(bytes_num, precision=5, unit_system='binary'):
    """
    将字节转换为更易读的单位（如 KB、MB、GB）
    
    :param bytes_num: 输入的字节数（整数或浮点数）
    :param precision: 保留小数位数（默认2）
    :param unit_system: 单位标准，可选 'binary'(二进制，基于1024) 或 'decimal'(十进制，基于1000)
    :return: 格式化后的字符串（如 "44.11 MB"）
    """
    units = {
        'binary': ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'],
        'decimal': ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    }
    
    base = 1024 if unit_system == 'binary' else 1000
    
    if bytes_num == 0:
        return f"0 {units[unit_system][0]}"
    
    unit_index = 0
    while abs(bytes_num) >= base and unit_index < len(units[unit_system]) - 1:
        bytes_num /= base
        unit_index += 1
    
    return f"{bytes_num:.{precision}f}"

# 按文件名顺序遍历CSV文件
for file_name in file_list:
    if file_name in except_file:
        continue
    file_path = os.path.join(input_folder, file_name)

    # 读取CSV文件
    df = pd.read_csv(file_path)
    if file_name in target_file:
        df_converted = df.applymap(lambda x: convert_bytes(x) if isinstance(x, (int, float)) else x)
        df = df_converted
    # 检查是否存在'social-compose-post'列
    for t in target:
        if t in df.columns:
        # 获取'social-compose-post'列并将其列名修改为文件名（去除扩展名）
            column_name = t + ':' +os.path.splitext(file_name)[0]
            merged_df[column_name] = df[t]
    #if 'social-compose-post' in df.columns:
        # 获取'social-compose-post'列并将其列名修改为文件名（去除扩展名）
     #   column_name = os.path.splitext(file_name)[0]
     #   merged_df[column_name] = df['social-compose-post']

# 将合并后的数据保存到一个新的CSV文件
merged_df.to_csv(output_file, index=False)

print(f"合并后的文件已保存到 {output_file}")
