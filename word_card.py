#!/usr/bin/env python3
"""
CET-4 单词卡片生成器
生成美观的 HTML 单词卡片，支持打印
"""

import argparse
import re
import os
from datetime import datetime

# 默认词汇数据（部分高频词）
DEFAULT_WORDS = [
    # 超高频词汇 (1-50)
    {"word": "available", "phonetic": "/əˈveɪləbl/", "pos": "adj.", "meaning": "可获得的；有空的", "example": "Tickets are available online.", "freq": "high"},
    {"word": "benefit", "phonetic": "/ˈbenɪfɪt/", "pos": "n./v.", "meaning": "益处；受益", "example": "Exercise has many benefits.", "freq": "high"},
    {"word": "challenge", "phonetic": "/ˈtʃælɪndʒ/", "pos": "n./v.", "meaning": "挑战；质疑", "example": "Learning Chinese is a challenge.", "freq": "high"},
    {"word": "communicate", "phonetic": "/kəˈmjuːnɪkeɪt/", "pos": "v.", "meaning": "交流；传达", "example": "We communicate by email.", "freq": "high"},
    {"word": "community", "phonetic": "/kəˈmjuːnəti/", "pos": "n.", "meaning": "社区；团体", "example": "The local community is very active.", "freq": "high"},
    {"word": "concern", "phonetic": "/kənˈsɜːn/", "pos": "n./v.", "meaning": "担心；关心；涉及", "example": "Environmental concern is growing.", "freq": "high"},
    {"word": "condition", "phonetic": "/kənˈdɪʃn/", "pos": "n.", "meaning": "条件；状况", "example": "The car is in good condition.", "freq": "high"},
    {"word": "contribute", "phonetic": "/kənˈtrɪbjuːt/", "pos": "v.", "meaning": "贡献；投稿", "example": "Everyone should contribute ideas.", "freq": "high"},
    {"word": "creative", "phonetic": "/kriˈeɪtɪv/", "pos": "adj.", "meaning": "创造性的", "example": "She has a creative mind.", "freq": "high"},
    {"word": "culture", "phonetic": "/ˈkʌltʃə(r)/", "pos": "n.", "meaning": "文化；培养", "example": "Chinese culture is rich and diverse.", "freq": "high"},
    {"word": "decade", "phonetic": "/ˈdekeɪd/", "pos": "n.", "meaning": "十年", "example": "Prices have risen sharply in the last decade.", "freq": "high"},
    {"word": "opportunity", "phonetic": "/ˌɒpəˈtjuːnəti/", "pos": "n.", "meaning": "机会", "example": "Don't miss this opportunity.", "freq": "high"},
    {"word": "experience", "phonetic": "/ɪkˈspɪəriəns/", "pos": "n./v.", "meaning": "经验；经历", "example": "She has 10 years of experience.", "freq": "high"},
    {"word": "environment", "phonetic": "/ɪnˈvaɪrənmənt/", "pos": "n.", "meaning": "环境", "example": "We must protect the environment.", "freq": "high"},
    {"word": "government", "phonetic": "/ˈɡʌvənmənt/", "pos": "n.", "meaning": "政府", "example": "The government announced new policies.", "freq": "high"},
    {"word": "individual", "phonetic": "/ˌɪndɪˈvɪdʒuəl/", "pos": "n./adj.", "meaning": "个人；个人的", "example": "Each individual has unique talents.", "freq": "high"},
    {"word": "influence", "phonetic": "/ˈɪnfluəns/", "pos": "n./v.", "meaning": "影响", "example": "Parents have great influence on children.", "freq": "high"},
    {"word": "knowledge", "phonetic": "/ˈnɒlɪdʒ/", "pos": "n.", "meaning": "知识", "example": "Knowledge is power.", "freq": "high"},
    {"word": "maintain", "phonetic": "/meɪnˈteɪn/", "pos": "v.", "meaning": "维持；维修", "example": "We must maintain good health.", "freq": "high"},
    {"word": "necessary", "phonetic": "/ˈnesəsəri/", "pos": "adj.", "meaning": "必要的", "example": "Sleep is necessary for health.", "freq": "high"},
    {"word": "performance", "phonetic": "/pəˈfɔːməns/", "pos": "n.", "meaning": "表现；表演", "example": "Her performance was excellent.", "freq": "high"},
    {"word": "potential", "phonetic": "/pəˈtenʃl/", "pos": "n./adj.", "meaning": "潜力；潜在的", "example": "He has great potential.", "freq": "high"},
    {"word": "pressure", "phonetic": "/ˈpreʃə(r)/", "pos": "n.", "meaning": "压力", "example": "Students face a lot of pressure.", "freq": "high"},
    {"word": "professional", "phonetic": "/prəˈfeʃənl/", "pos": "adj./n.", "meaning": "专业的；专业人员", "example": "You need professional help.", "freq": "high"},
    {"word": "resource", "phonetic": "/rɪˈsɔːs/", "pos": "n.", "meaning": "资源", "example": "Time is a valuable resource.", "freq": "high"},
    {"word": "responsible", "phonetic": "/rɪˈspɒnsəbl/", "pos": "adj.", "meaning": "负责的", "example": "Who is responsible for this?", "freq": "high"},
    {"word": "significant", "phonetic": "/sɪɡˈnɪfɪkənt/", "pos": "adj.", "meaning": "重要的；显著的", "example": "There is a significant difference.", "freq": "high"},
    {"word": "situation", "phonetic": "/ˌsɪtʃuˈeɪʃn/", "pos": "n.", "meaning": "情况；形势", "example": "The economic situation is improving.", "freq": "high"},
    {"word": "solution", "phonetic": "/səˈluːʃn/", "pos": "n.", "meaning": "解决方案", "example": "We need to find a solution.", "freq": "high"},
    {"word": "technology", "phonetic": "/tekˈnɒlədʒi/", "pos": "n.", "meaning": "技术", "example": "Technology changes our life.", "freq": "high"},
    # 继续添加更多高频词...
    {"word": "ability", "phonetic": "/əˈbɪləti/", "pos": "n.", "meaning": "能力", "example": "He has the ability to solve problems.", "freq": "medium"},
    {"word": "achieve", "phonetic": "/əˈtʃiːv/", "pos": "v.", "meaning": "实现；达到", "example": "She worked hard to achieve her goals.", "freq": "medium"},
    {"word": "approach", "phonetic": "/əˈprəʊtʃ/", "pos": "n./v.", "meaning": "方法；接近", "example": "We need a new approach to this problem.", "freq": "medium"},
    {"word": "attitude", "phonetic": "/ˈætɪtjuːd/", "pos": "n.", "meaning": "态度", "example": "Your attitude determines your success.", "freq": "medium"},
    {"word": "balance", "phonetic": "/ˈbæləns/", "pos": "n./v.", "meaning": "平衡", "example": "Work-life balance is important.", "freq": "medium"},
    {"word": "career", "phonetic": "/kəˈrɪə(r)/", "pos": "n.", "meaning": "职业", "example": "She is building a successful career.", "freq": "medium"},
    {"word": "complex", "phonetic": "/ˈkɒmpleks/", "pos": "adj.", "meaning": "复杂的", "example": "The problem is more complex than it seems.", "freq": "medium"},
    {"word": "concept", "phonetic": "/ˈkɒnsept/", "pos": "n.", "meaning": "概念", "example": "The concept is easy to understand.", "freq": "medium"},
    {"word": "confidence", "phonetic": "/ˈkɒnfɪdəns/", "pos": "n.", "meaning": "信心", "example": "Confidence is key to success.", "freq": "medium"},
    {"word": "consider", "phonetic": "/kənˈsɪdə(r)/", "pos": "v.", "meaning": "考虑；认为", "example": "Please consider my suggestion.", "freq": "medium"},
]


