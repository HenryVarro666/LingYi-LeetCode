---
title: "1885. 统计数对"
aliases: ["yiduobo的每日leetcode 1885.统计数对"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/622709582"
zhihu_id: "622709582"
zhihu_title: "yiduobo的每日leetcode 1885.统计数对"
question_id: "1885"
question: "统计数对"
problem_url: "https://leetcode.cn/problems/count-pairs-in-two-arrays/"
created: "2023-04-18T01:21:59+08:00"
updated: "2023-04-18T01:21:59+08:00"
upvotes: 0
comments: 0
---

# 1885. 统计数对

> **[yiduobo的每日leetcode 1885.统计数对](https://zhuanlan.zhihu.com/p/622709582) · 知乎 · 2023-04-18 · 赞同 0**
> 力扣：[1885. 统计数对](https://leetcode.cn/problems/count-pairs-in-two-arrays/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1885.统计数对

[力扣](https://leetcode.cn/problems/count-pairs-in-two-arrays/)

题目中数对的计算方法是nums1[i] + nums1[j] > nums2[i] + nums2[j]，移项后就是(nums1[i] - nums2[i]) + (nums1[j] - nums2[j]) > 0，那么就可以预处理出一个数组d，其中d[i] \= nums1[i] - nums2[i]，此时的问题就变成了给出一个数组d，找出所有满足d[i] + d[j] > 0且i \< j的数对，其中-99999 \<\= d[i] \<\= 99999。

对于这个问题，可以从后向前遍历数组d，对于当前的d[i]，使用某种数据结构找出i + 1到n - 1之间大于等于d[j] >\= -d[i]的数的个数。

我在这里采用的做法是想将每个d[i]都加上100000，那么d[i]的取值范围就变成了1 \<\= d[i] \<\= 199999，而问题则转化成了对于每个i找出i右侧所有满足d[i] + d[j] > 200000的j的数量，也就是满足d[j] > 200000 - d[i]的j的数量，而这个数量则可以通过i右侧的数的总数n - i - 1再减去i右侧所有满足d[j] \<\= 200000 - d[i]的j的数量。到了这一步，就可以直接套用树状数组来进行求解了。

最后附上python代码：

```python
class Solution(object):
    def countPairs(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        n = len(nums1)
        d = [nums1[index] - nums2[index] + 100000 for index in range(n)]
        res = 0

        f = [0] * 200000

        def get(x):
            s = 0
            while x > 0:
                s += f[x]
                x -= x & -x
            return s
        
        def add(x):
            while x < 200000:
                f[x] += 1
                x += x & -x

        for index in range(n - 1, -1, -1):
            res += (n - index - 1) - get(200000 - d[index])
            add(d[index])
        
        return res
```
