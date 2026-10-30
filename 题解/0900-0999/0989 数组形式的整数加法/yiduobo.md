---
title: "989. 数组形式的整数加法"
aliases: ["yiduobo的每日leetcode 989.数组形式的整数加法"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/364332319"
zhihu_id: "364332319"
zhihu_title: "yiduobo的每日leetcode 989.数组形式的整数加法"
question_id: "989"
question: "数组形式的整数加法"
problem_url: "https://leetcode.cn/problems/add-to-array-form-of-integer/"
created: "2021-04-12T23:07:42+08:00"
updated: "2021-04-12T23:07:42+08:00"
upvotes: 0
comments: 0
---

# 989. 数组形式的整数加法

> **[yiduobo的每日leetcode 989.数组形式的整数加法](https://zhuanlan.zhihu.com/p/364332319) · 知乎 · 2021-04-12 · 赞同 0**
> 力扣：[989. 数组形式的整数加法](https://leetcode.cn/problems/add-to-array-form-of-integer/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

989.数组形式的整数加法

[力扣](https://leetcode-cn.com/problems/add-to-array-form-of-integer/)

低配版本的高精度加法。为了方便起见，先将A翻转，此时较小的坐标值对应较低的位数，这样做的好处是方便最终进位。

接下来将K加到A[0]上，然后开始判断进位。具体做法为设p\=0，并检测当前的A[p]是否大于等于10，若大于等于10，那么将A[p + 1]加上1，同时将A[p]减去10，并将p向后移动一位继续检测；若不大于10，那么说明进位到此为止，将A再次反向后输出即可。

在具体实现时需要特别注意进位时的数组边界问题。

最后附上python代码：

```python
class Solution(object):
    def addToArrayForm(self, A, K):
        """
        :type A: List[int]
        :type K: int
        :rtype: List[int]
        """

        l = len(A)
        A.reverse()
        A[0] += K
        now = 0
        while now + 1 < l and A[now] >= 10:
            A[now + 1] += A[now] / 10
            A[now] %= 10
            now += 1

        while A[-1] >= 10:
            A.append(A[-1] / 10)
            A[-2] %= 10
        
        A.reverse()

        return A
```
