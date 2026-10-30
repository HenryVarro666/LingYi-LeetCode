---
title: "1053. 交换一次的先前排列"
aliases: ["yiduobo的每日leetcode 1053.交换一次的先前排列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/372113100"
zhihu_id: "372113100"
zhihu_title: "yiduobo的每日leetcode 1053.交换一次的先前排列"
question_id: "1053"
question: "交换一次的先前排列"
problem_url: "https://leetcode.cn/problems/previous-permutation-with-one-swap/"
created: "2021-05-13T21:32:53+08:00"
updated: "2021-05-13T21:32:53+08:00"
upvotes: 0
comments: 0
---

# 1053. 交换一次的先前排列

> **[yiduobo的每日leetcode 1053.交换一次的先前排列](https://zhuanlan.zhihu.com/p/372113100) · 知乎 · 2021-05-13 · 赞同 0**
> 力扣：[1053. 交换一次的先前排列](https://leetcode.cn/problems/previous-permutation-with-one-swap/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1053.交换一次的先前排列

[力扣](https://leetcode-cn.com/problems/previous-permutation-with-one-swap/)

回忆一下之前做过的求下一个排列的问题，本题与其类似，同样是从后向前进行一趟扫描，不过这里需要找出第一次出现逆序的位置p。若找不到，则说明当前arr已经是最小的排列，那么直接返回即可。

对于找到p而言，当前状况是arr[p + 1]到arr[-1]这些数目前是单调不减的，形成了最小的一种排列，我们现在需要从中间找到一个q，然后交换arr[p]和arr[q]。为了使得交换后的答案最大，那么我们就需要arr[q]尽可能大，但也需要满足arr[q] \< arr[p]。若存在同样大小的arr[q1]以及arr[q2]，我们则应该选择靠后的那一个。根据以上条件，我们可以从arr[p + 1]到arr[-1]中间找出一个q，然后交换arr[p]和arr[q]即可。

最后附上python代码：

```python
class Solution(object):
    def prevPermOpt1(self, arr):
        """
        :type arr: List[int]
        :rtype: List[int]
        """

        p1 = len(arr) - 2
        while p1 >= 0 and arr[p1] <= arr[p1 + 1]:
            p1 -= 1
        
        if p1 < 0:
            return arr
        
        p2 = None
        for index in range(p1 + 1, len(arr)):
            if arr[index] >= arr[p1]:
                break
            
            if p2 is None or arr[p2] < arr[index]:
                p2 = index

        arr[p1], arr[p2] = arr[p2], arr[p1]

        return arr
```
