# 1616. 分割两个字符串得到回文串

Medium · 难度分 1868 · [力扣原题](https://leetcode.cn/problems/split-two-strings-to-make-palindrome/)

所在刷题路径：灵神题单·滑动窗口与双指针、灵神题单·贪心与思维

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 动画（GIF）](1616%20分割两个字符串得到回文串%20·%20灵茶山艾府.gif) · [mp4 文件](1616%20分割两个字符串得到回文串%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 动画（GIF）](1616%20分割两个字符串得到回文串%20·%20yiduobo.gif) · [mp4 文件](1616%20分割两个字符串得到回文串%20·%20yiduobo.mp4) |

## 动画讲解

> 动图会循环播放；想暂停、拖进度条请下载上面表格里的 mp4 文件。

### 灵茶山艾府

![1616 分割两个字符串得到回文串 · 灵茶山艾府](1616%20分割两个字符串得到回文串%20·%20灵茶山艾府.gif)

### yiduobo

![1616 分割两个字符串得到回文串 · yiduobo](1616%20分割两个字符串得到回文串%20·%20yiduobo.gif)


## 题目描述

给你两个字符串 `a` 和 `b` ，它们长度相同。请你选择一个下标，将两个字符串都在 **相同的下标** 分割开。由 `a` 可以得到两个字符串： `a_prefix` 和 `a_suffix` ，满足 `a = a_prefix + a_suffix`<sub> </sub>，同理，由 `b` 可以得到两个字符串 `b_prefix` 和 `b_suffix` ，满足 `b = b_prefix + b_suffix` 。请你判断 `a_prefix + b_suffix` 或者 `b_prefix + a_suffix` 能否构成回文串。

当你将一个字符串 `s` 分割成 `s_prefix` 和 `s_suffix` 时， `s_suffix` 或者 `s_prefix` 可以为空。比方说， `s = "abc"` 那么 `"" + "abc"` ， `"a" + "bc" `， `"ab" + "c"` 和 `"abc" + ""` 都是合法分割。

如果 **能构成回文字符串** ，那么请返回 `true`，否则返回 `false` 。

**注意**， `x + y` 表示连接字符串 `x` 和 `y` 。

**示例 1：**

```

输入：a = "x", b = "y"
输出：true
解释：如果 a 或者 b 是回文串，那么答案一定为 true ，因为你可以如下分割：
a_prefix = "", a_suffix = "x"
b_prefix = "", b_suffix = "y"
那么 a_prefix + b_suffix = "" + "y" = "y" 是回文串。
```

**示例 2：**

```

输入：a = "xbdef", b = "xecab"
输出：false
```

**示例 3：**

```

输入：a = "ulacfd", b = "jizalu"
输出：true
解释：在下标为 3 处分割：
a_prefix = "ula", a_suffix = "cfd"
b_prefix = "jiz", b_suffix = "alu"
那么 a_prefix + b_suffix = "ula" + "alu" = "ulaalu" 是回文串。
```

**提示：**

- `1 <= a.length, b.length <= 10⁵`

- `a.length == b.length`

- `a` 和 `b` 都只包含小写英文字母

---
[↑ 返回 1600-1699](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
