---
title: "451. 根据字符出现频率排序"
aliases: ["yiduobo的每日leetcode 451.根据字符出现频率排序"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/212872439"
zhihu_id: "212872439"
zhihu_title: "yiduobo的每日leetcode 451.根据字符出现频率排序"
question_id: "451"
question: "根据字符出现频率排序"
problem_url: "https://leetcode.cn/problems/sort-characters-by-frequency/"
created: "2020-09-02T20:50:08+08:00"
updated: "2020-09-02T20:50:08+08:00"
upvotes: 0
comments: 0
---

# 451. 根据字符出现频率排序

> **[yiduobo的每日leetcode 451.根据字符出现频率排序](https://zhuanlan.zhihu.com/p/212872439) · 知乎 · 2020-09-02 · 赞同 0**
> 力扣：[451. 根据字符出现频率排序](https://leetcode.cn/problems/sort-characters-by-frequency/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

451.根据字符出现频率排序<https://leetcode-cn.com/problems/sort-characters-by-frequency/>

比较基础的题目。统计每个字符出现的次数，排序后输出即可。

最后附上python代码：

```python
class Solution(object):
    def frequencySort(self, s):
        """
        :type s: str
        :rtype: str
        """

        char_dict = {}
        for char in s:
            char_dict[char] = char_dict.get(char, 0) + 1
        
        res = ''
        for char, cnt in sorted(char_dict.items(), key=lambda d:d[1], reverse=True):
            res += char * cnt
        return res
```
