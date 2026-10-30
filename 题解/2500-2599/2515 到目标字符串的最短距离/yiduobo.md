---
title: "2515. 到目标字符串的最短距离"
aliases: ["yiduobo的每日leetcode 2515.到目标字符串的最短距离"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/enumeration"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/634848092"
zhihu_id: "634848092"
zhihu_title: "yiduobo的每日leetcode 2515.到目标字符串的最短距离"
question_id: "2515"
question: "到目标字符串的最短距离"
problem_url: "https://leetcode.cn/problems/shortest-distance-to-target-string-in-a-circular-array/"
difficulty: "Easy"
created: "2023-06-06T19:22:31+08:00"
updated: "2023-06-06T19:22:31+08:00"
upvotes: 0
comments: 0
---

# 2515. 到目标字符串的最短距离

> **[yiduobo的每日leetcode 2515.到目标字符串的最短距离](https://zhuanlan.zhihu.com/p/634848092) · 知乎 · 2023-06-06 · 赞同 0**
> 力扣：[2515. 到目标字符串的最短距离](https://leetcode.cn/problems/shortest-distance-to-target-string-in-a-circular-array/) · Easy · 灵茶山艾府：[两种方法：从左到右遍历 / 从 startIndex 往两侧遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2515.到目标字符串的最短距离

[力扣](https://leetcode.cn/problems/shortest-distance-to-target-string-in-a-circular-array/)

题目的数据规模较小，随便怎么处理都可以。我在这里采用的是从起始位置，使用两个指针分别向两侧同时移动，首次到达目标字符串所需的步数即为最终答案。另外，若最终两个指针最终汇集到一起，说明数组中不存在目标字符串，此时返回-1。

最后附上python代码：

```python
class Solution(object):
    def closetTarget(self, words, target, startIndex):
        """
        :type words: List[str]
        :type target: str
        :type startIndex: int
        :rtype: int
        """

        if words[startIndex] == target:
            return 0
        
        left = startIndex
        right = startIndex
        n = len(words)
        step = 0
        while True:
            left = (left - 1 + n) % n
            right = (right + 1) % n
            step += 1
            if words[left] == target or words[right] == target:
                return step
            
            if left == right or (left - 1 + n) % n == right:
                break
        
        return -1
```
