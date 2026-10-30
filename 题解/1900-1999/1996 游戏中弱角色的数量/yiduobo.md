---
title: "1996. 游戏中弱角色的数量"
aliases: ["yiduobo的每日leetcode 1996.游戏中弱角色的数量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/500806782"
zhihu_id: "500806782"
zhihu_title: "yiduobo的每日leetcode 1996.游戏中弱角色的数量"
question_id: "1996"
question: "游戏中弱角色的数量"
problem_url: "https://leetcode.cn/problems/the-number-of-weak-characters-in-the-game/"
difficulty: "Medium"
created: "2022-04-18T21:22:53+08:00"
updated: "2022-04-18T21:22:54+08:00"
upvotes: 0
comments: 0
---

# 1996. 游戏中弱角色的数量

> **[yiduobo的每日leetcode 1996.游戏中弱角色的数量](https://zhuanlan.zhihu.com/p/500806782) · 知乎 · 2022-04-18 · 赞同 0**
> 力扣：[1996. 游戏中弱角色的数量](https://leetcode.cn/problems/the-number-of-weak-characters-in-the-game/) · Medium · 灵茶山艾府：[简洁写法：排序+一次遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1996.游戏中弱角色的数量

[力扣](https://leetcode-cn.com/problems/the-number-of-weak-characters-in-the-game/)

对于这类多指标严格大于的问题，常见的做法是通过某种手段保证其中的一些指标有序，然后枚举另一些指标进行判断。

在这里是个最基本的二指标问题，只需将攻击从大到小进行排序，然后遍历防御。对于当前遍历到的攻击和防御，以及可以确定的是当前的攻击小于等于之前枚举过的攻击和防御，同时也必然大于等于后续要枚举的攻击和防御，换言之，严格强于当前角色的的人只可能出现在之前枚举的角色当中，那么只需要记录之前枚举到的最大防御值，若这个防御值大于当前角色的防御值，那么当前角色就是弱角色了。

这里需要注意一种特殊情况，就是攻击相同的情况。对于这种情况，可以在排序时针对性处理，即在攻击相同的情况下将防御较小的排在前面。

另外，对于这类问题的进阶版，三指标的一般是第一维排序，对第二维进行归并排序，在这个过程中枚举第三维；四指标的则是第一维排序，对第二维进行归并排序，在这个过程中使用数据结构维护第三维，然后枚举第四维；更高维度的问题我暂时还没见过。

最后附上python代码：

```python
class Solution(object):
    def numberOfWeakCharacters(self, properties):
        """
        :type properties: List[List[int]]
        :rtype: int
        """

        sorted_properties = sorted(properties, key=lambda d:(-d[0], d[1]))

        max_def = sorted_properties[0][1]
        res = 0
        for index in range(1, len(sorted_properties)):
            if sorted_properties[index][1] < max_def:
                res += 1
            else:
                max_def = sorted_properties[index][1]
            
        return res
```
