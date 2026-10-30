---
title: "1552. 两球之间的磁力"
aliases: ["yiduobo的每日leetcode 1552.两球之间的磁力"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/binary-search", "leetcode/sorting", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/426119858"
zhihu_id: "426119858"
zhihu_title: "yiduobo的每日leetcode 1552.两球之间的磁力"
question_id: "1552"
question: "两球之间的磁力"
problem_url: "https://leetcode.cn/problems/magnetic-force-between-two-balls/"
difficulty: "Medium"
rating: 2517
created: "2021-10-26T23:47:51+08:00"
updated: "2021-10-26T23:47:51+08:00"
upvotes: 0
comments: 0
---

# 1552. 两球之间的磁力

> **[yiduobo的每日leetcode 1552.两球之间的磁力](https://zhuanlan.zhihu.com/p/426119858) · 知乎 · 2021-10-26 · 赞同 0**
> 力扣：[1552. 两球之间的磁力](https://leetcode.cn/problems/magnetic-force-between-two-balls/) · Medium · 灵茶山艾府：[二分答案（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1552.两球之间的磁力

[力扣](https://leetcode-cn.com/problems/magnetic-force-between-two-balls/)

首先，当最终答案越大时，安排方案的难度显然是越高的，因此可以二分最终的答案。二分的下界自然为1，上界可以认为是两个边界上篮子的距离。

接下来，对于当前二分到的答案mid，需要想办法确定能否给出一种所有球最小间隔大于等于mid的方案。很明显，此时应该尽可能将边界上的篮子利用起来，于是可以从小到大一趟排序，然后从头开始尽可能尽凑地进行安排。若最终可以安排放置m个球，说明最终答案大于等于mid，此时应该更新左边界，否则更新右边界。

最后附上python代码：

```python
class Solution(object):
    def maxDistance(self, position, m):
        """
        :type position: List[int]
        :type m: int
        :rtype: int
        """

        position = sorted(position)
        l = 1
        r = position[-1] - position[0]
        n = len(position)
        while l < r:
            mid = (l + r + 1) >> 1
            cnt = 1
            now = 0
            next = 1

            while cnt < m:
                while next < n and position[next] - position[now] < mid:
                    next += 1
                if next == n:
                    break
            
                cnt += 1
                now = next
                next += 1

            if cnt == m:
                l = mid
            else:
                r = mid - 1
        
        return l
```
