---
title: "3760. 不同首字母的子字符串数目"
aliases: ["yiduobo的每日leetcode 3760.不同首字母的子字符串数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1978547617689509891"
zhihu_id: "1978547617689509891"
zhihu_title: "yiduobo的每日leetcode 3760.不同首字母的子字符串数目"
question_id: "3760"
question: "不同首字母的子字符串数目"
problem_url: "https://leetcode.cn/problems/maximum-substrings-with-distinct-start/"
difficulty: "Medium"
rating: 1364
created: "2025-11-30T19:40:56+08:00"
updated: "2025-11-30T19:40:57+08:00"
upvotes: 1
comments: 0
---

# 3760. 不同首字母的子字符串数目

> **[yiduobo的每日leetcode 3760.不同首字母的子字符串数目](https://zhuanlan.zhihu.com/p/1978547617689509891) · 知乎 · 2025-11-30 · 赞同 1**
> 力扣：[3760. 不同首字母的子字符串数目](https://leetcode.cn/problems/maximum-substrings-with-distinct-start/) · Medium · 灵茶山艾府：[脑筋急转弯 / 位运算（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3760.不同首字母的子字符串数目

[3760. 不同首字母的子字符串数目 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-substrings-with-distinct-start/description/)

题目给出一个由小写英文字母组成的字符串s。现在要求将s拆分为若干个子串，使得每个子串都以不同的字符开头。问最多可以划分出多少个子串。

首先可以明确的是，最终结果的上限是s中不同字符的种数，因为最好的情况就是以每种字符开头的子串都有一个，而构造这种情况是很容易的：不妨设s中一共有k种不同字符，这些字符的起点按从左到右的顺序分别为p\[0\]、p\[1\]、...、p\[k - 1\]，那么将s划分为s\[p\[0\]: p\[1\]\]、s\[p\[1\]: p\[2\]\]、...、s\[p\[k - 2\]: p\[k - 1\]\]、s\[p\[k - 1\]:\]，就可以得到k个以不同字符开头的子串了。

基于上面的结论，只需对s一趟遍历，使用集合统计其中不同字符的种数，这个种数即为最终答案。

```python
class Solution(object):
    def maxDistinct(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        char = set()
        for c in s:
            char.add(c)
        return len(char)
```
