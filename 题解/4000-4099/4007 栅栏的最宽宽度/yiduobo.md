---
title: "4007. 栅栏的最宽宽度"
aliases: ["yiduobo的每日leetcode 4007.栅栏的最宽宽度"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/enumeration"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2068105576907903122"
zhihu_id: "2068105576907903122"
zhihu_title: "yiduobo的每日leetcode 4007.栅栏的最宽宽度"
question_id: "4007"
question: "栅栏的最宽宽度"
problem_url: "https://leetcode.cn/problems/widest-possible-fence/"
difficulty: "Hard"
created: "2026-08-04T22:53:12+08:00"
updated: "2026-08-04T22:53:13+08:00"
upvotes: 0
comments: 0
---

# 4007. 栅栏的最宽宽度

> **[yiduobo的每日leetcode 4007.栅栏的最宽宽度](https://zhuanlan.zhihu.com/p/2068105576907903122) · 知乎 · 2026-08-04 · 赞同 0**
> 力扣：[4007. 栅栏的最宽宽度](https://leetcode.cn/problems/widest-possible-fence/) · Hard · 灵茶山艾府：[枚举 + 两个哈希表（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4007.栅栏的最宽宽度

<https://leetcode.cn/problems/widest-possible-fence/>

题目给出一个整数数组planks，其中planks[index]表示第index块木板的高度。每块木板的宽度为1。

现在要求使用木板制造一个栅栏，其中的木板必须具有相同的高度。

可以直接使用原本的木板，也可以将两块不同的原始木板拼接成一块新木板，其高度等于这两块木板的高度之和。需要注意，在这里不允许将三块或以上的木板拼接在一起。

每块原始木板只能使用一次，且不需要用完所有的原始木板。问可以构造的栅栏的最大宽度。

题目中栅栏的最终高度要么恰好等于某块原始木板的高度，要么等于两块原始木板高度之和，那么在这里就可以分别计算单独使用以及拼接使用得到的每种高度的数目，然后取这两项之和最大的高度作为最终高度。

具体来说，可以先使用一个哈希表记录每种单独木板高度出现的次数，接下来两两遍历这些高度的组合计算拼接得到的木板数量。若这个高度组合相同，那么可以拼接得到的木板数量就是总量除以2向下取整；若高度组合不同，那么为了防止重复，可以限定第一种的高度小于第二种的高度，然后拼接得到的木板数量就是这两种木板数量中的较小值。

最后附上python代码：

```python
class Solution(object):
    def maximumWidth(self, planks):
        """
        :type planks: List[int]
        :rtype: int
        """
        
        single = {}
        for v in planks:
            single[v] = single.get(v, 0) + 1
        
        pair = {}
        for first in single.keys():
            for second in single.keys():
                if first > second:
                    continue
                
                s = first + second
                if first == second:
                    pair[s] = pair.get(s, 0) + single[first] // 2
                else:
                    pair[s] = pair.get(s, 0) + min(single[first], single[second])
        

        res = 0
        for final in single:
            res = max(res, single[final] + pair.get(final, 0))
        for final in pair:
            res = max(res, pair[final] + single.get(final, 0))
        
        return res
```
