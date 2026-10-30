---
title: "LCP 39. 无人机方阵"
aliases: ["yiduobo的每日leetcode LCP39.无人机方阵"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/575697634"
zhihu_id: "575697634"
zhihu_title: "yiduobo的每日leetcode LCP39.无人机方阵"
question_id: "LCP 39"
question: "无人机方阵"
problem_url: "https://leetcode.cn/problems/0jQkd0/"
difficulty: "Easy"
created: "2022-10-21T00:20:36+08:00"
updated: "2022-10-21T00:20:36+08:00"
upvotes: 0
comments: 0
---

# LCP 39. 无人机方阵

> **[yiduobo的每日leetcode LCP39.无人机方阵](https://zhuanlan.zhihu.com/p/575697634) · 知乎 · 2022-10-21 · 赞同 0**
> 力扣：[LCP 39. 无人机方阵](https://leetcode.cn/problems/0jQkd0/) · Easy · 灵茶山艾府：[用哈希表统计差异](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP39.无人机方阵

[力扣](https://leetcode.cn/problems/0jQkd0/)

由于题目中的无人机可以任意调整位置，那么实际上问的就是两个矩阵中有多少个不一样的数字。那么只需遍历source矩阵，使用哈希表统计每个数字出现的次数，然后再遍历target矩阵，若当前遍历的数字在哈希表中出现的次数大于0，那么就将这个次数减去1，否则就将答案加上1。

最后附上python代码：

```python
class Solution(object):
    def minimumSwitchingTimes(self, source, target):
        """
        :type source: List[List[int]]
        :type target: List[List[int]]
        :rtype: int
        """

        cnt = {}
        n = len(source)
        m = len(source[0])
        for i in range(n):
            for j in range(m):
                cnt[source[i][j]] = cnt.get(source[i][j], 0) + 1
        
        res = 0
        for i in range(n):
            for j in range(m):
                if cnt.get(target[i][j], 0) > 0:
                    cnt[target[i][j]] -= 1
                else:
                    res += 1
        
        return res
```
