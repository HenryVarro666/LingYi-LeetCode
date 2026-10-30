---
title: "2938. 区分黑球和白球"
aliases: ["yiduobo的每日leetcode 2938.区分黑球和白球"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/690999027"
zhihu_id: "690999027"
zhihu_title: "yiduobo的每日leetcode 2938.区分黑球和白球"
question_id: "2938"
question: "区分黑球与白球"
problem_url: "https://leetcode.cn/problems/separate-black-and-white-balls/"
difficulty: "Medium"
created: "2024-04-07T01:12:29+08:00"
updated: "2024-04-07T01:12:29+08:00"
upvotes: 1
comments: 0
---

# 2938. 区分黑球和白球

> **[yiduobo的每日leetcode 2938.区分黑球和白球](https://zhuanlan.zhihu.com/p/690999027) · 知乎 · 2024-04-07 · 赞同 1**
> 力扣：[2938. 区分黑球与白球](https://leetcode.cn/problems/separate-black-and-white-balls/) · Medium · 灵茶山艾府：[累加每个 0 左边的 1 的个数（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2938.区分黑球和白球

[. - 力扣（LeetCode）](https://leetcode.cn/problems/separate-black-and-white-balls/description/)

题目要求通过交换相邻的球将所有白球都集中到左侧，那么一个直观的想法就是将当前最左侧的球交换到答案的最左侧，将当前第二靠左的球交换到答案的第二靠左的位置，依次类推。可以简单认为如果打破了这个顺序，那么必然会出现两个白球进行交换的情况，这种情况在最优解中明显是不会产生的。

于是可以使用一个变量t记录下一个白球的目标位置，然后一趟遍历。对于当前遍历到的下标为index的球，若其为白球，那么就需要将其移动到下标为t的位置，代价为index - t。此时应该将其累加到答案，将t加上1，然后继续考虑剩下的球。

最后附上python代码：

```python
class Solution(object):
    def minimumSteps(self, s):
        """
        :type s: str
        :rtype: int
        """

        res = 0
        t = 0
        for index in range(len(s)):
            if s[index] == '0':
                res += index - t
                t += 1
        
        return res
```
