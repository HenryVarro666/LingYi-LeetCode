---
title: "1246. 删除回文子数组"
aliases: ["yiduobo的每日leetcode 1246.删除回文子数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/614637321"
zhihu_id: "614637321"
zhihu_title: "yiduobo的每日leetcode 1246.删除回文子数组"
question_id: "1246"
question: "删除回文子数组"
problem_url: "https://leetcode.cn/problems/palindrome-removal/"
created: "2023-03-16T23:49:12+08:00"
updated: "2023-03-16T23:49:12+08:00"
upvotes: 0
comments: 0
---

# 1246. 删除回文子数组

> **[yiduobo的每日leetcode 1246.删除回文子数组](https://zhuanlan.zhihu.com/p/614637321) · 知乎 · 2023-03-16 · 赞同 0**
> 力扣：[1246. 删除回文子数组](https://leetcode.cn/problems/palindrome-removal/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1246.删除回文子数组

[力扣](https://leetcode.cn/problems/palindrome-removal/)

动态规划的题目。令f[i][j]表示arr[i]到arr[j]这一段删除所需的最少操作次数，那么对于f[i][j]：

1、若i \= j：

显然有f[i][j] \= 1

2、若i \= j - 1：

若arr[i] \= arr[j]，那么f[i][j] \= 1，否则f[i][j] \= 2

3、其他情况：

若arr[i] \= arr[j]，那么就有f[i][j] \= f[i +1][j - 1]，因为arr[i]和arr[j]的删除可以附着在f[i + 1][j - 1]中的任意一次删除的两侧，因此不需要额外计算删除次数

反之，若arr[i] !\= arr[j]，那么就需要枚举一个分割点cut_pos，将f[i][j]分为f[i][cut_pos]以及f[cut_pos +1][j]来计算，因此就有f[i][j] \= min(f[i][j], f[i][cut_pos] + f[cut_pos + 1][j])

计算完成后，f[0][n - 1]就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def minimumMoves(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        n = len(arr)

        f = [[n] * n for _ in range(n)]

        for length in range(1, n + 1):
            for left in range(n):
                right = left + length - 1
                if right >= n:
                    break
                
                if left == right:
                    f[left][right] = 1
                elif left == right - 1:
                    if arr[left] == arr[right]:
                        f[left][right] = 1
                    else:
                        f[left][right] = 2
                else:
                    if arr[left] == arr[right]:
                        f[left][right] = f[left + 1][right - 1]
                    
                    for cut_pos in range(left, right):
                        f[left][right] = min(f[left][right], f[left][cut_pos] + f[cut_pos + 1][right])
        
        return f[0][n - 1]
```
