import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import io
from pywebio.output import put_image, put_html, put_file

def plot_data_with_datetime(start_date, end_date, data, xlabel, ylabel, title):
    # 生成日期范围
    date_range = [start_date + timedelta(hours=x) for x in range(int((end_date-start_date).total_seconds()/3600))]

    # 创建图表并绘制数据
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(date_range, data, marker='o')  # 使用圆点标记每个数据点
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # 设置X轴刻度为日期和时间格式，并避免重叠
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))  # 设置刻度间隔为6小时

    # 旋转X轴刻度，使其垂直显示，避免重叠
    plt.xticks(rotation=-30)

    # 调整底部空间
    plt.subplots_adjust(bottom=0.2)

    # 保存为SVG文件，并返回SVG文本
    svg_buffer = io.StringIO()
    plt.savefig(svg_buffer, format='svg', bbox_inches='tight')
    svg_text = svg_buffer.getvalue()
    svg_buffer.close()
    return svg_text
if __name__ == "__main__":
    # 示例数据和调用示例
    start_date = datetime(2024, 1, 1, 0, 0, 0)
    end_date = datetime(2024, 1, 3, 0, 0, 0)
    date_range = [start_date + timedelta(hours=x) for x in range(int((end_date-start_date).total_seconds()/3600))]
    data = np.sin(np.arange(len(date_range)))  # 示例数据，可以替换为您的实际数据

    svg_text = plot_data_with_datetime(start_date, end_date, data, 'Date and Time', 'Value', 'Data with Date and Time on X-axis')
    put_html(svg_text)
    put_file("图片.svg", svg_text)