---
name: cet4-vocabulary-trainer
description: CET-4 英语四级单词记忆学习助手。用于生成高频词汇记忆卡片、制定艾宾浩斯复习计划、创建自测练习题。支持 HTML 输出可打印的单词卡片和学习计划。当用户需要备考英语四级、记忆单词、制定学习计划或进行词汇自测时使用此 Skill。
---

# CET-4 单词记忆学习助手

帮助用户高效记忆英语四级高频词汇，提供卡片生成、学习规划和自测功能。

## 核心功能

1. **单词卡片生成** - 生成美观的 HTML 单词卡片（含音标、释义、例句）
2. **学习计划制定** - 基于艾宾浩斯遗忘曲线的复习计划
3. **自测练习生成** - 生成选择题、填空题等多种题型的测试卷

## 使用脚本

所有脚本位于 `scripts/` 目录：

### 1. 生成单词卡片

```bash
python scripts/word_card.py [选项]
```

参数：
- `-o, --output`: 输出文件名 (默认: cet4_word_cards.html)
- `-n, --number`: 生成单词数量 (默认: 50)
- `-d, --daily`: 每日学习量，用于计算建议天数 (默认: 25)
- `-g, --group`: 词汇组名称 (默认: 高频核心词汇)
- `--start`: 起始索引 (默认: 0)

示例：
```bash
# 生成前100个高频词卡片
python scripts/word_card.py -n 100 -o day1_cards.html

# 生成第51-100个词
python scripts/word_card.py --start 50 -n 50 -o day2_cards.html
```

### 2. 生成学习计划

```bash
python scripts/study_plan.py [选项]
```

参数：
- `-w, --words`: 总词汇量 (默认: 500)
- `-d, --daily`: 每日新词量 (默认: 25)
- `-s, --start`: 开始日期 YYYY-MM-DD (默认: 今天)
- `-o, --output`: 输出文件名 (默认: study_plan.html)
- `--md`: 同时生成 Markdown 版本

示例：
```bash
# 30天背完450词，每天15词
python scripts/study_plan.py -w 450 -d 15 -o my_plan.html --md
```

### 3. 生成测试卷

```bash
python scripts/quiz_generator.py [选项]
```

参数：
- `-n, --number`: 题目数量 (默认: 20)
- `-o, --output`: 输出文件名 (默认: quiz.html)
- `-t, --title`: 测试标题
- `--choice`: 选择题比例 (默认: 0.5)
- `--fill`: 填空题比例 (默认: 0.3)

示例：
```bash
# 生成30题的测试卷
python scripts/quiz_generator.py -n 30 -t "第一周复习测试"
```

## 参考资源

- `references/high_freq_words.md` - CET-4 高频核心词汇表（约250词）
- `references/word_roots.md` - 常见词根词缀速记表

## 推荐学习流程

1. **第一阶段：制定计划**
   ```bash
   python scripts/study_plan.py -w 300 -d 20 -o plan.html
   ```

2. **第二阶段：每日学习**
   ```bash
   # Day 1: 生成第1-20词卡片
   python scripts/word_card.py --start 0 -n 20 -o day1.html
   
   # Day 2: 生成第21-40词卡片
   python scripts/word_card.py --start 20 -n 20 -o day2.html
   ```

3. **第三阶段：定期自测**
   ```bash
   # 每周末生成测试卷
   python scripts/quiz_generator.py -n 25 -t "Week 1 Review"
   ```

## HTML 输出特点

- **响应式设计** - 适配手机、平板、电脑
- **打印优化** - 可直接打印成纸质卡片
- **美观配色** - 采用渐变色和卡片式布局
- **交互功能** - 测试卷支持在线答题和自动评分

## 学习建议

1. **优先掌握超高频词汇**（前100词）- 真题出现率最高
2. **每天学习20-30词** - 配合艾宾浩斯复习节奏
3. **结合词根记忆** - 参考 word_roots.md 举一反三
4. **真题语境记忆** - 每个单词都配有真题例句
5. **坚持每日打卡** - 按计划完成新学和复习任务
