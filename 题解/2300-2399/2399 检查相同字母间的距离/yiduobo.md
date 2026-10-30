---
title: "2399. 检查相同字母间的距离"
aliases: ["yiduobo的每日leetcode 2399.检查相同字母间的距离"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/566905480"
zhihu_id: "566905480"
zhihu_title: "yiduobo的每日leetcode 2399.检查相同字母间的距离"
question_id: "2399"
question: "检查相同字母间的距离"
problem_url: "https://leetcode.cn/problems/check-distances-between-same-letters/"
difficulty: "Easy"
created: "2022-09-22T01:15:39+08:00"
updated: "2022-09-22T01:15:39+08:00"
upvotes: 0
comments: 0
---

# 2399. 检查相同字母间的距离

> **[yiduobo的每日leetcode 2399.检查相同字母间的距离](https://zhuanlan.zhihu.com/p/566905480) · 知乎 · 2022-09-22 · 赞同 0**
> 力扣：[2399. 检查相同字母间的距离](https://leetcode.cn/problems/check-distances-between-same-letters/) · Easy · 灵茶山艾府：[一次遍历：记录字母上次出现的位置（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2399.检查相同子母间的距离

[力扣](https://leetcode.cn/problems/check-distances-between-same-letters/)

题目要求相同字母间的距离符合distance数组中的规定，那么可以使用一个哈希表last_pos储存每个字符最后一次出现的位置，然后遍历s。对于当前字符char，若char出现在last_pos中，那么就需要计算当前位置和last_pos[char]之间的距离，并检测这个距离是否符合distance中的规定。若不符合，则直接返回false，否则就将last_pos[char]更新为当前位置，然后继续向后遍历。若顺利遍历完s，那么就返回true。

最后附上python代码：

```python
class Solution(object):
    def checkDistances(self, s, distance):
        """
        :type s: str
        :type distance: List[int]
        :rtype: bool
        """

        last_pos = {}
        for index, char in enumerate(s):
            if char in last_pos:
                if index - last_pos[char] - 1 != distance[ord(char) - 97]:
                    return False
            
            last_pos[char] = index
        
        return True
```
