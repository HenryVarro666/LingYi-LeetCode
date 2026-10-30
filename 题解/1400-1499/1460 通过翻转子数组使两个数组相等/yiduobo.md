---
title: "1460. 通过翻转子数组使两个数组相等"
aliases: ["yiduobo的每日leetcode 1460.通过翻转子数组使两个数组相等"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/412436887"
zhihu_id: "412436887"
zhihu_title: "yiduobo的每日leetcode 1460.通过翻转子数组使两个数组相等"
question_id: "1460"
question: "通过翻转子数组使两个数组相等"
problem_url: "https://leetcode.cn/problems/make-two-arrays-equal-by-reversing-sub-arrays/"
created: "2021-09-21T13:53:55+08:00"
updated: "2021-09-21T13:53:55+08:00"
upvotes: 0
comments: 0
---

# 1460. 通过翻转子数组使两个数组相等

> **[yiduobo的每日leetcode 1460.通过翻转子数组使两个数组相等](https://zhuanlan.zhihu.com/p/412436887) · 知乎 · 2021-09-21 · 赞同 0**
> 力扣：[1460. 通过翻转子数组使两个数组相等](https://leetcode.cn/problems/make-two-arrays-equal-by-reversing-sub-arrays/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1460.通过翻转子数组使得两个数组相等

[力扣](https://leetcode-cn.com/problems/make-two-arrays-equal-by-reversing-sub-arrays/)

由于题目不要求使得翻转次数最少，因此可以使用一种简单的构造法。

遍历target，若此时的target[index]不等于arr[index]，那么我们找出最小的p，满足p > index以及arr[p] \= target[index]。翻转index到p这一段，就能让target[index]与arr[index]相等了。接下来依次处理后续的所有数即可。

这样一来，就只需要考察target以及arr中各个数出现的次数是否完全一样即可。

最后附上python代码：

```python
class Solution(object):
    def canBeEqual(self, target, arr):
        """
        :type target: List[int]
        :type arr: List[int]
        :rtype: bool
        """

        cnt_list = [0] * 1001
        for num in target:
            cnt_list[num] += 1
        
        for num in arr:
            cnt_list[num] -= 1
            if cnt_list[num] < 0:
                return False

        return True
```
