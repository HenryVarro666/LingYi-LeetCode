---
title: "1941. 检查是否所有字符出现次数相同"
aliases: ["yiduobo的每日leetcode 1941.检查是否所有字符出现次数相同"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/489144979"
zhihu_id: "489144979"
zhihu_title: "yiduobo的每日leetcode 1941.检查是否所有字符出现次数相同"
question_id: "1941"
question: "检查是否所有字符出现次数相同"
problem_url: "https://leetcode.cn/problems/check-if-all-characters-have-equal-number-of-occurrences/"
difficulty: "Easy"
created: "2022-03-28T19:23:10+08:00"
updated: "2022-03-28T19:23:10+08:00"
upvotes: 0
comments: 0
---

# 1941. 检查是否所有字符出现次数相同

> **[yiduobo的每日leetcode 1941.检查是否所有字符出现次数相同](https://zhuanlan.zhihu.com/p/489144979) · 知乎 · 2022-03-28 · 赞同 0**
> 力扣：[1941. 检查是否所有字符出现次数相同](https://leetcode.cn/problems/check-if-all-characters-have-equal-number-of-occurrences/) · Easy · 灵茶山艾府：[Go 模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1941.检查是否所有字符出现次数相同

[力扣](https://leetcode-cn.com/problems/check-if-all-characters-have-equal-number-of-occurrences/)

比较基础的题目，一趟遍历，使用dict统计每种字符出现的次数，然后判断每种出现过的字符其出现次数是否相同即可。

最后附上python代码：

```python
class Solution(object):
    def areOccurrencesEqual(self, s):
        """
        :type s: str
        :rtype: bool
        """

        char_dict = {}
        for char in s:
            char_dict[char] = char_dict.get(char, 0) + 1
        
        char_cnt = char_dict.values()
        for index in range(1, len(char_cnt)):
            if char_cnt[index] != char_cnt[0]:
                return False

        return True
```
