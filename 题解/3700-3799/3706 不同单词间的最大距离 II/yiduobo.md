---
title: "3706. 不同单词间的最大距离 II"
aliases: ["yiduobo的每日leetcode 3706.不同单词间的最大距离 II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1958906002863793318"
zhihu_id: "1958906002863793318"
zhihu_title: "yiduobo的每日leetcode 3706.不同单词间的最大距离 II"
question_id: "3706"
question: "不同单词间的最大距离 II"
problem_url: "https://leetcode.cn/problems/maximum-distance-between-unequal-words-in-array-ii/"
created: "2025-10-07T14:50:30+08:00"
updated: "2025-10-07T14:50:30+08:00"
upvotes: 0
comments: 0
---

# 3706. 不同单词间的最大距离 II

> **[yiduobo的每日leetcode 3706.不同单词间的最大距离 II](https://zhuanlan.zhihu.com/p/1958906002863793318) · 知乎 · 2025-10-07 · 赞同 0**
> 力扣：[3706. 不同单词间的最大距离 II](https://leetcode.cn/problems/maximum-distance-between-unequal-words-in-array-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3706.不同单词间的最大距离II

[3706. Maximum Distance Between Unequal Words in Array II - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-distance-between-unequal-words-in-array-ii/description/)

题目给出一个字符串数组words，要求找出其中不同元素对之间的最远距离是多少，这里的距离定义为不同元素对的下标之差，再加上1。如果words中所有元素都相同，则返回0。

本题的题设与之前的3696题相同，不过数据规模较大，words的长度可达10^5。

之前3696题的处理方法时间复杂度是很优的，可以直接照搬之前3696题的处理方法，先检测两端的字符串是否相同，若是，再检测中部是否存在不同与两端的字符串。

[yiduobo的每日leetcode 3696.不同单词间的最大距离 I](https://zhuanlan.zhihu.com/p/1956331897916461220)

最后附上python代码：

```python
class Solution(object):
    def maxDistance(self, words):
        """
        :type words: List[str]
        :rtype: int
        """
        
        if words[0] != words[-1]:
            return len(words)
        
        res = 0
        for index in range(1, len(words) - 1):
            if words[index] != words[0]:
                res = max(res, index + 1, len(words) - index)
        
        return res
```
