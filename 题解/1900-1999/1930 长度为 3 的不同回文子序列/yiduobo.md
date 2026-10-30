---
title: "1930. 长度为3的不同回文子序列"
aliases: ["yiduobo的每日leetcode 1930.长度为3的不同回文子序列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/enumeration", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/零-常用枚举技巧", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/487726566"
zhihu_id: "487726566"
zhihu_title: "yiduobo的每日leetcode 1930.长度为3的不同回文子序列"
question_id: "1930"
question: "长度为 3 的不同回文子序列"
problem_url: "https://leetcode.cn/problems/unique-length-3-palindromic-subsequences/"
difficulty: "Medium"
rating: 1533
created: "2022-03-25T23:04:06+08:00"
updated: "2022-03-25T23:04:06+08:00"
upvotes: 0
comments: 0
---

# 1930. 长度为3的不同回文子序列

> **[yiduobo的每日leetcode 1930.长度为3的不同回文子序列](https://zhuanlan.zhihu.com/p/487726566) · 知乎 · 2022-03-25 · 赞同 0**
> 力扣：[1930. 长度为 3 的不同回文子序列](https://leetcode.cn/problems/unique-length-3-palindromic-subsequences/) · Medium · 灵茶山艾府：[两种方法：枚举两侧 / 枚举中间，附进阶问题（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1930.长度为3的不同回文子序列

[力扣](https://leetcode-cn.com/problems/unique-length-3-palindromic-subsequences/)

题目要求找出长度为3，且不重复的所有回文子序列的个数。由于题目要求不重复，那么就有两个思路，第一个是先枚举两边的字符，然后从a到z枚举中间的字符，判断字符串中是否具备这样的回文子序列；另一个则是先枚举中间的字符，然后从a到z枚举两侧的字符在进行判断。我在这里采用的是枚举两侧字符的做法。

为了使得字符串中更容易出现枚举到的子序列，那么显然应该让两边的字符尽量靠边。换言之，对于枚举到的两边的字符，应该选择该字符串第一次出现和最后一次的位置作为两边，然后再考察这两个位置之间是否有枚举到的中间字符。这里实际上是一个区间内是否存在某字符的问题，可以通过前缀和来进行优化，于是现在就得到了一种做法：

1、从头向后一趟遍历，统计出每个字符第一次和最后一次出现位置，并对每个字符都计算后前缀中出现该字符的次数

2、枚举回文子序列两侧的字符char：

若char没有出现过，或者其首次出现的位置就等于最后一次出现的位置，也就是说其仅出现一次，那么char就不可能成为合法回文子序列两侧的字符。

否则的话枚举中间的字符，并利用前缀数组来判断char首次的位置与最后一次出现的位置之间是否存在枚举到的字符，若存在，就说明得到了合法的回文子序列，答案加上1

最后附上python代码：

```python
class Solution(object):
    def countPalindromicSubsequence(self, s):
        """
        :type s: str
        :rtype: int
        """

        first = {}
        last = {}
        cnt_list = []
        for index, char in enumerate(s):
            if char not in first:
                first[char] = index
            last[char] = index
            if index == 0:
                cnt_list.append({char : 1})
            else:
                cnt_list.append(cnt_list[-1].copy())
                cnt_list[-1][char] = cnt_list[-1].get(char, 0) + 1
        
        res = 0
        for asc in range(97, 123):
            char = chr(asc)
            if char in first and first[char] != last[char]:
                for mid_asc in range(97, 123):
                    mid_char = chr(mid_asc)
                    cnt = cnt_list[last[char] - 1].get(mid_char, 0) - cnt_list[first[char]].get(mid_char, 0)
                    if cnt > 0:
                        res += 1

        return res
```
