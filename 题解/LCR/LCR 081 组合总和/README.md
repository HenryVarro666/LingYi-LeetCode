# LCR 081. 组合总和

Medium · [力扣原题](https://leetcode.cn/problems/Ygoe9J/)

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 动画（GIF）](LCR%20081%20组合总和%20·%20灵茶山艾府.gif) · [mp4 文件](LCR%20081%20组合总和%20·%20灵茶山艾府.mp4) |
| yiduobo | — | — |

## 动画讲解

> 动图会循环播放；想暂停、拖进度条请下载上面表格里的 mp4 文件。

### 灵茶山艾府

![LCR 081 组合总和 · 灵茶山艾府](LCR%20081%20组合总和%20·%20灵茶山艾府.gif)


## 题目描述

给定一个**无重复元素**的正整数数组 `candidates` 和一个正整数 `target` ，找出 `candidates` 中所有可以使数字和为目标数 `target` 的唯一组合。

`candidates` 中的数字可以无限制重复被选取。如果至少一个所选数字数量不同，则两种组合是不同的。

对于给定的输入，保证和为 `target` 的唯一组合数少于 `150` 个。

**示例 1：**

```

输入: candidates = [2,3,6,7], target = 7
输出: [[7],[2,2,3]]
```

**示例 2：**

```

输入: candidates = [2,3,5], target = 8
输出: [[2,2,2,2],[2,3,3],[3,5]]
```

**示例 3：**

```

输入: candidates = [2], target = 1
输出: []
```

**示例 4：**

```

输入: candidates = [1], target = 1
输出: [[1]]
```

**示例 5：**

```

输入: candidates = [1], target = 2
输出: [[1,1]]
```

**提示：**

- `1 <= candidates.length <= 30`

- `1 <= candidates[i] <= 200`

- `candidate` 中的每个元素都是独一无二的。

- `1 <= target <= 500`

注意：本题与主站 39 题相同： [https://leetcode.cn/problems/combination-sum/](https://leetcode.cn/problems/combination-sum/)

---
[↑ 返回 LCR](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
