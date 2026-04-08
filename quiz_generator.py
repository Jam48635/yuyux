#!/usr/bin/env python3
"""
CET-4 单词测试生成器
生成多种题型的自测题目
"""

import argparse
import random
import os


# 默认词汇库
DEFAULT_WORDS = [
    {"word": "available", "meaning": "可获得的；有空的", "options": ["可获得的", "不可能的", "昂贵的", "困难的"]},
    {"word": "benefit", "meaning": "益处；受益", "options": ["益处", "损失", "危险", "错误"]},
    {"word": "challenge", "meaning": "挑战；质疑", "options": ["挑战", "放弃", "同意", "忽视"]},
    {"word": "communicate", "meaning": "交流；传达", "options": ["交流", "拒绝", "隐藏", "忘记"]},
    {"word": "community", "meaning": "社区；团体", "options": ["社区", "公司", "学校", "家庭"]},
    {"word": "concern", "meaning": "担心；关心", "options": ["担心", "放心", "满意", "开心"]},
    {"word": "condition", "meaning": "条件；状况", "options": ["条件", "结果", "原因", "目的"]},
    {"word": "contribute", "meaning": "贡献；投稿", "options": ["贡献", "索取", "浪费", "破坏"]},
    {"word": "creative", "meaning": "创造性的", "options": ["创造性的", "破坏性的", "传统的", "普通的"]},
    {"word": "culture", "meaning": "文化；培养", "options": ["文化", "自然", "科学", "经济"]},
    {"word": "decade", "meaning": "十年", "options": ["十年", "一年", "百年", "一月"]},
    {"word": "opportunity", "meaning": "机会", "options": ["机会", "困难", "危险", "失败"]},
    {"word": "experience", "meaning": "经验；经历", "options": ["经验", "理论", "想象", "猜测"]},
    {"word": "environment", "meaning": "环境", "options": ["环境", "建筑", "交通", "人口"]},
    {"word": "government", "meaning": "政府", "options": ["政府", "企业", "学校", "医院"]},
    {"word": "individual", "meaning": "个人；个人的", "options": ["个人", "集体", "国家", "社会"]},
    {"word": "influence", "meaning": "影响", "options": ["影响", "忽视", "反对", "支持"]},
    {"word": "knowledge", "meaning": "知识", "options": ["知识", "无知", "技能", "能力"]},
    {"word": "maintain", "meaning": "维持；维修", "options": ["维持", "破坏", "改变", "放弃"]},
    {"word": "necessary", "meaning": "必要的", "options": ["必要的", "多余的", "可选的", "无用的"]},
    {"word": "performance", "meaning": "表现；表演", "options": ["表现", "失败", "准备", "计划"]},
    {"word": "potential", "meaning": "潜力；潜在的", "options": ["潜力", "现状", "过去", "限制"]},
    {"word": "pressure", "meaning": "压力", "options": ["压力", "放松", "舒适", "快乐"]},
    {"word": "professional", "meaning": "专业的", "options": ["专业的", "业余的", "普通的", "临时的"]},
    {"word": "resource", "meaning": "资源", "options": ["资源", "废物", "产品", "商品"]},
    {"word": "responsible", "meaning": "负责的", "options": ["负责的", "逃避的", "懒惰的", "粗心的"]},
    {"word": "significant", "meaning": "重要的；显著的", "options": ["重要的", "微不足道的", "微小的", "普通的"]},
    {"word": "situation", "meaning": "情况；形势", "options": ["情况", "想象", "梦想", "理论"]},
    {"word": "solution", "meaning": "解决方案", "options": ["解决方案", "问题", "困难", "疑问"]},
    {"word": "technology", "meaning": "技术", "options": ["技术", "艺术", "体育", "音乐"]},
]


def generate_choice_question(word_data, all_words):
    """生成选择题"""
    correct = word_data['meaning']
    # 随机选择3个错误选项
    other_meanings = [w['meaning'] for w in all_words if w['word'] != word_data['word']]
    wrong_options = random.sample(other_meanings, min(3, len(other_meanings)))
    
    options = wrong_options + [correct]
    random.shuffle(options)
    
    correct_index = options.index(correct)
    
    return {
        "type": "choice",
        "question": f"{word_data['word']} 的意思是？",
        "options": options,
        "correct": correct_index,
        "answer": correct
    }


