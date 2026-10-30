---
title: "1626. 无矛盾的最佳球队"
aliases: ["yiduobo的每日leetcode 1626.无矛盾的最佳球队"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-indexed-tree", "leetcode/dynamic-programming", "leetcode/sorting", "leetcode/shi-pin", "leetcode/dp", "leetcode/dp-2", "leetcode/ti-dan", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/八-树状数组和线段树", "题单/动态规划/四-经典线性-DP", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/436930625"
zhihu_id: "436930625"
zhihu_title: "yiduobo的每日leetcode 1626.无矛盾的最佳球队"
question_id: "1626"
question: "无矛盾的最佳球队"
problem_url: "https://leetcode.cn/problems/best-team-with-no-conflicts/"
difficulty: "Medium"
rating: 2027
created: "2021-11-24T00:18:48+08:00"
updated: "2021-11-24T00:18:48+08:00"
upvotes: 0
comments: 0
---

# 1626. 无矛盾的最佳球队

> **[yiduobo的每日leetcode 1626.无矛盾的最佳球队](https://zhuanlan.zhihu.com/p/436930625) · 知乎 · 2021-11-24 · 赞同 0**
> 力扣：[1626. 无矛盾的最佳球队](https://leetcode.cn/problems/best-team-with-no-conflicts/) · Medium · 灵茶山艾府：[最长递增子序列：从 O(n^2) 到 O(nlogn)（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1626.无矛盾的最佳球队

[力扣](https://leetcode-cn.com/problems/best-team-with-no-conflicts/)

想想球队里有一千岁老妖怪也是很厉害了。。

回到题目。题目要求从球员中选出一部分，满足这些球员的分数虽然年龄的增长单调递增，问选出来球员的最大分数是多少。

对于这类多维度有序问题，如果维度为二，那么常见的做法就是对其中一维进行排序，然后直接处理另一维；若维度为三，则是先对其中一维进行排序，然后通过归并排序第二维的时候处理第三维；当维度更高时，似乎就没有太好的多项式算法了。

这里是一个二维度的问题，那么首先可以将球员按分数从小到大排序。排序完成后，对于某个球员而言，其前面的球员分数都比当前球员要小，因此只需要考察年龄就好了，于是问题就转化成了经典的动态规划问题。

令f[i]表示第0到i位球员，如果选择了第i位球员加入球队时球队的最大分数。那么对于f[i]而言，就需要在0到i - 1之间找到某个j，满足j的年龄小于等于i，且f[j]最大。这里隐藏了一个条件是对于j而言，f[j]代表的球队中j的分数最大，因此j的年龄也是最大的，这样一来这只球队中所有人的年龄就都小于等于i了，于是此时只需将i也加入到这支球队即可，即f[i] \= f[j] + scores[i]。

上面这种做法的时间复杂度为O(n^2)。不过注意到对于i而言，需要找到的是年龄在1到i之间，且球队分数最大的j，这是一个前缀最大值问题，很自然想到使用树状数组来进行优化。

对于i而言，首先通过树状数组找到年龄在1到i之间的球队最大得分s，此时将i加入到球队之后得分变为了s + scores[i]。用这个分数更新答案，并将其加入到树状数组当中即可。这样一来，就得到了一种时间复杂度为O(nlogn)的做法。

最后附上python代码：

```python
class Solution(object):
    def bestTeamScore(self, scores, ages):
        """
        :type scores: List[int]
        :type ages: List[int]
        :rtype: int
        """

        infos = sorted(zip(scores, ages), key=lambda d:(d[0], d[1]))
        index_array = [0] * 1001
        res = 0
        for score, age in infos:
            now = age
            tmp = 0
            while now >= 1:
                tmp = max(tmp, index_array[now])
                now -= now & -now
            
            tmp += score
            res = max(tmp, res)
            
            now = age
            while now <= 1000:
                index_array[now] = max(index_array[now], tmp)
                now += now & -now

        return res
```
