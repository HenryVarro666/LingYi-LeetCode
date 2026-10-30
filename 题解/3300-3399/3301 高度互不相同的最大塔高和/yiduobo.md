---
title: "3301. 高度互不相同的最大塔高和"
aliases: ["yiduobo的每日leetcode 3301.高度互不相同的最大塔高和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/978410776"
zhihu_id: "978410776"
zhihu_title: "yiduobo的每日leetcode 3301.高度互不相同的最大塔高和"
question_id: "3301"
question: "高度互不相同的最大塔高和"
problem_url: "https://leetcode.cn/problems/maximize-the-total-height-of-unique-towers/"
difficulty: "Medium"
rating: 1448
created: "2024-10-13T02:21:09+08:00"
updated: "2024-10-13T02:21:25+08:00"
upvotes: 1
comments: 0
---

# 3301. 高度互不相同的最大塔高和

> **[yiduobo的每日leetcode 3301.高度互不相同的最大塔高和](https://zhuanlan.zhihu.com/p/978410776) · 知乎 · 2024-10-13 · 赞同 1**
> 力扣：[3301. 高度互不相同的最大塔高和](https://leetcode.cn/problems/maximize-the-total-height-of-unique-towers/) · Medium · 灵茶山艾府：[从最大元素开始贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3301.高度互不相同的最大塔高和

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-the-total-height-of-unique-towers/description/)

题目给出一个数组maximumHeight，其中maximumHeight[i]表示第i座塔的高度上限。现在需要为每座塔都设置一个高度，要求塔的高度不能超过高度上限，且所有塔的高度都互不相同。问所有塔高度之和最大可以是多少。

题目要求所有塔的高度之和最大，那么最理想的情况自然是所有塔都能达到其高度上限。但是还有一个条件是不能出现相同高度的塔，那么当两座塔高度相同时，就不得不降低其中一座塔的高度。注意到同高这种情况可能多次出现，而且也可能出现一座塔高度降低后还是与另一座塔同高，那么就需要将这些塔按高度上限从大到小排序，这样才方便处理高度相同的情况。

另外在具体实现上，不需要记录当前高度的塔的数量然后这个向下设置高度，而是可以使用一个变量now，表示上一座塔高度，通过now来为下一座塔设置高度。now在一开始设置为最高塔的高度上限，即排序后的maximumHeight[0]，接下来从下标1开始遍历排序后的maximumHeight，对于当前高度上限h，若h \< now，那么就可以顶格安排这座塔的高度，同时now降低到h，反之若h >\= now，那么当前这座塔的高度最高只能是now - 1，于是此时应该将now减去1。若某一时刻now等于0，说明当前塔无法设置高度，直接返回-1。若都能设置高度，那么每轮的now累加起来就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def maximumTotalSum(self, maximumHeight):
        """
        :type maximumHeight: List[int]
        :rtype: int
        """

        maximumHeight.sort(reverse=True)
        now = maximumHeight[0]
        s = now

        for h in maximumHeight[1:]:
            if now > h:
                now = h
            else:
                now -= 1
                if now == 0:
                    return -1
            
            s += now
        
        return s
```
