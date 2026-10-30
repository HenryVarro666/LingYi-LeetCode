---
title: "2813. 子序列最大优雅度"
aliases: ["yiduobo的每日leetcode 2813.子序列最大优雅度"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/greedy", "leetcode/hash-table", "leetcode/sorting", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/五-堆-优先队列", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/658179397"
zhihu_id: "658179397"
zhihu_title: "yiduobo的每日leetcode 2813.子序列最大优雅度"
question_id: "2813"
question: "子序列最大优雅度"
problem_url: "https://leetcode.cn/problems/maximum-elegance-of-a-k-length-subsequence/"
difficulty: "Hard"
rating: 2582
created: "2023-09-25T05:44:47+08:00"
updated: "2023-09-25T05:44:47+08:00"
upvotes: 0
comments: 0
---

# 2813. 子序列最大优雅度

> **[yiduobo的每日leetcode 2813.子序列最大优雅度](https://zhuanlan.zhihu.com/p/658179397) · 知乎 · 2023-09-25 · 赞同 0**
> 力扣：[2813. 子序列最大优雅度](https://leetcode.cn/problems/maximum-elegance-of-a-k-length-subsequence/) · Hard · 灵茶山艾府：[反悔贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2813.子序列最大优雅度

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximum-elegance-of-a-k-length-subsequence/description/)

题目给出一些项目，每个项目都有利润和品类两个属性。要求从中选出k个项目，使得这些项目的利润之和再加上不同品类的数量平方之和最大。

由于存在两个属性需要考虑，因此不能直接贪心，必须寻找合理的贪心方案。

既然有利润和品类两个属性，那么不妨先将其中之一做到极致，然后再看有没有修正的余地。我在这里选择的优先满足品类。

具体来说，先将所有项目按照利润从大到小进行排序，然后一趟遍历，尽量选出不同品类的项目。

在这里有两种可能。

第一种是选出了k个不同品类的项目，这些项目的利润是同品类项目中最大的。这里有一个隐藏条件是其他品类项目中利润最大的也没被选上，这也就以为着其他品类的项目利润都不如这些已经选择的项目。

第二种则是选出的不同品类项目不足k个，但是这些项目的利润依然是同品类项目中最大的。

使用一个数组choose记录选出项目的利润值，那么在当前情况下，优雅度就是sum(choose) + len(choose)^2

接下来则需要按利润从大到小再次遍历所有项目，尝试使用未被选取的项目来替换掉已选择的某些项目。

在这里又有一个隐藏条件，就是如果某个项目被替换掉了，那么这个被替换出去的项目一定是一个独一无二的品类。理由很简单，若某个品类的项目当前出现的次数大于等于2，那么说明至少有一个项目是在当前这个替换的阶段被加入进来的。由于是按利润从大到小遍历的，因此当前处理的项目的利润一定不超过之前被替换进来的项目，因此也不可能比这个对应品类一开始就有的那个项目要大，也就没有执行替换操作的理由了。

换言之，在这里被替换掉的一定是一开始执行品类选择时被选择的利润最小的项目，也就是choose最后的元素choose[-1]。

另外，如果在选取品类阶段出现了不同品类项目数目不足k个的情况，那么在这里需要先将选取的项目补足到k个，而不是直接进行替换。

若当前已经选取了k个项目，那么对于新来的这个项目，首先对比其利润与choose[-1]的大小。若新来的项目利润更低，那么说明当前项目以及之后的所有项目都不需要再考虑了，因为这些项目的利润太低。反之，若其利润比choose[-1]要大，那么就是用该项目替换choose[-1]。

在这里需要说明的一点时，这个替换操作必然会使得已有的品类减一，即当前项目必然是之前已经选取的某个品类的项目，理由是当前项目既不可能是之前从未出现过的某个品类的项目，也不可能是某个之前被替换出去的品类的项目，更不可能与其要替换的目标为同一品类。

前面部分成立的理由是在选取不同品类时的隐藏条件，即其他未被选取的品类的项目利润一定不如选择的项目的利润，也就是choose数组中的元素。

中间部分成立的理由则是若当前项目的品类与之前被替换出去的项目品类相同，那么就意味着当前项目的利润比当前的choose[-1]大，但是之前被替换出去的同品类项目的利润应该处于之前choose数组的末尾，也就是小于等于当前的choose[-1]，这样一来一去就是当前项目利润 > choose[-1] >\= 原同品类项目利润，然而在最开始进行品类选择时，选取的是品类中利润最高的项目，与这个不等式是矛盾的。

最后这个部分最简单，因为当前项目的利润必然小于等于最开始被选择的同品类项目，因此完全没有替换的必要。

综合起来，就可以明确当前的替换行为，一定是某个已选择品类的项目，替换掉某个唯一品类的项目。

根据这一点，就可以方便计算当前的优雅度了。对于上一轮的优雅度now，首先需要将其减去len(choose) \* 2 - 1，也就是choose的长度减去1之后，品类的平方这一项从(len(choose))^2变为了(len(choose) - 1)^2，变化的量是len(choose) \* 2 - 1。接下来，还需要将now减去choose[-1]，表示choose的最后这个项目被替换掉，同时再将now加上当前新来的项目的利润p。最后，将choose的末尾弹出然后使用now更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def findMaximumElegance(self, items, k):
        """
        :type items: List[List[int]]
        :type k: int
        :rtype: int
        """

        vis = set()
        vis_cate = set()
        choose = []
        now = 0
        items.sort(reverse=True)
        for index, (p, c) in enumerate(items):
            if c not in vis_cate:
                vis_cate.add(c)
                choose.append(p)
                vis.add(index)
                if len(choose) == k:
                    break
        
        now = sum(choose) + len(vis_cate) ** 2

        k -= len(vis_cate)
        res = now
        for index, (p, c) in enumerate(items):
            if index not in vis:
                if k > 0:
                    now += p
                    k -= 1
                else:
                    if choose[-1] >= p:
                        break
                    now -= len(choose) * 2 - 1
                    now -= choose.pop()
                    now += p
                
                res = max(res, now)
        
        return res
```
