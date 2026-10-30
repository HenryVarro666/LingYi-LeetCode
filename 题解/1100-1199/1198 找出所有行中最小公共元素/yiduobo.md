---
title: "1198. 找出所有行中最小公共元素"
aliases: ["yiduobo的每日leetcode 1198.找出所有行中最小公共元素"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/612767260"
zhihu_id: "612767260"
zhihu_title: "yiduobo的每日leetcode 1198.找出所有行中最小公共元素"
question_id: "1198"
question: "找出所有行中最小公共元素"
problem_url: "https://leetcode.cn/problems/find-smallest-common-element-in-all-rows/"
created: "2023-03-10T02:25:53+08:00"
updated: "2023-03-10T02:25:53+08:00"
upvotes: 0
comments: 0
---

# 1198. 找出所有行中最小公共元素

> **[yiduobo的每日leetcode 1198.找出所有行中最小公共元素](https://zhuanlan.zhihu.com/p/612767260) · 知乎 · 2023-03-10 · 赞同 0**
> 力扣：[1198. 找出所有行中最小公共元素](https://leetcode.cn/problems/find-smallest-common-element-in-all-rows/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1198.找出所有行中最小公共元素

[力扣](https://leetcode.cn/problems/find-smallest-common-element-in-all-rows/)

如果存在题目中要求的这个元素，那么其必然存在于第0行中，那么可以从左向右枚举第0行中的数，检测这个数是否存在于其他行中。

由于每一行都是排好序的，那么随着第0行中的数越来越大，其如果出现在其他行中，那么出现的下标也必然越来越靠后，于是可以使用一个数组p记录其他行中当前检测到下标，接下来就只需要随着枚举的数的增大逐行调整其对应的p的位置。

最后附上python代码：

```python
class Solution(object):
    def smallestCommonElement(self, mat):
        """
        :type mat: List[List[int]]
        :rtype: int
        """

        m = len(mat)
        n = len(mat[0])

        p = [0] * m

        for num in mat[0]:
            flag = True

            for i in range(1, m):
                while p[i] < n and mat[i][p[i]] < num:
                    p[i] += 1
                
                if p[i] == n:
                    return -1
                
                if mat[i][p[i]] != num:
                    flag = False
            
            if flag:
                return num
        
        return -1
```
