#!/usr/bin/env python3
"""
CET-4 学习计划生成器
基于艾宾浩斯遗忘曲线制定复习计划
"""

import argparse
import os
from datetime import datetime, timedelta


def generate_ebbinghaus_schedule(start_date, total_words, daily_new=20):
    """
    基于艾宾浩斯遗忘曲线生成复习计划
    复习时间点：第1天、第2天、第4天、第7天、第15天
    """
    intervals = [1, 2, 4, 7, 15]  # 艾宾浩斯复习间隔
    schedule = []
    
    start = datetime.strptime(start_date, "%Y-%m-%d")
    days_needed = (total_words + daily_new - 1) // daily_new
    
    for day in range(days_needed):
        current_date = start + timedelta(days=day)
        
        # 新词范围
        new_start = day * daily_new + 1
        new_end = min((day + 1) * daily_new, total_words)
        
        # 确定当天复习内容
        review_tasks = []
        
        # 添加新词学习
        tasks = [f"学习新词 {new_start}-{new_end}"]
        
        # 检查需要复习的词组
        for interval in intervals:
            review_day = day - interval
            if review_day >= 0:
                review_start = review_day * daily_new + 1
                review_end = min((review_day + 1) * daily_new, total_words)
                tasks.append(f"复习第{review_day + 1}天 ({review_start}-{review_end})")
        
        schedule.append({
            "day": day + 1,
            "date": current_date.strftime("%Y-%m-%d (%a)"),
            "tasks": tasks,
            "new_count": new_end - new_start + 1,
            "review_count": len(tasks) - 1
        })
    
    return schedule


