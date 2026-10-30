---
title: "3468. 可行数组的数目"
aliases: ["yiduobo的每日leetcode 3468.可行数组的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1895962339540453155"
zhihu_id: "1895962339540453155"
zhihu_title: "yiduobo的每日leetcode 3468.可行数组的数目"
question_id: "3468"
question: "可行数组的数目"
problem_url: "https://leetcode.cn/problems/find-the-number-of-copy-arrays/"
difficulty: "Medium"
rating: 1545
created: "2025-04-17T00:39:19+08:00"
updated: "2025-04-17T00:39:19+08:00"
upvotes: 0
comments: 0
---

# 3468. 可行数组的数目

> **[yiduobo的每日leetcode 3468.可行数组的数目](https://zhuanlan.zhihu.com/p/1895962339540453155) · 知乎 · 2025-04-17 · 赞同 0**
> 力扣：[3468. 可行数组的数目](https://leetcode.cn/problems/find-the-number-of-copy-arrays/) · Medium · 灵茶山艾府：[详细数学推导（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3468.可行数组的数目

[3468. 可行数组的数目 - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-number-of-copy-arrays/description/)

题目给出一个长度为n的数组original和一个长度为n \* 2的二维数组bounds，其中bounds\[index\] \= \[u\[index\], v\[index\]\]。现在需要找出长度为n，且满足一下条件的可能的数组copy的数量：

1、对于1 \<\= index \<\= n - 1，都有copy[index] - copy[index -1] \= original[index] - original[index - 1]

2、对于0 \<\= index \<\= n - 1，都有u[index] \<\= copy[index] \<\= v[index]

首先观察题目给出的条件1，将下标相同的项移动到同一侧，就有

copy[index] - original[index] \= copy[index - 1] - original[index - 1]

可以发现，copy就相当于对original中的每一项都加上了同一个偏移量offset，而本题就转化成了计算有多少种可行的offset可以使得copy满足条件2。

对于条件2，实际上就是要求对于每个index都满足u[index] \<\= original[index] + offset \<\= v[index]，那么在这里就有u[index] - original[index] \<\= offset \<\= v[index] - original[index]。

一共可以得到n个这样的不等式，而最终offset的取值范围就是max(u[index] - original[index]) \<\= offset \<\= min(v[index] - original[index])。

记x \= max(u[index] - original[index])，y \= min(v[index] - original[index])，那么当x \<\= y时，offset有x到y一共y - x + 1个可行的取值，答案就是y - x + 1，否则offset没有可行的取值，答案为0。

最后附上python代码：

```python
class Solution(object):
    def countArrays(self, original, bounds):
        """
        :type original: List[int]
        :type bounds: List[List[int]]
        :rtype: int
        """
        
        x, y = None, None
        for o, (u, v) in zip(original, bounds):
            new_x, new_y = u - o, v - o
            if x is None or x < new_x:
                x = new_x
            if y is None or y > new_y:
                y = new_y
        
        if x <= y:
            return y - x + 1
        else:
            return 0
```
