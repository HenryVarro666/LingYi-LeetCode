---
title: "646. 最长数对链"
aliases: ["yiduobo的每日leetcode 646.最长数对链"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/二-区间贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/274873768"
zhihu_id: "274873768"
zhihu_title: "yiduobo的每日leetcode 646.最长数对链"
question_id: "646"
question: "最长数对链"
problem_url: "https://leetcode.cn/problems/maximum-length-of-pair-chain/"
difficulty: "Medium"
created: "2020-11-05T22:32:19+08:00"
updated: "2020-11-05T22:32:19+08:00"
upvotes: 0
comments: 0
---

# 646. 最长数对链

> **[yiduobo的每日leetcode 646.最长数对链](https://zhuanlan.zhihu.com/p/274873768) · 知乎 · 2020-11-05 · 赞同 0**
> 力扣：[646. 最长数对链](https://leetcode.cn/problems/maximum-length-of-pair-chain/) · Medium · 灵茶山艾府：[贪心+证明（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

646.最长数对链

[力扣](https://leetcode-cn.com/problems/maximum-length-of-pair-chain/)

题目虽然写作最长数对链，但实际上是标准的区间问题。这里要求的是最多能选出多少个不相交的区间。

由于这里的区间权重是一致的，因此对于两个相交的区间，我们应当选择右边界较小的那一个，这样的话可以留出更多选择的空间给后面的区间。于是我们按区间的右边界从小到大进行排序，然后一趟扫描遍历每个区间。若当前区间的左边界大于答案的右边界，那么将当前区间加入到答案当中。

最后附上python代码：

```python
class Solution(object):
    def findLongestChain(self, pairs):
        """
        :type pairs: List[List[int]]
        :rtype: int
        """

        now = None
        res = 0
        for pair in sorted(pairs, key=lambda d:d[1]):
            if now is None or now < pair[0]:
                now = pair[1]
                res += 1
        
        return res
```
