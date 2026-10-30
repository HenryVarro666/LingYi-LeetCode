---
title: "3442. 奇偶频次间的最大差值I"
aliases: ["yiduobo的每日leetcode 3442.奇偶频次间的最大差值I"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1891940931588039871"
zhihu_id: "1891940931588039871"
zhihu_title: "yiduobo的每日leetcode 3442.奇偶频次间的最大差值I"
question_id: "3442"
question: "奇偶频次间的最大差值 I"
problem_url: "https://leetcode.cn/problems/maximum-difference-between-even-and-odd-frequency-i/"
difficulty: "Easy"
created: "2025-04-05T19:57:05+08:00"
updated: "2025-04-05T19:57:05+08:00"
upvotes: 1
comments: 0
---

# 3442. 奇偶频次间的最大差值I

> **[yiduobo的每日leetcode 3442.奇偶频次间的最大差值I](https://zhuanlan.zhihu.com/p/1891940931588039871) · 知乎 · 2025-04-05 · 赞同 1**
> 力扣：[3442. 奇偶频次间的最大差值 I](https://leetcode.cn/problems/maximum-difference-between-even-and-odd-frequency-i/) · Easy · 灵茶山艾府：[统计每种字母的出现次数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3442.奇偶频次间的最大差值I

[3442. 奇偶频次间的最大差值 I - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-difference-between-even-and-odd-frequency-i/description/)

题目给出一个由小写字符组成的字符串s，要求从中找出一个出现奇数次的字符a以及一个出现偶数次的字符b，使得这个a的出现次数减去b的出现次数尽可能大。题目保证字符串中至少存在一个出现奇数次的字符以及一个出现偶数次的字符。

为了使得差值最大，那么就应该取出现次数为奇数中次数最多的字符作为a，同时取出现次数为偶数中次数最少的字符作为b，于是可以先一趟遍历，使用哈希表cnt统计每种字符串出现的次数，然后再遍历哈希表中的每种字符，找出对应的a和b以及a和b出现的次数，二者相减即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxDifference(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        cnt = {}
        for char in s:
            cnt[char] = cnt.get(char, 0) + 1
        
        max_odd = None
        min_even = None
        for char in cnt:
            if cnt[char] % 2 == 1:
                if max_odd is None or max_odd < cnt[char]:
                    max_odd = cnt[char]
            else:
                if min_even is None or min_even > cnt[char]:
                    min_even = cnt[char]
        
        return max_odd - min_even
```
