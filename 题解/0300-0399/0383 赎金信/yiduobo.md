---
title: "383. 赎金信"
aliases: ["yiduobo的每日leetcode 383.赎金信"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/hash-table", "题单/面试经典-150-题", "题单/面试经典-150-题/哈希表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/166660618"
zhihu_id: "166660618"
zhihu_title: "yiduobo的每日leetcode 383.赎金信"
question_id: "383"
question: "赎金信"
problem_url: "https://leetcode.cn/problems/ransom-note/"
difficulty: "Easy"
created: "2020-08-04T20:18:42+08:00"
updated: "2020-08-04T20:18:42+08:00"
upvotes: 0
comments: 0
---

# 383. 赎金信

> **[yiduobo的每日leetcode 383.赎金信](https://zhuanlan.zhihu.com/p/166660618) · 知乎 · 2020-08-04 · 赞同 0**
> 力扣：[383. 赎金信](https://leetcode.cn/problems/ransom-note/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

383.赎金信<https://leetcode-cn.com/problems/ransom-note/>

比较基础的题目。分别统计ransom和magazine中每个字符出现的次数，然后逐个比较即可。

最后附上python代码：

```python
class Solution(object):
    def canConstruct(self, ransomNote, magazine):
        """
        :type ransomNote: str
        :type magazine: str
        :rtype: bool
        """

        ransom_dict = {}
        magazine_dict = {}

        for char in ransomNote:
            ransom_dict[char] = ransom_dict.get(char, 0) + 1
        for char in magazine:
            magazine_dict[char] = magazine_dict.get(char, 0) + 1

        for char in ransom_dict:
            if magazine_dict.get(char, 0) < ransom_dict[char]:
                return False

        return True
```
