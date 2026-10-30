---
title: "354. 俄罗斯套娃信封问题"
aliases: ["yiduobo的每日leetcode 354.俄罗斯套娃信封问题"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-search", "leetcode/dynamic-programming", "leetcode/sorting", "题单/动态规划", "题单/动态规划/四-经典线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/163792446"
zhihu_id: "163792446"
zhihu_title: "yiduobo的每日leetcode 354.俄罗斯套娃信封问题"
question_id: "354"
question: "俄罗斯套娃信封问题"
problem_url: "https://leetcode.cn/problems/russian-doll-envelopes/"
difficulty: "Hard"
created: "2020-07-26T15:06:15+08:00"
updated: "2020-07-26T15:06:15+08:00"
upvotes: 1
comments: 0
---

# 354. 俄罗斯套娃信封问题

> **[yiduobo的每日leetcode 354.俄罗斯套娃信封问题](https://zhuanlan.zhihu.com/p/163792446) · 知乎 · 2020-07-26 · 赞同 1**
> 力扣：[354. 俄罗斯套娃信封问题](https://leetcode.cn/problems/russian-doll-envelopes/) · Hard · 灵茶山艾府：[巧妙排序，转化成一维 LIS 问题（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

354.俄罗斯套娃信封问题<https://leetcode-cn.com/problems/russian-doll-envelopes/>

注意到这里不需要满足原始序列中的先后顺序，因此我们可以先按w进行排序，然后问题就转化成了在h上的最长上升子序列问题。不过需要注意的是，对于w相同的情况是不能选取两个的，因此在排序时可以将w相同的信封按h逆序排好，这样一来就可以避免因为h的原因选取到两封相同w信封的情况了。

排序和最长上升子序列的复杂度都是O(nlogn)，因此最终的时间复杂度就是O(nlogn)。

最后附上python代码：

```python
class Solution(object):
    def maxEnvelopes(self, envelopes):
        """
        :type envelopes: List[List[int]]
        :rtype: int
        """

        sorted_envelopes = [x[1] for x in sorted(envelopes, key=lambda d:(d[0], -d[1]))]
        res = []
        for height in sorted_envelopes:
            if not res or height > res[-1]:
                res.append(height)
            else:
                l = 0
                r = len(res) - 1
                while l < r:
                    mid = (l + r) / 2
                    if res[mid] < height:
                        l = mid + 1
                    else:
                        r = mid

                res[r] = height

        return len(res)
```
