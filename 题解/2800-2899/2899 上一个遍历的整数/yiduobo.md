---
title: "2899. 上一个遍历的整数"
aliases: ["yiduobo的每日leetcode 2899.上一个遍历的整数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/663387975"
zhihu_id: "663387975"
zhihu_title: "yiduobo的每日leetcode 2899.上一个遍历的整数"
question_id: "2899"
question: "上一个遍历的整数"
problem_url: "https://leetcode.cn/problems/last-visited-integers/"
difficulty: "Easy"
created: "2023-10-26T03:16:13+08:00"
updated: "2023-10-26T03:16:13+08:00"
upvotes: 0
comments: 0
---

# 2899. 上一个遍历的整数

> **[yiduobo的每日leetcode 2899.上一个遍历的整数](https://zhuanlan.zhihu.com/p/663387975) · 知乎 · 2023-10-26 · 赞同 0**
> 力扣：[2899. 上一个遍历的整数](https://leetcode.cn/problems/last-visited-integers/) · Easy · 灵茶山艾府：[按题意模拟即可（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2899.上一个遍历的整数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/last-visited-integers/)

直接按照题目的意思进行模拟。

一趟遍历，使用数组nums记录过程中需要记录的数字，并使用一个变量k记录当前连续出现的prev的次数。

若当前遍历到的是prev，那么就将k加上1，若此时的k大于nums的长度，那么将-1添加到答案中，否则将nums中倒数第k个数添加到答案中。

反之若不是prev，那么就将当前遍历到的数添加到nums中，并将k置为0。

最后附上python代码：

```python
class Solution(object):
    def lastVisitedIntegers(self, words):
        """
        :type words: List[str]
        :rtype: List[int]
        """

        nums = []
        k = 0
        res = []
        for w in words:
            if w[0] == 'p':
                k += 1
                if k > len(nums):
                    res.append(-1)
                else:
                    res.append(nums[-k])
            
            else:
                nums.append(int(w))
                k = 0
        
        return res
```
