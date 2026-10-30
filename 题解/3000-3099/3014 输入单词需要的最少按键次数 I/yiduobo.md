---
title: "3014. 输入单词需要的最少按键次数I & 3016. 输入单词需要的最少按键次数II"
aliases: ["yiduobo的每日leetcode 3014.输入单词需要的最少按键次数I && 3016.输入单词需要的最少按键次数II", "3014. 输入单词需要的最少按键次数I", "3016. 输入单词需要的最少按键次数II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/694185298"
zhihu_id: "694185298"
zhihu_title: "yiduobo的每日leetcode 3014.输入单词需要的最少按键次数I && 3016.输入单词需要的最少按键次数II"
question_id: ["3014", "3016"]
question: ["输入单词需要的最少按键次数 I", "输入单词需要的最少按键次数 II"]
problem_url: ["https://leetcode.cn/problems/minimum-number-of-pushes-to-type-word-i/", "https://leetcode.cn/problems/minimum-number-of-pushes-to-type-word-ii/"]
difficulty: ["Easy", "Medium"]
rating: 1534
created: "2024-04-24T02:23:38+08:00"
updated: "2024-04-24T02:23:40+08:00"
upvotes: 2
comments: 0
---

# 3014. 输入单词需要的最少按键次数I & 3016. 输入单词需要的最少按键次数II

> **[yiduobo的每日leetcode 3014.输入单词需要的最少按键次数I && 3016.输入单词需要的最少按键次数II](https://zhuanlan.zhihu.com/p/694185298) · 知乎 · 2024-04-24 · 赞同 2**
> 力扣：[3014. 输入单词需要的最少按键次数 I](https://leetcode.cn/problems/minimum-number-of-pushes-to-type-word-i/) · Easy · 灵茶山艾府：[O(1) 数学公式（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[3016. 输入单词需要的最少按键次数 II](https://leetcode.cn/problems/minimum-number-of-pushes-to-type-word-ii/) · Medium · 灵茶山艾府：[根据排序不等式贪心，简洁写法（Python/Java/C++/Go）](../3016%20输入单词需要的最少按键次数%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3014.输入单词需要的最少按键次数I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-number-of-pushes-to-type-word-i/description/)

3016.输入单词需要的最少按键次数II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-number-of-pushes-to-type-word-ii/description/)

两题的题设基本一样，第二题的数据规模大很多且出现的字母可能重复。

为了使得按键次数最少，就应该让频率高的字符尽量靠前。于是只需统计每种字符出现的次数，然后从大到小排列，将排名在0-7的字符映射在2-9的第一个字符上，第8-15的字符映射在2-9的第二个字符上，第16-23的字符映射在2-9的第三个字符上，剩下的则映射在第四个字符。

具体实现上，并不需要真的进行映射，只需计算当前字符出现的次数与映射位置所需的按键数的乘积，然后累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def minimumPushes(self, word):
        """
        :type word: str
        :rtype: int
        """

        freq = Counter(word)
        res = 0
        for index, f in enumerate(sorted(freq.values(), reverse=True)):
            if index < 8:
                res += f
            elif index < 16:
                res += f * 2
            elif index < 24:
                res += f * 3
            else:
                res += f * 4
        
        return res
```
