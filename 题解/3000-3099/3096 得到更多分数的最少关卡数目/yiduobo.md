---
title: "3096. 得到更多分数的最少关卡数目"
aliases: ["yiduobo的每日leetcode 3096.得到更多分数的最少关卡数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration", "leetcode/prefix-sum"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/699729704"
zhihu_id: "699729704"
zhihu_title: "yiduobo的每日leetcode 3096.得到更多分数的最少关卡数目"
question_id: "3096"
question: "得到更多分数的最少关卡数目"
problem_url: "https://leetcode.cn/problems/minimum-levels-to-gain-more-points/"
difficulty: "Medium"
created: "2024-05-25T00:52:19+08:00"
updated: "2024-05-25T00:52:19+08:00"
upvotes: 1
comments: 0
---

# 3096. 得到更多分数的最少关卡数目

> **[yiduobo的每日leetcode 3096.得到更多分数的最少关卡数目](https://zhuanlan.zhihu.com/p/699729704) · 知乎 · 2024-05-25 · 赞同 1**
> 力扣：[3096. 得到更多分数的最少关卡数目](https://leetcode.cn/problems/minimum-levels-to-gain-more-points/) · Medium · 灵茶山艾府：[前后缀分解（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3096.得到更多分数的最少关卡数目

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-levels-to-gain-more-points/description/)

题目中给出n个关卡，有简单和困难两种类型。每通过一个简单关卡可以得一分，通过一个困难关卡需要扣掉一分，需要找出一个最短的关卡前缀使得这个前缀的总得分比其他关卡的总得分更多。

由于关卡的总得分是固定的，不妨设简单关卡一共有x个，那么困难关卡就是n - x个，因此通过所有关卡的分数之和就是x + x - n。接下来只需一趟遍历，计算通过当前前缀关卡的得分now，若now大于x + x - n - now，那么当前通过的关卡数即为答案，若不存在这样的关卡，则返回-1。

最后附上python代码：

```python
class Solution(object):
    def minimumLevels(self, possible):
        """
        :type possible: List[int]
        :rtype: int
        """

        tot = sum(possible) * 2 - len(possible)
        now = 0
        for index in range(len(possible) - 1):
            if possible[index] == 1:
                now += 1
            else:
                now -= 1
            
            if now > tot - now:
                return index + 1
        
        return -1
```
