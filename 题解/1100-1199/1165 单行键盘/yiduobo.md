---
title: "1165. 单行键盘"
aliases: ["yiduobo的每日leetcode 1165.单行键盘"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/611363676"
zhihu_id: "611363676"
zhihu_title: "yiduobo的每日leetcode 1165.单行键盘"
question_id: "1165"
question: "单行键盘"
problem_url: "https://leetcode.cn/problems/single-row-keyboard/"
created: "2023-03-04T21:44:39+08:00"
updated: "2023-03-04T21:44:39+08:00"
upvotes: 0
comments: 0
---

# 1165. 单行键盘

> **[yiduobo的每日leetcode 1165.单行键盘](https://zhuanlan.zhihu.com/p/611363676) · 知乎 · 2023-03-04 · 赞同 0**
> 力扣：[1165. 单行键盘](https://leetcode.cn/problems/single-row-keyboard/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1165.单行键盘

[力扣](https://leetcode.cn/problems/single-row-keyboard/)

首先对键盘一趟遍历，使用哈希表记录每个字符的位置，接下来遍历单词，通过哈希表计算相邻字符间的距离并累计起来作为最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def calculateTime(self, keyboard, word):
        """
        :type keyboard: str
        :type word: str
        :rtype: int
        """

        pos = {}
        for index, char in enumerate(keyboard):
            pos[char] = index
        
        now = 0
        res = 0
        for char in word:
            p = pos[char]
            res += abs(now - p)
            now = p
        
        return res
```