def generate_word_card(word_data):
    """生成单个单词卡片 HTML"""
    freq_class = f"freq-{word_data.get('freq', 'normal')}"
    freq_text = {"high": "超高频", "medium": "高频", "normal": "中频"}.get(word_data.get('freq', 'normal'), "")
    
    roots_html = ""
    if 'roots' in word_data and word_data['roots']:
        roots_html = f'<div class="word-roots"><strong>词根:</strong> {word_data["roots"]}</div>'
    
    return f'''
        <div class="word-card">
            <div class="word-header">
                <div>
                    <div class="word-title">{word_data['word']}<span class="frequency-badge {freq_class}">{freq_text}</span></div>
                    <div class="word-phonetic">{word_data['phonetic']}</div>
                </div>
                <span class="word-pos">{word_data['pos']}</span>
            </div>
            <div class="word-meaning">{word_data['meaning']}</div>
            <div class="word-example">{word_data['example']}</div>
            {roots_html}
        </div>
    '''


def generate_html(words, group_name="CET-4 核心词汇", daily_count=25):
    """生成完整的 HTML 页面"""
    
    # 读取模板
    template_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'card_template.html')
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    else:
        # 使用默认模板
        template = DEFAULT_TEMPLATE
    
    # 生成卡片内容
    cards_content = '\n'.join([generate_word_card(w) for w in words])
    
    # 计算统计信息
    total_words = len(words)
    study_days = (total_words + daily_count - 1) // daily_count
    
    # 替换模板变量
    html = template.replace('{{GROUP_NAME}}', group_name)
    html = html.replace('{{TOTAL_WORDS}}', str(total_words))
    html = html.replace('{{STUDY_DAYS}}', str(study_days))
    html = html.replace('{{DAILY_COUNT}}', str(daily_count))
    html = html.replace('{{CARDS_CONTENT}}', cards_content)
    
    return html


