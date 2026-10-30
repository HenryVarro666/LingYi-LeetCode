---
title: "3541. 找到频率最高的元音和辅音"
aliases: ["yiduobo的每日leetcode 3541.找到频率最高的元音和辅音"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1907586366629483860"
zhihu_id: "1907586366629483860"
zhihu_title: "yiduobo的每日leetcode 3541.找到频率最高的元音和辅音"
question_id: "3541"
question: "找到频率最高的元音和辅音"
problem_url: "https://leetcode.cn/problems/find-most-frequent-vowel-and-consonant/"
difficulty: "Easy"
created: "2025-05-19T22:31:59+08:00"
updated: "2025-05-19T22:31:59+08:00"
upvotes: 1
comments: 0
---

# 3541. 找到频率最高的元音和辅音

> **[yiduobo的每日leetcode 3541.找到频率最高的元音和辅音](https://zhuanlan.zhihu.com/p/1907586366629483860) · 知乎 · 2025-05-19 · 赞同 1**
> 力扣：[3541. 找到频率最高的元音和辅音](https://leetcode.cn/problems/find-most-frequent-vowel-and-consonant/) · Easy · 灵茶山艾府：[统计字母出现次数+位运算优化（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3541.找到频率最高的元音和辅音

[3541. 找到频率最高的元音和辅音 - 力扣（LeetCode）](https://leetcode.cn/problems/find-most-frequent-vowel-and-consonant/description/)

题目给出一个由小写英文字母组成的字符串s，要求找出其中出现频率最高的元音以及出现频率最高的辅音，返回这两个频率之和。

使用哈希表freq记录每种字符出现的次数，然后一趟遍历。对于当前字符char，先更新freq[char]，接下来若当前字符是元音，则使用freq[char]更新元音的最大频率max_v，否则使用freq[char]更新辅音的最大频率max_c。遍历完成后，返回max_v和max_c之和即可。

最后附上python代码：

```python
class Solution(object):
    def maxFreqSum(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        freq = {}
        vowel = set(['a', 'e', 'i', 'o', 'u'])
        max_v = 0
        max_c = 0
        for char in s:
            freq[char] = freq.get(char, 0) + 1
            if char in vowel:
                max_v = max(max_v, freq[char])
            else:
                max_c = max(max_c, freq[char])
        
        return max_v + max_c
```
