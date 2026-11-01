# LCR 129. 字母迷宫

Medium · [力扣原题](https://leetcode.cn/problems/ju-zhen-zhong-de-lu-jing-lcof/)

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 动画（GIF）](LCR%20129%20字母迷宫%20·%20灵茶山艾府.gif) · [mp4 文件](LCR%20129%20字母迷宫%20·%20灵茶山艾府.mp4) |
| yiduobo | — | — |

## 动画讲解

> 动图会循环播放；想暂停、拖进度条请下载上面表格里的 mp4 文件。

### 灵茶山艾府

![LCR 129 字母迷宫 · 灵茶山艾府](LCR%20129%20字母迷宫%20·%20灵茶山艾府.gif)


## 题目描述

字母迷宫游戏初始界面记作 `m x n` 二维字符串数组 `grid`，请判断玩家是否能在 `grid` 中找到目标单词 `target`。

注意：寻找单词时 **必须** 按照字母顺序，通过水平或垂直方向相邻的单元格内的字母构成，同时，同一个单元格内的字母 **不允许被重复使用** 。

![](../../_assets/灵茶山艾府/868c28442626d8ae.jpg)

**示例 1：**

```

输入：grid = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], target = "ABCCED"
输出：true
```

**示例 2：**

```

输入：grid = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], target = "SEE"
输出：true
```

**示例 3：**

```

输入：grid = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], target = "ABCB"
输出：false
```

**提示：**

- `m == grid.length`

- `n = grid[i].length`

- `1 <= m, n <= 6`

- `1 <= target.length <= 15`

- `grid` 和 `target` 仅由大小写英文字母组成

**注意：**本题与主站 79 题相同：[https://leetcode.cn/problems/word-search/](https://leetcode.cn/problems/word-search/)

---
[↑ 返回 LCR](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
