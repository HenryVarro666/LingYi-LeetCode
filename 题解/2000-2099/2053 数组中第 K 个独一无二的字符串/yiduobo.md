---
title: "2053. 数组中第K个独一无二的字符串"
aliases: ["yiduobo的每日leetcode 2053.数组中第K个独一无二的字符串"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/hash-table", "leetcode/string", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/512329521"
zhihu_id: "512329521"
zhihu_title: "yiduobo的每日leetcode 2053.数组中第K个独一无二的字符串"
question_id: "2053"
question: "数组中第 K 个独一无二的字符串"
problem_url: "https://leetcode.cn/problems/kth-distinct-string-in-an-array/"
difficulty: "Easy"
created: "2022-05-10T20:43:16+08:00"
updated: "2022-05-10T20:43:16+08:00"
upvotes: 0
comments: 0
---

# 2053. 数组中第K个独一无二的字符串

> **[yiduobo的每日leetcode 2053.数组中第K个独一无二的字符串](https://zhuanlan.zhihu.com/p/512329521) · 知乎 · 2022-05-10 · 赞同 0**
> 力扣：[2053. 数组中第 K 个独一无二的字符串](https://leetcode.cn/problems/kth-distinct-string-in-an-array/) · Easy · 灵茶山艾府：[哈希表扫两遍](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2053.数组中第K个独一无二的字符串

[力扣](https://leetcode.cn/problems/kth-distinct-string-in-an-array/)

由于字符串的长度都很小，那么可以直接使用哈希表统计每个字符串出现的次数，然后遍历原数组，若找到第k个只在哈希表中出现一次的字符串即可。

最后附上python代码：

```python
class Solution(object):
    def kthDistinct(self, arr, k):
        """
        :type arr: List[str]
        :type k: int
        :rtype: str
        """

        s_dict = {}
        for index, s in enumerate(arr):
            s_dict[s] = s_dict.get(s, 0) + 1
        
        cnt = 0
        for s in arr:
            if s_dict[s] == 1:
                cnt += 1
                if cnt == k:
                    return s
        
        return ""
```
