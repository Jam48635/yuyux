# 🎓 CET-4 单词记忆学习助手

> 基于艾宾浩斯遗忘曲线的英语四级高频词汇记忆工具

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ 功能特性

- 📇 **单词卡片生成** - 美观的 HTML 卡片，支持打印
- 📅 **智能学习计划** - 基于艾宾浩斯遗忘曲线的复习安排
- 📝 **自测练习** - 选择+填空题型，支持在线评分
- 🎯 **高频词汇** - 精选四级真题核心词汇

## 📂 项目结构

```
cet4-vocabulary-trainer/
├── README.md                 # 项目说明
├── SKILL.md                  # 使用指南
├── assets/
│   └── card_template.html    # 卡片模板
├── references/
│   ├── high_freq_words.md    # 高频词汇表
│   └── word_roots.md         # 词根词缀表
└── scripts/
    ├── word_card.py          # 单词卡片生成器
    ├── study_plan.py         # 学习计划生成器
    └── quiz_generator.py     # 测试卷生成器
```

## 🚀 快速开始

### 1. 生成学习计划

```bash
cd scripts
python study_plan.py -w 300 -d 20 -o my_plan.html
```

参数说明：
- `-w`: 总词汇量（默认500）
- `-d`: 每日新词量（默认25）
- `-o`: 输出文件名

### 2. 生成单词卡片

```bash
python word_card.py -n 20 -o cards.html
```

参数说明：
- `-n`: 单词数量
- `--start`: 起始索引（用于分批学习）

### 3. 生成自测练习

```bash
python quiz_generator.py -n 15 -t "第一周测试"
```

## 📊 学习计划示例

| 天数 | 新词 | 复习内容 |
|------|------|----------|
| Day 1 | 1-20 | - |
| Day 2 | 21-40 | Day 1 |
| Day 3 | 41-60 | Day 2, Day 1 |
| Day 4 | 61-80 | Day 3, Day 2 |
| Day 5 | 81-100 | Day 4, Day 3, Day 1 |

> 复习间隔：1-2-4-7-15 天（艾宾浩斯遗忘曲线）

## 📖 学习建议

1. **优先掌握超高频词汇**（前100词）
2. **每天学习20-30词**，不要贪多
3. **按时复习**，复习比学新词更重要
4. **结合例句记忆**，了解单词用法
5. **每周自测**，检验掌握情况

## 🛠️ 环境要求

- Python 3.8+
- 现代浏览器（Chrome/Firefox/Edge）

## 📄 许可证

MIT License

---

**祝四级考试顺利！** 🎯
