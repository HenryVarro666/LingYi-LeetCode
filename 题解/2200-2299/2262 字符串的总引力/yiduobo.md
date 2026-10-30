---
title: "2262. 字符串的总引力"
aliases: ["yiduobo的每日leetcode 2262.字符串的总引力"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/string", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/548218093"
zhihu_id: "548218093"
zhihu_title: "yiduobo的每日leetcode 2262.字符串的总引力"
question_id: "2262"
question: "字符串的总引力"
problem_url: "https://leetcode.cn/problems/total-appeal-of-a-string/"
difficulty: "Hard"
rating: 2033
created: "2022-07-31T14:43:51+08:00"
updated: "2022-07-31T14:43:51+08:00"
upvotes: 0
comments: 0
---

# 2262. 字符串的总引力

> **[yiduobo的每日leetcode 2262.字符串的总引力](https://zhuanlan.zhihu.com/p/548218093) · 知乎 · 2022-07-31 · 赞同 0**
> 力扣：[2262. 字符串的总引力](https://leetcode.cn/problems/total-appeal-of-a-string/) · Hard · 灵茶山艾府：[两种方法：贡献法 / 增量法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2262.字符串的总引力

[力扣](https://leetcode.cn/problems/total-appeal-of-a-string/)

题目中字符串的长度比较长，不能直接枚举所有子串来计算，只能考虑使用O(n)或者O(nlogn)的算法。通常来说，这个复杂度的算法只有贪心和动态规划，在这里跟贪心是没有关联的，因此考虑使用动态规划算法。

由于时间复杂度的限制，动态规划的状态表示应该是O(n)的。一般O(n)的状态有两种经典的状态表示法：

1、f[i]表示前i个字符形成的子串如何如何

2、f[i]表示以s[i]结尾的所有子串如何如何

在这里使用第二种状态表示是比较合适的。令f[i]表示以s[i]结尾的所有子串的总引力之和，那么对于f[i]，可以认为是在所有以s[i - 1]结尾的子串末尾再添加字符s[i]，另外还有一个单独的s[i]也可以认为是以s[i]结尾的子串。

在理想情况下，也就是在前面从来没出现过s[i]的情况下，s[i]可以为总共i + 1个以s[i]结尾的子串提供额度为1的引力，也就是说f[i]将在f[i - 1]的基础上额外提供i + 1的因此，即f[i] \= f[i - 1] + i + 1。

当然，上面描述的是理想情况，但是在s[0]到s[i - 1]之间可能已经出现过了s[i]。记s[0]到s[i - 1]之间最后一次出现s[i]的下标为p，那么对于起点在0到p之间的以s[i]为结尾的子串而言，s[i]将无法提供额度为1的引力，因此在这里就有f[i] \= f[i - 1] + i + 1 - (p - 0 + 1) \= f[i - 1] + i - p。

另外，为了可以高效地直到s[i]最后一次出现的位置，需要使用一个哈希表记录所有字符最后一次出现的位置。在更新完f[i]之后，还需要使用s[i]来更新哈希表。

一趟遍历，计算所有的f值之后累加就是最终答案了。另外注意到每一轮的f只与上一轮有关，因此可以使用变量迭代省去f的空间。

最后附上python代码：

```python
class Solution(object):
    def appealSum(self, s):
        """
        :type s: str
        :rtype: int
        """

        last_pos = {s[0] : 0}
        now = 1
        res = 1
        for index in range(1, len(s)):
            """
            if s[index] in last_pos:
                now += index - last_pos[s[index]]
            else:
                now += index + 1
            """

            now += index - last_pos.get(s[index], -1)
            res += now
            last_pos[s[index]] = index

        return res
```