def generate_fill_question(word_data):
    """生成填空题（英译中）"""
    return {
        "type": "fill",
        "question": f"{word_data['word']}",
        "hint": f"提示：{word_data['word'][:2]}...",
        "answer": word_data['meaning']
    }


def generate_reverse_question(word_data):
    """生成反向题（中译英）"""
    return {
        "type": "reverse",
        "question": f"写出英文单词：{word_data['meaning']}",
        "hint": f"提示：首字母是 {word_data['word'][0].upper()}",
        "answer": word_data['word']
    }


def generate_quiz(words, question_count=20, mix_ratio=None):
    """生成测试卷"""
    if mix_ratio is None:
        mix_ratio = {"choice": 0.5, "fill": 0.3, "reverse": 0.2}
    
    questions = []
    selected_words = random.sample(words, min(question_count, len(words)))
    
    # 按比例生成各类题型
    choice_count = int(question_count * mix_ratio["choice"])
    fill_count = int(question_count * mix_ratio["fill"])
    reverse_count = question_count - choice_count - fill_count
    
    for i, word in enumerate(selected_words[:choice_count]):
        q = generate_choice_question(word, words)
        q['number'] = i + 1
        questions.append(q)
    
    for i, word in enumerate(selected_words[choice_count:choice_count+fill_count]):
        q = generate_fill_question(word)
        q['number'] = choice_count + i + 1
        questions.append(q)
    
    for i, word in enumerate(selected_words[choice_count+fill_count:]):
        q = generate_reverse_question(word)
        q['number'] = choice_count + fill_count + i + 1
        questions.append(q)
    
    random.shuffle(questions)
    for i, q in enumerate(questions):
        q['number'] = i + 1
    
    return questions


