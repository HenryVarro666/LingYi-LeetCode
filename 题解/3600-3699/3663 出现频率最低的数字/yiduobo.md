---
title: "3663. 出现频率最低的数字"
aliases: ["yiduobo的每日leetcode 3663.出现频率最低的数字"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1950294967340732463"
zhihu_id: "1950294967340732463"
zhihu_title: "yiduobo的每日leetcode 3663.出现频率最低的数字"
question_id: "3663"
question: "出现频率最低的数字"
problem_url: "https://leetcode.cn/problems/find-the-least-frequent-digit/"
difficulty: "Easy"
created: "2025-09-16T22:36:11+08:00"
updated: "2025-09-16T22:36:27+08:00"
upvotes: 1
comments: 0
---

# 3663. 出现频率最低的数字

> **[yiduobo的每日leetcode 3663.出现频率最低的数字](https://zhuanlan.zhihu.com/p/1950294967340732463) · 知乎 · 2025-09-16 · 赞同 1**
> 力扣：[3663. 出现频率最低的数字](https://leetcode.cn/problems/find-the-least-frequent-digit/) · Easy · 灵茶山艾府：[统计每个数字的出现次数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3663.出现频率最低的数字

[3663. 出现频率最低的数字 - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-least-frequent-digit/description/)

题目给出一个整数n，要求找出其在十进制表示中出现频率最低的数字。若多个数字出现频率相同，则选择最小的那个数字。

通过模10除以10的方法分离出n的每一位数字，同时使用一个哈希表记录这些数字出现的次数。接下来对哈希表中出现的数字进行一趟遍历，选取其中频率最低且最小的数字作为最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def getLeastFrequentDigit(self, n):
        """
        :type n: int
        :rtype: int
        """

        cnt = {}
        while n:
            d = n % 10
            n //= 10
            cnt[d] = cnt.get(d, 0) + 1
        
        res = None
        for d in cnt:
            if res is None or cnt[d] < cnt[res] or (cnt[d] == cnt[res] and d < res):
                res = d
        return res
```
