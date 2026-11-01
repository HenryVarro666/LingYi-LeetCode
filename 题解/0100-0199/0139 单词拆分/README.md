# 139. 单词拆分

Medium · [力扣原题](https://leetcode.cn/problems/word-break/)

所在刷题路径：labuladong、灵神核心路线、灵神突击、灵神题单·动态规划、灵神题单·常用数据结构

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 动画（GIF）](0139%20单词拆分%20·%20灵茶山艾府.gif) · [mp4 文件](0139%20单词拆分%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 动画（GIF）](0139%20单词拆分%20·%20yiduobo.gif) · [mp4 文件](0139%20单词拆分%20·%20yiduobo.mp4) |

## 动画讲解

> 动图会循环播放；想暂停、拖进度条请下载上面表格里的 mp4 文件。

### 灵茶山艾府

![0139 单词拆分 · 灵茶山艾府](0139%20单词拆分%20·%20灵茶山艾府.gif)

### yiduobo

![0139 单词拆分 · yiduobo](0139%20单词拆分%20·%20yiduobo.gif)


## 题目描述

给你一个字符串 `s` 和一个字符串列表 `wordDict` 作为字典。如果可以利用字典中出现的一个或多个单词拼接出 `s` 则返回 `true`。

**注意：**不要求字典中出现的单词全部都使用，并且字典中的单词可以重复使用。

**示例 1：**

```

输入: s = "leetcode", wordDict = ["leet", "code"]
输出: true
解释: 返回 true 因为 "leetcode" 可以由 "leet" 和 "code" 拼接成。
```

**示例 2：**

```

输入: s = "applepenapple", wordDict = ["apple", "pen"]
输出: true
解释: 返回 true 因为 "applepenapple" 可以由 "apple" "pen" "apple" 拼接成。
     注意，你可以重复使用字典中的单词。
```

**示例 3：**

```

输入: s = "catsandog", wordDict = ["cats", "dog", "sand", "and", "cat"]
输出: false
```

**提示：**

- `1 <= s.length <= 300`

- `1 <= wordDict.length <= 1000`

- `1 <= wordDict[i].length <= 20`

- `s` 和 `wordDict[i]` 仅由小写英文字母组成

- `wordDict` 中的所有字符串 **互不相同**

---
[↑ 返回 0100-0199](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
