# 68. 文本左右对齐

Hard · [力扣原题](https://leetcode.cn/problems/text-justification/)

所在刷题路径：灵神突击、灵神题单·滑动窗口与双指针、灵神题单·常用数据结构

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 动画（GIF）](0068%20文本左右对齐%20·%20灵茶山艾府.gif) · [mp4 文件](0068%20文本左右对齐%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 动画（GIF）](0068%20文本左右对齐%20·%20yiduobo.gif) · [mp4 文件](0068%20文本左右对齐%20·%20yiduobo.mp4) |

## 动画讲解

> 动图会循环播放；想暂停、拖进度条请下载上面表格里的 mp4 文件。

### 灵茶山艾府

![0068 文本左右对齐 · 灵茶山艾府](0068%20文本左右对齐%20·%20灵茶山艾府.gif)

### yiduobo

![0068 文本左右对齐 · yiduobo](0068%20文本左右对齐%20·%20yiduobo.gif)


## 题目描述

给定一个单词数组 `words` 和一个长度 `maxWidth` ，重新排版单词，使其成为每行恰好有 `maxWidth` 个字符，且左右两端对齐的文本。

你应该使用 “**贪心算法**” 来放置给定的单词；也就是说，尽可能多地往每行中放置单词。必要时可用空格 `' '` 填充，使得每行恰好有 <em>maxWidth</em> 个字符。

要求尽可能均匀分配单词间的空格数量。如果某一行单词间的空格不能均匀分配，则左侧放置的空格数要多于右侧的空格数。

文本的最后一行应为左对齐，且单词之间不插入**额外的**空格。

**注意:**

- 单词是指由非空格字符组成的字符序列。

- 每个单词的长度大于 0，小于等于 <em>maxWidth</em>。

- 输入单词数组 `words` 至少包含一个单词。

**示例 1:**

```

输入: words = ["This", "is", "an", "example", "of", "text", "justification."], maxWidth = 16
输出:
[
   "This    is    an",
   "example  of text",
   "justification.  "
]
```

**示例 2:**

```

输入:words = ["What","must","be","acknowledgment","shall","be"], maxWidth = 16
输出:
[
  "What   must   be",
  "acknowledgment  ",
  "shall be        "
]
解释: 注意最后一行的格式应为 "shall be    " 而不是 "shall     be",
     因为最后一行应为左对齐，而不是左右两端对齐。
     第二行同样为左对齐，这是因为这行只包含一个单词。
```

**示例 3:**

```

输入:words = ["Science","is","what","we","understand","well","enough","to","explain","to","a","computer.","Art","is","everything","else","we","do"]，maxWidth = 20
输出:
[
  "Science  is  what we",
  "understand      well",
  "enough to explain to",
  "a  computer.  Art is",
  "everything  else  we",
  "do                  "
]
```

**提示:**

- `1 <= words.length <= 300`

- `1 <= words[i].length <= 20`

- `words[i]` 由小写英文字母和符号组成

- `1 <= maxWidth <= 100`

- `words[i].length <= maxWidth`

---
[↑ 返回 0000-0099](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
