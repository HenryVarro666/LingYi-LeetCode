# 3582. 为视频标题生成标签

Easy · [力扣原题](https://leetcode.cn/problems/generate-tag-for-video-caption/)

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 动画（GIF）](3582%20为视频标题生成标签%20·%20灵茶山艾府.gif) · [mp4 文件](3582%20为视频标题生成标签%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 动画（GIF）](3582%20为视频标题生成标签%20·%20yiduobo.gif) · [mp4 文件](3582%20为视频标题生成标签%20·%20yiduobo.mp4) |

## 动画讲解

> 动图会循环播放；想暂停、拖进度条请下载上面表格里的 mp4 文件。

### 灵茶山艾府

![3582 为视频标题生成标签 · 灵茶山艾府](3582%20为视频标题生成标签%20·%20灵茶山艾府.gif)

### yiduobo

![3582 为视频标题生成标签 · yiduobo](3582%20为视频标题生成标签%20·%20yiduobo.gif)


## 题目描述

给你一个字符串 `caption`，表示一个视频的标题。

需要按照以下步骤 **按顺序** 生成一个视频的 **有效标签** ：

1.

将 **所有单词** 组合为单个 **驼峰命名字符串** ，并在前面加上 `'#'`。**驼峰命名字符串** 指的是除第一个单词外，其余单词的首字母大写，且每个单词的首字母之后的字符必须是小写。

2.

**移除** 所有不是英文字母的字符，但 **保留** 第一个字符 `'#'`。

3.

将结果 **截断** 为最多 100 个字符。

对 `caption` 执行上述操作后，返回生成的 **标签** 。

**示例 1：**

**输入：** `caption = "Leetcode daily streak achieved"`

**输出：** `"#leetcodeDailyStreakAchieved"`

**解释：**

除了 `"leetcode"` 以外的所有单词的首字母需要大写。

**示例 2：**

**输入：** `caption = "can I Go There"`

**输出：** `"#canIGoThere"`

**解释：**

除了 `"can"` 以外的所有单词的首字母需要大写。

**示例 3：**

**输入：** `caption = "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"`

**输出：** `"#hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"`

**解释：**

由于第一个单词长度为 101，因此需要从单词末尾截去最后两个字符。

**提示：**

- `1 <= caption.length <= 150`

- `caption` 仅由英文字母和 `' '` 组成。

---
[↑ 返回 3500-3599](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
