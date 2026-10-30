---
title: "1011. 在D天内送达包裹的能力"
aliases: ["yiduobo的每日leetcode 1011.在D天内送达包裹的能力"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/367334077"
zhihu_id: "367334077"
zhihu_title: "yiduobo的每日leetcode 1011.在D天内送达包裹的能力"
question_id: "1011"
question: "在D天内送达包裹的能力"
problem_url: "https://leetcode.cn/problems/capacity-to-ship-packages-within-d-days/"
created: "2021-04-23T21:20:13+08:00"
updated: "2021-04-23T21:20:13+08:00"
upvotes: 0
comments: 0
---

# 1011. 在D天内送达包裹的能力

> **[yiduobo的每日leetcode 1011.在D天内送达包裹的能力](https://zhuanlan.zhihu.com/p/367334077) · 知乎 · 2021-04-23 · 赞同 0**
> 力扣：[1011. 在D天内送达包裹的能力](https://leetcode.cn/problems/capacity-to-ship-packages-within-d-days/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

1011.在D天内送达包裹的能力

[力扣](https://leetcode-cn.com/problems/capacity-to-ship-packages-within-d-days/)

首先可以明确的一点是，虽然每批次运载能力的提升，所需的天数必然是单调不增的，因此我们可以二分这个运载能力，然后判断是否能在D天内运完。

为了在D天内完成搬运，那么运力的下限就是min_w \= sum(weight) / D，而上限则是max_w \= sum(weight)，我们接下来就可以在min_w和max_w之间二分答案。

设当前二分到的运力为w，由于这里没有调度这一说，那么我们就应该每一批次都尽可能地上船，于是现在就变成了weight的某个区间之后是否小于等于w的问题。区间和问题的经典处理方法是前缀和，而前缀和是单调递增的，也就是说我们在这里又可以在前缀和数组prefix中二分。假设我们上一轮次运输到了weight[now]，那么我们这次就需要在前缀和数组中找到pos，其满足prefix[pos] - prefix[now] \<\= w，且prefix[pos + 1] - prefix[now] > w，也就是使用w + prefix[now]在now + 1到len(weight) -1 之间进行二分。

于是现在的做法就是先预处理出前缀和数组prefix，并求解二分答案的上下限min_w和max_w，然后开始二分w。对于当前的w，在prefix再次使用二分求解需要多少天才能完成运输，并根据这个天数与D的大小来调整w的上下限。

最后附上python代码：

```python
class Solution(object):
    def shipWithinDays(self, weights, D):
        """
        :type weights: List[int]
        :type D: int
        :rtype: int
        """

        s = [weights[0]]
        for num in weights[1:]:
            s.append(s[-1] + num)
        
        min_w = s[0]
        max_w = s[-1]
        while min_w < max_w:
            w = (max_w + min_w) >> 1
            now = -1
            step = 0
            offset = 0
            while now < len(weights):
                step += 1
                l = now + 1
                r = len(weights) - 1
                next = None
                if w >= s[r] - offset:
                    now = r
                    break
                while l <= r:
                    mid = (l + r) >> 1
                    if w >= s[mid] - offset:
                        next = mid
                        l = mid + 1
                    else:
                        r = mid - 1
                
                if next is None:
                    break

                now = next
                offset = s[now]

                
            
            if now < len(weights) - 1 or step > D:
                min_w = w + 1
            else:
                max_w = w
            
        return min_w
```
