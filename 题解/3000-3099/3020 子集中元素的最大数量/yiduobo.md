---
title: "3020. 子集中元素的最大数量"
aliases: ["yiduobo的每日leetcode 3020.子集中元素的最大数量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/enumeration", "leetcode/bao-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/694599866"
zhihu_id: "694599866"
zhihu_title: "yiduobo的每日leetcode 3020.子集中元素的最大数量"
question_id: "3020"
question: "子集中元素的最大数量"
problem_url: "https://leetcode.cn/problems/find-the-maximum-number-of-elements-in-subset/"
difficulty: "Medium"
created: "2024-04-26T01:55:41+08:00"
updated: "2024-04-26T01:55:41+08:00"
upvotes: 1
comments: 0
---

# 3020. 子集中元素的最大数量

> **[yiduobo的每日leetcode 3020.子集中元素的最大数量](https://zhuanlan.zhihu.com/p/694599866) · 知乎 · 2024-04-26 · 赞同 1**
> 力扣：[3020. 子集中元素的最大数量](https://leetcode.cn/problems/find-the-maximum-number-of-elements-in-subset/) · Medium · 灵茶山艾府：[暴力枚举，简洁写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3020.子集中元素的最大数量

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-maximum-number-of-elements-in-subset/description/)

由于题目构成集合需要知道特定的数出现的次数，因此在这里就可以先使用哈希表统计每个数出现的次数。

接下来对于x \= 1这种特殊情况，由于x^2, x^4, ..., x^k都还是1，因此当1出现了奇数次时，这些1可以全部加入到集合中，反之当1出现了偶数次时，则需要去掉一个。

最后对于x > 1的情况，因为是计算自身的乘方，因此增长的速度是非常快的，因此完全可以暴力枚举所有的x，然后检测x是否至少出现了两次同时x^2至少出现了一次，如果满足，就将x更新为x^2然后继续检测。每通过一轮的检测，都会多出两个数加入到答案中，因此构成的集合大小就是检测的轮次乘以2再减去1。

最后附上python代码：

```python
class Solution(object):
    def maximumLength(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 1
        freq = Counter(nums)
        for v in freq:
            if v == 1:
                if freq[v] % 2 == 0:
                    res = max(res, freq[v] - 1)
                else:
                    res = max(res, freq[v])
                    
                continue
            
            x = v
            y = x * x
            step = 1
            while freq[x] >= 2 and freq[y] >= 1:
                step += 1
                x, y = y, y * y
            
            res = max(res, step * 2 - 1)

        return res
```
