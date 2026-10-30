---
title: "2946. 循环移位后的矩阵相似检测"
aliases: ["yiduobo的每日leetcode 2946.循环移位后的矩阵相似检测"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/八-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/691820218"
zhihu_id: "691820218"
zhihu_title: "yiduobo的每日leetcode 2946.循环移位后的矩阵相似检测"
question_id: "2946"
question: "循环移位后的矩阵相似检查"
problem_url: "https://leetcode.cn/problems/matrix-similarity-after-cyclic-shifts/"
difficulty: "Easy"
rating: 1406
created: "2024-04-11T02:00:23+08:00"
updated: "2024-04-11T02:00:23+08:00"
upvotes: 1
comments: 0
---

# 2946. 循环移位后的矩阵相似检测

> **[yiduobo的每日leetcode 2946.循环移位后的矩阵相似检测](https://zhuanlan.zhihu.com/p/691820218) · 知乎 · 2024-04-11 · 赞同 1**
> 力扣：[2946. 循环移位后的矩阵相似检查](https://leetcode.cn/problems/matrix-similarity-after-cyclic-shifts/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2946.循环移位后的矩阵相似检测

[. - 力扣（LeetCode）](https://leetcode.cn/problems/matrix-similarity-after-cyclic-shifts/description/)

令m表示矩阵的列数，那么当k >\= m时，会出现套圈的情况，因此在这里可以先将k对m取模。而对于一个长度为m的数组，将其中的元素向左移动k位，就相当于将其中的元素向右移动m - k位，于是可以在进行比较之前可以先通过这个计算将问题都转化为每一行对应的数组向右移动的问题。

不妨设当前行的元素需要向后移动t位，那么原来处于第j列的元素将被移动到(j + t) % m位，于是只需遍历每一行然后计算出对应的t，然后遍历行中的元素，检测目标元素是否与当前元素相等即可。

最后附上python代码：

```python
class Solution(object):
    def areSimilar(self, mat, k):
        """
        :type mat: List[List[int]]
        :type k: int
        :rtype: bool
        """

        n = len(mat)
        m = len(mat[0])

        k %= m

        for i in range(n):
            if i % 2 == 0:
                t = m - k
            else:
                t = k

            for j in range(m):
                if mat[i][j] != mat[i][(j + t) % m]:
                    return False

        return True
```
