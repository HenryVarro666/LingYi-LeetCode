---
title: "2418. 按身高排序"
aliases: ["yiduobo的每日leetcode 2418.按身高排序"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/569541582"
zhihu_id: "569541582"
zhihu_title: "yiduobo的每日leetcode 2418.按身高排序"
question_id: "2418"
question: "按身高排序"
problem_url: "https://leetcode.cn/problems/sort-the-people/"
difficulty: "Easy"
created: "2022-09-30T01:18:53+08:00"
updated: "2022-09-30T01:18:53+08:00"
upvotes: 1
comments: 0
---

# 2418. 按身高排序

> **[yiduobo的每日leetcode 2418.按身高排序](https://zhuanlan.zhihu.com/p/569541582) · 知乎 · 2022-09-30 · 赞同 1**
> 力扣：[2418. 按身高排序](https://leetcode.cn/problems/sort-the-people/) · Easy · 灵茶山艾府：[常用编程技巧（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2418.按身高排序

[力扣](https://leetcode.cn/problems/sort-the-people/)

比较基础的题目，按题目要求排序就行了。具体实现上，既可以将姓名和身高合并在一起，然后按照身高作为关键字排序，也可以将身高单独排序获得顺序数组，再将对应的名字填充到答案对应的位置中。

最后附上python代码：

```python
class Solution(object):
    def sortPeople(self, names, heights):
        """
        :type names: List[str]
        :type heights: List[int]
        :rtype: List[str]
        """

        return [names[x] for x in sorted(range(len(heights)), key=lambda d:heights[d], reverse=True)]
```
