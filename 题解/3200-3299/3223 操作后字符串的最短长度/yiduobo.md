---
title: "3223. 操作后字符串的最短长度"
aliases: ["yiduobo的每日leetcode 3223.操作后字符串的最短长度"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/719638475"
zhihu_id: "719638475"
zhihu_title: "yiduobo的每日leetcode 3223.操作后字符串的最短长度"
question_id: "3223"
question: "操作后字符串的最短长度"
problem_url: "https://leetcode.cn/problems/minimum-length-of-string-after-operations/"
difficulty: "Medium"
created: "2024-09-12T00:03:05+08:00"
updated: "2024-09-12T00:03:05+08:00"
upvotes: 2
comments: 0
---

# 3223. 操作后字符串的最短长度

> **[yiduobo的每日leetcode 3223.操作后字符串的最短长度](https://zhuanlan.zhihu.com/p/719638475) · 知乎 · 2024-09-12 · 赞同 2**
> 力扣：[3223. 操作后字符串的最短长度](https://leetcode.cn/problems/minimum-length-of-string-after-operations/) · Medium · 灵茶山艾府：[统计字母出现次数+分奇偶讨论（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3223.操作后字符串的最短长度

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-length-of-string-after-operations/description/)

题目给出一个字符串，每一轮可以选择其中的某个字符s[i]，若s[i]左侧与右侧都存在与s[i]相同的字符，那么就可以删掉s[i]左侧与右侧离s[i]最近的那个相同字符。问最终可以得到的最短字符串的长度是多少。

注意到题目中的删除并不要求字符相邻，那么只要某个字符串的出现次数大于等于三次，那么就可以从中删去两个字符。更进一步的，若某种字符一开始出现了奇数次，那么这个字符最终必然会剩下一个，反之若一开始出现了偶数次，那么最终将剩下两个。

根据上面的结论，就可以先统计每种字符出现的次数，接下来一趟遍历，若当前字符出现的次数为奇数，那么就将答案加上1，否则将答案加上2。

最后附上python代码：

```python
class Solution(object):
    def minimumLength(self, s):
        """
        :type s: str
        :rtype: int
        """

        res = 0
        freq = Counter(s)
        for f in freq.values():
            if f % 2 == 1:
                res += 1
            else:
                res += 2
        
        return res
```
