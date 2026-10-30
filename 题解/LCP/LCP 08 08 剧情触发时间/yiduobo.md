---
title: "LCP 08. 剧情触发时间"
aliases: ["yiduobo的每日leetcode LCP08.剧情触发时间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/570676677"
zhihu_id: "570676677"
zhihu_title: "yiduobo的每日leetcode LCP08.剧情触发时间"
question_id: "LCP 08"
question: "剧情触发时间"
problem_url: "https://leetcode.cn/problems/ju-qing-hong-fa-shi-jian/"
created: "2022-10-05T03:39:50+08:00"
updated: "2022-10-05T03:39:50+08:00"
upvotes: 0
comments: 0
---

# LCP 08. 剧情触发时间

> **[yiduobo的每日leetcode LCP08.剧情触发时间](https://zhuanlan.zhihu.com/p/570676677) · 知乎 · 2022-10-05 · 赞同 0**
> 力扣：[LCP 08. 剧情触发时间](https://leetcode.cn/problems/ju-qing-hong-fa-shi-jian/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP08.剧情触发时间

[力扣](https://leetcode.cn/problems/ju-qing-hong-fa-shi-jian/)

首先，由于题目中给出的三种属性C、R、H互相之间不会产生影响，因此可以分开来考虑。对于第i个剧情的触发条件(c[i], r[i], h[i])，若其中某种属性值最终依然达不到要求，那么这个剧情就无法触发，否则可以分别计算出C、R、H三者达到要求的最早的天数，这三个天数中的最大值就是该剧情触发的时间。

接下来的问题就变成了给出某个属性值v，计算对应的属性在第几天大于等于v。注意到题目给出的increase数组中的值都非负，也就意味着C、R、H这三个属性值是随着日期单调不减的。于是可以先将每一天的属性值都计算出来，然后就可以通过二分查找解决对应属性值在第几天大于等于给出的v了。

最后附上python代码：

```python
class Solution(object):
    def getTriggerTime(self, increase, requirements):
        """
        :type increase: List[List[int]]
        :type requirements: List[List[int]]
        :rtype: List[int]
        """

        tot_r = [0]
        tot_c = [0]
        tot_h = [0]
        for inc in increase:
            tot_r.append(tot_r[-1] + inc[0])
            tot_c.append(tot_c[-1] + inc[1])
            tot_h.append(tot_h[-1] + inc[2])
        
        def search(f, v):
            if v > f[-1]:
                return -1
            l = 0
            r = len(f) - 1
            while l < r:
                mid = (l + r) / 2
                if f[mid] < v:
                    l = mid + 1
                else:
                    r = mid
            
            return l

        res = []
        for require in requirements:
            date_r = search(tot_r, require[0])
            date_c = search(tot_c, require[1])
            date_h = search(tot_h, require[2])
            if date_r < 0 or date_c < 0 or date_h < 0:
                res.append(-1)
            else:
                res.append(max(date_r, date_c, date_h))
                
        return res
```
