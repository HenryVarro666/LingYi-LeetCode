---
title: "1657. 确定两个字符串是否接近"
aliases: ["yiduobo的每日leetcode 1657.确定两个字符串是否接近"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/array", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/441505558"
zhihu_id: "441505558"
zhihu_title: "yiduobo的每日leetcode 1657.确定两个字符串是否接近"
question_id: "1657"
question: "确定两个字符串是否接近"
problem_url: "https://leetcode.cn/problems/determine-if-two-strings-are-close/"
difficulty: "Medium"
rating: 1530
created: "2021-12-05T18:07:47+08:00"
updated: "2021-12-05T18:07:47+08:00"
upvotes: 0
comments: 0
---

# 1657. 确定两个字符串是否接近

> **[yiduobo的每日leetcode 1657.确定两个字符串是否接近](https://zhuanlan.zhihu.com/p/441505558) · 知乎 · 2021-12-05 · 赞同 0**
> 力扣：[1657. 确定两个字符串是否接近](https://leetcode.cn/problems/determine-if-two-strings-are-close/) · Medium · 灵茶山艾府：[理解操作本质+简洁写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1657.确定两个字符串是否接近

[力扣](https://leetcode-cn.com/problems/determine-if-two-strings-are-close/)

由于操作一可以任意交换两个字符的位置，就说明无需考虑各个字符的位置，只需要考虑字符的种类以及数量就好了。又由于操作二的转换是两种字符互换的，因此无论怎么操作，出现字符的种类是不会变化的，因此需要先考察两个字符串中出现字符的种类是否一样。另一方面，这个交换也不会改变各个字符出现次数的分布情况，因此还需要考察各个字符出现次数的分布。

根据上面的结论，可以发现只需要统计两个字符串中各个字符出现的次数，然后分别对比出现的字符是否一致，且次数的分布是否一致即可。

最后附上python代码：

```python
class Solution(object):
    def closeStrings(self, word1, word2):
        """
        :type word1: str
        :type word2: str
        :rtype: bool
        """

        cnt_dict1 = {}
        cnt_dict2 = {}

        for char in word1:
            cnt_dict1[char] = cnt_dict1.get(char, 0) + 1
        
        for char in word2:
            cnt_dict2[char] = cnt_dict2.get(char, 0) + 1
        
        if len(cnt_dict1) != len(cnt_dict2):
            return False
        
        for key in cnt_dict1.keys():
            if key not in cnt_dict2:
                return False
        
        if sorted(cnt_dict1.values()) != sorted(cnt_dict2.values()):
            return False
        
        return True
```
