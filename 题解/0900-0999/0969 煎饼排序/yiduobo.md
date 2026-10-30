---
title: "969. 煎饼排序"
aliases: ["yiduobo的每日leetcode 969.煎饼排序"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/361999135"
zhihu_id: "361999135"
zhihu_title: "yiduobo的每日leetcode 969.煎饼排序"
question_id: "969"
question: "煎饼排序"
problem_url: "https://leetcode.cn/problems/pancake-sorting/"
created: "2021-04-02T23:47:29+08:00"
updated: "2021-04-02T23:47:29+08:00"
upvotes: 0
comments: 0
---

# 969. 煎饼排序

> **[yiduobo的每日leetcode 969.煎饼排序](https://zhuanlan.zhihu.com/p/361999135) · 知乎 · 2021-04-02 · 赞同 0**
> 力扣：[969. 煎饼排序](https://leetcode.cn/problems/pancake-sorting/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

969.煎饼排序

[力扣](https://leetcode-cn.com/problems/pancake-sorting/)

由于题目只要求给出一个可行解，同时数组的规模并不大，因此可以按照每一轮将当前剩下数中的最大值归位的思路给出一个构造解法。

具体来说就是对于第k轮，当前最大值应该是n - k，那么我们首先通过一趟遍历找出n - k在数组中的位置pos。若pos \= n - k - 1，说明n - k已经归位，那么继续进行下一轮，否则就想将0到pos反序，然后将0到n - k - 1反序。经过这两轮操作，n - k就处于n - k - 1这个位置了，然后继续下一轮。

一共进行n轮，每轮需要一次遍历以及两次翻转操作，因此最终时间复杂度为O(n^2)。

最后附上python代码：

```python
class Solution(object):
    def pancakeSort(self, arr):
        """
        :type arr: List[int]
        :rtype: List[int]
        """

        n = len(arr)
        res = []
        for target in range(n, 0, -1):
            for pos in range(n):
                if arr[pos] == target:
                    break
            if pos != target - 1:
                if pos != 0:
                    res.append(pos + 1)
                    l = 0
                    r = pos
                    while l < r:
                        arr[l], arr[r] = arr[r], arr[l]
                        l += 1
                        r -= 1

                l = 0
                r = target - 1
                while l < r:
                    arr[l], arr[r] = arr[r], arr[l]
                    l += 1
                    r -= 1
                
                res.append(target)
        
        return res
```