def generate_html_quiz(questions, title="CET-4 单词自测"):
    """生成 HTML 测试卷"""
    
    questions_html = ""
    for q in questions:
        if q['type'] == 'choice':
            options_html = ""
            for i, opt in enumerate(q['options']):
                options_html += f'<label class="option"><input type="radio" name="q{q["number"]}" value="{i}"> {chr(65+i)}. {opt}</label>'
            
            questions_html += f'''
            <div class="question" data-answer="{q['correct']}" data-type="choice">
                <div class="q-number">{q['number']}</div>
                <div class="q-content">
                    <div class="q-text">{q['question']}</div>
                    <div class="options">{options_html}</div>
                    <div class="answer-reveal" style="display:none;">✓ 正确答案：{chr(65+q['correct'])}. {q['answer']}</div>
                </div>
            </div>
            '''
        elif q['type'] == 'fill':
            questions_html += f'''
            <div class="question" data-answer="{q['answer']}" data-type="fill">
                <div class="q-number">{q['number']}</div>
                <div class="q-content">
                    <div class="q-text">{q['question']}</div>
                    <input type="text" class="fill-input" placeholder="输入中文释义">
                    <div class="hint">{q['hint']}</div>
                    <div class="answer-reveal" style="display:none;">✓ 正确答案：{q['answer']}</div>
                </div>
            </div>
            '''
        else:  # reverse
            questions_html += f'''
            <div class="question" data-answer="{q['answer']}" data-type="reverse">
                <div class="q-number">{q['number']}</div>
                <div class="q-content">
                    <div class="q-text">{q['question']}</div>
                    <input type="text" class="fill-input" placeholder="输入英文单词">
                    <div class="hint">{q['hint']}</div>
                    <div class="answer-reveal" style="display:none;">✓ 正确答案：{q['answer']}</div>
                </div>
            </div>
            '''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
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
            padding: 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 12px;
        }}
        .header h1 {{ font-size: 26px; margin-bottom: 8px; }}
        .header p {{ opacity: 0.9; font-size: 14px; }}
        
        .quiz-container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        
        .question {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            display: flex;
            gap: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        
        .q-number {{
            width: 36px;
            height: 36px;
            background: #667eea;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            flex-shrink: 0;
        }}
        
        .q-content {{
            flex: 1;
        }}
        
        .q-text {{
            font-size: 16px;
            color: #333;
            margin-bottom: 12px;
            font-weight: 500;
        }}
        
        .options {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        
        .option {{
            display: flex;
            align-items: center;
            padding: 10px 12px;
            background: #f8f9fa;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        .option:hover {{
            background: #e9ecef;
        }}
        
        .option input {{
            margin-right: 10px;
        }}
        
        .fill-input {{
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 15px;
            transition: border-color 0.2s;
        }}
        
        .fill-input:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .hint {{
            margin-top: 8px;
            font-size: 13px;
            color: #888;
        }}
        
        .answer-reveal {{
            margin-top: 12px;
            padding: 10px;
            background: #e8f5e9;
            color: #2e7d32;
            border-radius: 8px;
            font-size: 14px;
        }}
        
        .controls {{
            max-width: 800px;
            margin: 30px auto;
            display: flex;
            gap: 15px;
            justify-content: center;
        }}
        
        .btn {{
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        .btn-primary {{
            background: #667eea;
            color: white;
        }}
        
        .btn-primary:hover {{
            background: #5a67d8;
        }}
        
        .btn-secondary {{
            background: #e0e0e0;
            color: #333;
        }}
        
        .btn-secondary:hover {{
            background: #d0d0d0;
        }}
        
        .result {{
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background: white;
            border-radius: 12px;
            text-align: center;
            display: none;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        
        .result.show {{ display: block; }}
        
        .score {{
            font-size: 48px;
            font-weight: bold;
            color: #667eea;
        }}
        
        .score-label {{
            color: #666;
            margin-top: 5px;
        }}
        
        @media print {{
            .controls, .btn {{ display: none; }}
            .answer-reveal {{ display: block !important; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📝 {title}</h1>
        <p>共 {len(questions)} 题 | 选择题 + 填空题 | 完成后点击提交查看答案</p>
    </div>
    
    <div class="quiz-container">
        {questions_html}
    </div>
    
    <div class="controls">
        <button class="btn btn-primary" onclick="checkAnswers()">提交答案</button>
        <button class="btn btn-secondary" onclick="window.print()">打印试卷</button>
    </div>
    
    <div class="result" id="result">
        <div class="score" id="score">0</div>
        <div class="score-label">分</div>
    </div>
    
    <script>
        function checkAnswers() {{
            let correct = 0;
            let total = {len(questions)};
            
            document.querySelectorAll('.question').forEach(q => {{
                const type = q.dataset.type;
                const answer = q.dataset.answer;
                const reveal = q.querySelector('.answer-reveal');
                
                let isCorrect = false;
                
                if (type === 'choice') {{
                    const selected = q.querySelector('input:checked');
                    if (selected && selected.value == answer) {{
                        isCorrect = true;
                    }}
                }} else {{
                    const input = q.querySelector('.fill-input');
                    if (input && input.value.trim().toLowerCase() === answer.toLowerCase()) {{
                        isCorrect = true;
                    }}
                }}
                
                if (isCorrect) correct++;
                reveal.style.display = 'block';
            }});
            
            const score = Math.round((correct / total) * 100);
            document.getElementById('score').textContent = score;
            document.getElementById('result').classList.add('show');
            window.scrollTo(0, document.body.scrollHeight);
        }}
    </script>
</body>
</html>
'''
    
    return html


def main():
    parser = argparse.ArgumentParser(description='生成 CET-4 单词测试卷')
    parser.add_argument('-n', '--number', type=int, default=20, help='题目数量')
    parser.add_argument('-o', '--output', default='quiz.html', help='输出文件名')
    parser.add_argument('-t', '--title', default='CET-4 单词自测', help='测试标题')
    parser.add_argument('--choice', type=float, default=0.5, help='选择题比例')
    parser.add_argument('--fill', type=float, default=0.3, help='填空题比例')
    
    args = parser.parse_args()
    
    # 计算比例
    reverse_ratio = 1 - args.choice - args.fill
    mix_ratio = {
        "choice": args.choice,
        "fill": args.fill,
        "reverse": max(0, reverse_ratio)
    }
    
    # 生成测试
    questions = generate_quiz(DEFAULT_WORDS, args.number, mix_ratio)
    html = generate_html_quiz(questions, args.title)
    
    # 保存
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"[OK] 已生成测试卷: {args.output}")
    print(f"     - 题目数量: {len(questions)}")
    print(f"     - 选择题: {int(args.number * args.choice)} 题")
    print(f"     - 英译中: {int(args.number * args.fill)} 题")
    print(f"     - 中译英: {args.number - int(args.number * args.choice) - int(args.number * args.fill)} 题")


if __name__ == '__main__':
    main()
