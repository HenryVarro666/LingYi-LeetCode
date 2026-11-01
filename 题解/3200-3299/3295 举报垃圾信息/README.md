# 3295. 举报垃圾信息

Medium · [力扣原题](https://leetcode.cn/problems/report-spam-message/)

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 动画（GIF）](3295%20举报垃圾信息%20·%20灵茶山艾府.gif) · [mp4 文件](3295%20举报垃圾信息%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 动画（GIF）](3295%20举报垃圾信息%20·%20yiduobo.gif) · [mp4 文件](3295%20举报垃圾信息%20·%20yiduobo.mp4) |

## 动画讲解

> 动图会循环播放；想暂停、拖进度条请下载上面表格里的 mp4 文件。

### 灵茶山艾府

![3295 举报垃圾信息 · 灵茶山艾府](3295%20举报垃圾信息%20·%20灵茶山艾府.gif)

### yiduobo

![3295 举报垃圾信息 · yiduobo](3295%20举报垃圾信息%20·%20yiduobo.gif)


## 题目描述

给你一个字符串数组 `message` 和一个字符串数组 `bannedWords`。

如果数组中 **至少** 存在两个单词与 `bannedWords` 中的任一单词 **完全相同**，则该数组被视为 **垃圾信息**。

如果数组 `message` 是垃圾信息，则返回 `true`；否则返回 `false`。

**示例 1：**

**输入：** `message = ["hello","world","leetcode"], bannedWords = ["world","hello"]`

**输出：** `true`

**解释：**

数组 `message` 中的 `"hello"` 和 `"world"` 都出现在数组 `bannedWords` 中。

**示例 2：**

**输入：** `message = ["hello","programming","fun"], bannedWords = ["world","programming","leetcode"]`

**输出：** `false`

**解释：**

数组 `message` 中只有一个单词（`"programming"`）出现在数组 `bannedWords` 中。

**提示：**

- `1 <= message.length, bannedWords.length <= 10⁵`

- `1 <= message[i].length, bannedWords[i].length <= 15`

- `message[i]` 和 `bannedWords[i]` 都只由小写英文字母组成。

---
[↑ 返回 3200-3299](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
