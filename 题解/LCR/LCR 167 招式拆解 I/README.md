# LCR 167. 招式拆解 I

Medium · [力扣原题](https://leetcode.cn/problems/zui-chang-bu-han-zhong-fu-zi-fu-de-zi-zi-fu-chuan-lcof/)

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 动画（GIF）](LCR%20167%20招式拆解%20I%20·%20灵茶山艾府.gif) · [mp4 文件](LCR%20167%20招式拆解%20I%20·%20灵茶山艾府.mp4) |
| yiduobo | — | — |

## 动画讲解

> 动图会循环播放；想暂停、拖进度条请下载上面表格里的 mp4 文件。

### 灵茶山艾府

![LCR 167 招式拆解 I · 灵茶山艾府](LCR%20167%20招式拆解%20I%20·%20灵茶山艾府.gif)


## 题目描述

某套连招动作记作序列 `arr`，其中 `arr[i]` 为第 `i` 个招式的名字。请返回 `arr` 中最多可以出连续不重复的多少个招式。

**示例 1：**

```

输入：arr = "dbascDdad"
输出：6
解释：因为连续且最长的招式序列是 "dbascD" 或 "bascDd"，所以其长度为 6。
```

**示例 2：**

```

输入：arr = "KKK"
输出：1
解释：因为无重复字符的最长子串是 "K"，所以其长度为 1。
```

**示例 3：**

```

输入：arr = "pwwkew"
输出：3
解释：因为连续且最长的招式序列是 "wke"，所以其长度为 3。
请注意区分 子串 与 子序列 的概念：你的答案必须是 连续招式 的长度，也就是 子串。而 "pwke" 是一个非连续的 子序列，不是 子串。
```

**提示：**

- `0 <= arr.length <= 40000`

- `arr` 由英文字母、数字、符号和空格组成。

注意：本题与主站 3 题相同：[https://leetcode.cn/problems/longest-substring-without-repeating-characters/](https://leetcode.cn/problems/longest-substring-without-repeating-characters/)

---
[↑ 返回 LCR](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
