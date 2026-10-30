---
title: "3506. 查找消除细菌菌株所需时间"
aliases: ["yiduobo的每日leetcode 3506.查找消除细菌菌株所需时间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1901796131744256013"
zhihu_id: "1901796131744256013"
zhihu_title: "yiduobo的每日leetcode 3506.查找消除细菌菌株所需时间"
question_id: "3506"
question: "查找消除细菌菌株所需时间"
problem_url: "https://leetcode.cn/problems/find-time-required-to-eliminate-bacterial-strains/"
created: "2025-05-03T01:04:44+08:00"
updated: "2025-05-03T01:04:44+08:00"
upvotes: 1
comments: 0
---

# 3506. 查找消除细菌菌株所需时间

> **[yiduobo的每日leetcode 3506.查找消除细菌菌株所需时间](https://zhuanlan.zhihu.com/p/1901796131744256013) · 知乎 · 2025-05-03 · 赞同 1**
> 力扣：[3506. 查找消除细菌菌株所需时间](https://leetcode.cn/problems/find-time-required-to-eliminate-bacterial-strains/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3506.查找消除细菌菌株所需时间

[3506. 查找消除细菌菌株所需时间 - 力扣（LeetCode）](https://leetcode.cn/problems/find-time-required-to-eliminate-bacterial-strains/description/)

题目给出一个整数数组timeReq以及一个整数splitTime。

初始情况下，只有一个白细胞。单个白细胞只能消除一个细菌，消除第index种细菌所需的时间为timeReq[index]。另外白细胞也可以选择进行分裂，分裂所需的时间为splitTime。多个白细胞可以并行操作，但是不能同时攻击同一个细菌。

问最少需要多少时间才能消除所有细菌。

首先可以明确的是，时间越充足，消除所有细菌的成功率就越高，因此在这里可以二分答案。二分的下界自然是timeReq中的最大值，而上界则是在这个基础上加上白细胞通过分裂使得数量大于等于timeReq长度所需的时间。

另一方面，白细胞的工作方式应该是按照

分裂->单个白细胞处理所需时间最长的细菌->分裂->单个白细胞处理所需时间最长的细菌->...

这个顺序来执行的。其中每轮分裂的次数可能是0次，也可能是多次。理由是分裂应该趁早执行，而为了保证在特定的时间内处理掉所有细菌，到了特定的时间就必须开始攻击当前所需时间最长的细菌。

那么对于当前二分到的mid，可以使用两个变量now和split_cnt分别表示当前白细胞的数量以及已经分裂的次数，now初始值为1，表示一开始唯一的白细胞，而split_cnt初始值自然为0。接下来对timeReq从大到小进行排序，然后一趟遍历。对于当前遍历到的时间t，需要从mid中预留出时间t来吞噬这个细菌，另外此前已经执行过split_cnt次分裂，消耗了split_cnt \* splitTime的时间，因此剩余的事件r为mid - t - split_cnt \* splitTime。若这个r足够大，那么就可以继续执行分裂，具体来说，就是当r大于等于splitTime时，可以将now翻倍，然后将r减去splitTime，同时将已分裂的次数split_cnt加上1。

若某一时刻now大于等于剩余为吞噬的细菌数量，那么说明mid足够大，此时应该调整二分上界为mid；反之，若某一时刻now为0，说明mid不够大，此时应该调整二分下界为mid + 1。

最后附上python代码：

```python
class Solution(object):
    def minEliminationTime(self, timeReq, splitTime):
        """
        :type timeReq: List[int]
        :type splitTime: int
        :rtype: int
        """
        
        n = len(timeReq)
        now = 1
        t = 0
        while now < n:
            now += now
            t += splitTime

        timeReq.sort(reverse=True)
        left = timeReq[0]
        right = t + left
        while left < right:
            mid = (left + right) // 2
            now = 1
            flag = True
            split_cnt = 0
            for index, t in enumerate(timeReq):
                r = mid - t - split_cnt * splitTime
                while r >= splitTime and now < n - index:
                    now += now
                    r -= splitTime
                    split_cnt += 1

                if now >= n - index:
                    break
                
                if now == 0:
                    flag = False
                    break
                
                now -= 1
            
            if flag:
                right = mid
            else:
                left = mid + 1
        
        return left
```