# 默认模板（当文件不存在时使用）
DEFAULT_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CET-4 单词卡片 - {{GROUP_NAME}}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
            line-height: 1.6;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 12px;
        }
        .header h1 { font-size: 28px; margin-bottom: 10px; }
        .stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 15px;
        }
        .stat-item { text-align: center; }
        .stat-number { font-size: 24px; font-weight: bold; }
        .stat-label { font-size: 12px; opacity: 0.8; }
        .card-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        .word-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-left: 4px solid #667eea;
        }
        .word-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 12px;
        }
        .word-title { font-size: 24px; font-weight: bold; color: #333; }
        .word-phonetic { color: #666; font-size: 14px; margin-top: 4px; }
        .word-pos {
            background: #667eea;
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
        }
        .word-meaning {
            color: #444;
            font-size: 15px;
            margin-bottom: 12px;
            padding-bottom: 12px;
            border-bottom: 1px dashed #eee;
        }
        .word-example {
            color: #666;
            font-size: 13px;
            font-style: italic;
        }
        .frequency-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            margin-left: 8px;
        }
        .freq-high { background: #ff6b6b; color: white; }
        .freq-medium { background: #feca57; color: #333; }
        .freq-normal { background: #48dbfb; color: white; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📚 CET-4 单词记忆卡片</h1>
        <p>{{GROUP_NAME}} | 按真题高频排序</p>
        <div class="stats">
            <div class="stat-item"><div class="stat-number">{{TOTAL_WORDS}}</div><div class="stat-label">总词汇</div></div>
            <div class="stat-item"><div class="stat-number">{{STUDY_DAYS}}</div><div class="stat-label">建议天数</div></div>
            <div class="stat-item"><div class="stat-number">{{DAILY_COUNT}}</div><div class="stat-label">每日任务</div></div>
        </div>
    </div>
    <div class="card-container">{{CARDS_CONTENT}}</div>
</body>
</html>'''


def main():
    parser = argparse.ArgumentParser(description='生成 CET-4 单词记忆卡片')
    parser.add_argument('-o', '--output', default='cet4_word_cards.html', help='输出文件名')
    parser.add_argument('-n', '--number', type=int, default=50, help='生成单词数量')
    parser.add_argument('-d', '--daily', type=int, default=25, help='每日学习量')
    parser.add_argument('-g', '--group', default='高频核心词汇', help='词汇组名称')
    parser.add_argument('--start', type=int, default=0, help='起始索引')
    
    args = parser.parse_args()
    
    # 选择单词
    words = DEFAULT_WORDS[args.start:args.start + args.number]
    
    # 生成 HTML
    html = generate_html(words, args.group, args.daily)
    
    # 保存文件
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"[OK] 已生成单词卡片: {args.output}")
    print(f"     - 词汇数量: {len(words)}")
    print(f"     - 建议天数: {(len(words) + args.daily - 1) // args.daily}")
    print(f"     - 每日任务: {args.daily} 个单词")


if __name__ == '__main__':
    main()
