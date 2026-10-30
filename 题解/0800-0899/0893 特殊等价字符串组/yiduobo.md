---
title: "893. 特殊等价字符串组"
aliases: ["yiduobo的每日leetcode 893.特殊等价字符串组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/352446855"
zhihu_id: "352446855"
zhihu_title: "yiduobo的每日leetcode 893.特殊等价字符串组"
question_id: "893"
question: "特殊等价字符串组"
problem_url: "https://leetcode.cn/problems/groups-of-special-equivalent-strings/"
created: "2021-02-23T22:00:47+08:00"
updated: "2021-02-23T22:00:47+08:00"
upvotes: 0
comments: 0
---

# 893. 特殊等价字符串组

> **[yiduobo的每日leetcode 893.特殊等价字符串组](https://zhuanlan.zhihu.com/p/352446855) · 知乎 · 2021-02-23 · 赞同 0**
> 力扣：[893. 特殊等价字符串组](https://leetcode.cn/problems/groups-of-special-equivalent-strings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

893.特殊等价字符串组

[力扣](https://leetcode-cn.com/problems/groups-of-special-equivalent-strings/)

由于奇数位上或偶数位上的字符可以任意交换，那么只要两个字符串奇数位上的字符组成一致，同时偶数位上的字符组成一致，那么这两个字符串就是特殊等价字符串。

我在这里的方法是将奇数位上的字符转化为大写字符，那么就可以直接统计字符串中每个字符出现的次数，然后用哈希表记录下来，最终答案就是哈希表的长度。

最后附上python代码：

```python
class Solution(object):
    def numSpecialEquivGroups(self, A):
        """
        :type A: List[str]
        :rtype: int
        """

        word_set = set()
        res = 0
        for word in A:
            char_dict = {}
            for index, char in enumerate(word):
                if index & 1:
                    char = chr(ord(char) - 32)
                char_dict[char] = char_dict.get(char, 0) + 1
            word_set.add(tuple(sorted(char_dict.items())))

        return len(word_set)
```