def generate_html_schedule(schedule, total_words, daily_new, start_date):
    """生成 HTML 格式的学习计划表"""
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CET-4 单词学习计划</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
            line-height: 1.6;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 30px;
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            border-radius: 12px;
        }}
        .header h1 {{ font-size: 32px; margin-bottom: 10px; }}
        .header p {{ opacity: 0.9; font-size: 16px; }}
        .stats {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        .stat-box {{
            background: rgba(255,255,255,0.2);
            padding: 15px 25px;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-number {{ font-size: 28px; font-weight: bold; }}
        .stat-label {{ font-size: 13px; opacity: 0.9; }}
        
        .schedule-container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        
        .day-card {{
            background: white;
            border-radius: 12px;
            margin-bottom: 15px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        
        .day-header {{
            background: #f8f9fa;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #eee;
        }}
        
        .day-number {{
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }}
        
        .day-date {{
            color: #666;
            font-size: 14px;
        }}
        
        .day-badges {{
            display: flex;
            gap: 8px;
        }}
        
        .badge {{
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }}
        
        .badge-new {{
            background: #e3f2fd;
            color: #1976d2;
        }}
        
        .badge-review {{
            background: #fff3e0;
            color: #f57c00;
        }}
        
        .day-tasks {{
            padding: 15px 20px;
        }}
        
        .task-item {{
            display: flex;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px dashed #f0f0f0;
        }}
        
        .task-item:last-child {{
            border-bottom: none;
        }}
        
        .task-check {{
            width: 20px;
            height: 20px;
            border: 2px solid #ddd;
            border-radius: 4px;
            margin-right: 12px;
            flex-shrink: 0;
        }}
        
        .task-text {{
            color: #444;
            font-size: 14px;
        }}
        
        .task-text.new {{
            color: #1976d2;
            font-weight: 500;
        }}
        
        .tips {{
            max-width: 900px;
            margin: 30px auto;
            padding: 20px;
            background: #fffbeb;
            border-left: 4px solid #f59e0b;
            border-radius: 8px;
        }}
        
        .tips h3 {{
            color: #b45309;
            margin-bottom: 10px;
            font-size: 16px;
        }}
        
        .tips ul {{
            margin-left: 20px;
            color: #78716c;
            font-size: 14px;
        }}
        
        .tips li {{
            margin-bottom: 6px;
        }}
        
        @media print {{
            body {{ background: white; padding: 10px; }}
            .day-card {{ break-inside: avoid; box-shadow: none; border: 1px solid #ddd; }}
            .tips {{ background: #fffbeb !important; -webkit-print-color-adjust: exact; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📅 CET-4 单词学习计划</h1>
        <p>基于艾宾浩斯遗忘曲线 | 科学高效记忆</p>
        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">{total_words}</div>
                <div class="stat-label">目标词汇</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{len(schedule)}</div>
                <div class="stat-label">学习天数</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{daily_new}</div>
                <div class="stat-label">每日新词</div>
            </div>
        </div>
    </div>
    
    <div class="schedule-container">
'''
    
    for day in schedule:
        tasks_html = ""
        for i, task in enumerate(day['tasks']):
            is_new = "新词" in task
            task_class = "new" if is_new else ""
            tasks_html += f'''
                <div class="task-item">
                    <div class="task-check"></div>
                    <div class="task-text {task_class}">{task}</div>
                </div>
            '''
        
        html += f'''
        <div class="day-card">
            <div class="day-header">
                <div>
                    <div class="day-number">Day {day['day']}</div>
                    <div class="day-date">{day['date']}</div>
                </div>
                <div class="day-badges">
                    <span class="badge badge-new">+{day['new_count']} 新词</span>
                    <span class="badge badge-review">{day['review_count']} 复习</span>
                </div>
            </div>
            <div class="day-tasks">
                {tasks_html}
            </div>
        </div>
'''
    
    html += '''
    </div>
    
    <div class="tips">
        <h3>💡 学习建议</h3>
        <ul>
            <li><strong>黄金时间：</strong>建议早晨或睡前学习，记忆效果更佳</li>
            <li><strong>复习原则：</strong>按照艾宾浩斯曲线，在第1、2、4、7、15天复习</li>
            <li><strong>记忆技巧：</strong>结合词根词缀、真题例句记忆，不要死记硬背</li>
            <li><strong>自测方法：</strong>用卡片遮挡中文，尝试回忆英文释义</li>
            <li><strong>坚持打卡：</strong>每天完成学习后勾选任务，保持学习节奏</li>
        </ul>
    </div>
</body>
</html>
'''
    
    return html


def generate_markdown_schedule(schedule, total_words, daily_new):
    """生成 Markdown 格式的学习计划"""
    
    md = f"""# 📅 CET-4 单词学习计划

## 计划概览

| 项目 | 数值 |
|------|------|
| 目标词汇 | {total_words} 词 |
| 学习天数 | {len(schedule)} 天 |
| 每日新词 | {daily_new} 词 |
| 复习间隔 | 1-2-4-7-15 天 |

## 每日任务安排

"""
    
    for day in schedule:
        md += f"""### Day {day['day']} - {day['date']}

**新增:** {day['new_count']} 词 | **复习:** {day['review_count']} 组

"""
        for task in day['tasks']:
            prefix = "🆕" if "新词" in task else "🔄"
            md += f"- [ ] {prefix} {task}\n"
        
        md += "\n"
    
    md += """## 学习建议

1. **黄金时间**：建议早晨或睡前学习，记忆效果更佳
2. **复习原则**：按照艾宾浩斯曲线，在第1、2、4、7、15天复习
3. **记忆技巧**：结合词根词缀、真题例句记忆
4. **自测方法**：用卡片遮挡中文，尝试回忆英文释义
"""
    
    return md


def main():
    parser = argparse.ArgumentParser(description='生成 CET-4 单词学习计划')
    parser.add_argument('-w', '--words', type=int, default=500, help='总词汇量')
    parser.add_argument('-d', '--daily', type=int, default=25, help='每日新词量')
    parser.add_argument('-s', '--start', default=datetime.now().strftime("%Y-%m-%d"), help='开始日期 (YYYY-MM-DD)')
    parser.add_argument('-o', '--output', default='study_plan.html', help='输出文件名')
    parser.add_argument('--md', action='store_true', help='同时生成 Markdown 版本')
    
    args = parser.parse_args()
    
    # 生成计划
    schedule = generate_ebbinghaus_schedule(args.start, args.words, args.daily)
    
    # 生成 HTML
    html = generate_html_schedule(schedule, args.words, args.daily, args.start)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"[OK] 已生成学习计划: {args.output}")
    print(f"     - 总词汇: {args.words}")
    print(f"     - 学习天数: {len(schedule)} 天")
    print(f"     - 每日新词: {args.daily}")
    print(f"     - 开始日期: {args.start}")
    
    # 可选生成 Markdown
    if args.md:
        md_output = args.output.replace('.html', '.md')
        md = generate_markdown_schedule(schedule, args.words, args.daily)
        with open(md_output, 'w', encoding='utf-8') as f:
            f.write(md)
        print(f"[OK] 已生成 Markdown 版本: {md_output}")


if __name__ == '__main__':
    main()
