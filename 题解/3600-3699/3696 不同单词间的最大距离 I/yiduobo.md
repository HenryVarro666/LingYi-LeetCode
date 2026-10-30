---
title: "3696. 不同单词间的最大距离 I"
aliases: ["yiduobo的每日leetcode 3696.不同单词间的最大距离 I"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1956331897916461220"
zhihu_id: "1956331897916461220"
zhihu_title: "yiduobo的每日leetcode 3696.不同单词间的最大距离 I"
question_id: "3696"
question: "不同单词间的最大距离 I"
problem_url: "https://leetcode.cn/problems/maximum-distance-between-unequal-words-in-array-i/"
created: "2025-10-03T15:37:10+08:00"
updated: "2025-10-07T14:31:41+08:00"
upvotes: 1
comments: 0
---

# 3696. 不同单词间的最大距离 I

> **[yiduobo的每日leetcode 3696.不同单词间的最大距离 I](https://zhuanlan.zhihu.com/p/1956331897916461220) · 知乎 · 2025-10-03 · 赞同 1**
> 力扣：[3696. 不同单词间的最大距离 I](https://leetcode.cn/problems/maximum-distance-between-unequal-words-in-array-i/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3696.不同单词间的最大距离I

[3696. 不同单词间的最大距离 I - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-distance-between-unequal-words-in-array-i/)

题目给出一个字符串数组words，要求找出其中不同元素对之间的最远距离是多少，这里的距离定义为不同元素对的下标之差，再加上1。如果words中所有元素都相同，则返回0。

首先可以明确的是，若words[0]与words[-1]不同，那么就应该选择这两个元素间的距离作为最终答案，因为这就是数组中最远的距离。

更进一步的，如果words[0]与words[-1]相同，那么答案就是words中不等于words[0]的每个元素，到0或者n - 1的距离中的最大值。

理由是设当前答案由一组下标对(p, q)构成，那么显然有words[p] !\= words[q]，也就是说words[p]和words[q]中至少有一个不等于words[0]的元素。从这个元素的视角出发来进行分析，如果另一个元素在当前元素的左侧，那么使用words[0]替代另一个元素得到的结果是更优的，同样的，如果另一个元素在当前元素的右侧，那么使用words[-1]替代另一个元素得到的结果是更优的。也就是说，最终结果必然是words[0]或者words[-1]，与words中另一个不同于words[0]的元素构成的。

基于这个结论，就只需从下标1开始遍历到n - 2，对于其中与words[0]不同的元素，使用当前下标到0以及n - 1的距离来更新答案即可。

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
