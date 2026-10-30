---
title: "2237. 计算街道上满足所需亮度的位置数量"
aliases: ["yiduobo的每日leetcode 2237.计算街道上满足所需亮度的位置数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/628455603"
zhihu_id: "628455603"
zhihu_title: "yiduobo的每日leetcode 2237.计算街道上满足所需亮度的位置数量"
question_id: "2237"
question: "计算街道上满足所需亮度的位置数量"
problem_url: "https://leetcode.cn/problems/count-positions-on-street-with-required-brightness/"
created: "2023-05-11T04:07:37+08:00"
updated: "2023-05-11T04:07:37+08:00"
upvotes: 0
comments: 0
---

# 2237. 计算街道上满足所需亮度的位置数量

> **[yiduobo的每日leetcode 2237.计算街道上满足所需亮度的位置数量](https://zhuanlan.zhihu.com/p/628455603) · 知乎 · 2023-05-11 · 赞同 0**
> 力扣：[2237. 计算街道上满足所需亮度的位置数量](https://leetcode.cn/problems/count-positions-on-street-with-required-brightness/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2237.计算街道上满足所需亮度的位置数量

[力扣](https://leetcode.cn/problems/count-positions-on-street-with-required-brightness/)

又是经典的开灯问题，处理方法依然是差分数组。对于每盏灯[position, range]，相当于在数组上[position - range，position + range]这个区间上都加上1，也就是相当于将差分数组的position - range位置加上1，position + range + 1位置减去1。

接下来则只需要遍历整个差分数组，求解前缀和并与对应的request比较大小即可。

另外需要特别注意本题的街道有边界，因此在计算照亮区间时需要注意不要越界。

最后附上python代码：

```python
class Solution(object):
    def meetRequirement(self, n, lights, requirement):
        """
        :type n: int
        :type lights: List[List[int]]
        :type requirement: List[int]
        :rtype: int
        """

        f = [0] * (n + 1)
        for pos, rng in lights:
            f[max(0, pos - rng)] += 1
            f[min(n - 1, pos + rng) + 1] -= 1

        now = 0
        res = 0
        for index in range(n):
            now += f[index]
            if now >= requirement[index]:
                res += 1
        
        return res
```
