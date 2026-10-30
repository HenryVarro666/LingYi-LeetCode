---
title: "2234. 花园的最大总美丽值"
aliases: ["yiduobo的每日leetcode 2234.花园的最大总美丽值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/two-pointers", "leetcode/sorting", "题单/滑动窗口与双指针", "题单/贪心算法", "题单/滑动窗口与双指针/三-单序列双指针", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/544217622"
zhihu_id: "544217622"
zhihu_title: "yiduobo的每日leetcode 2234.花园的最大总美丽值"
question_id: "2234"
question: "花园的最大总美丽值"
problem_url: "https://leetcode.cn/problems/maximum-total-beauty-of-the-gardens/"
difficulty: "Hard"
rating: 2562
created: "2022-07-21T01:38:37+08:00"
updated: "2022-07-21T01:38:37+08:00"
upvotes: 0
comments: 0
---

# 2234. 花园的最大总美丽值

> **[yiduobo的每日leetcode 2234.花园的最大总美丽值](https://zhuanlan.zhihu.com/p/544217622) · 知乎 · 2022-07-21 · 赞同 0**
> 力扣：[2234. 花园的最大总美丽值](https://leetcode.cn/problems/maximum-total-beauty-of-the-gardens/) · Hard · 灵茶山艾府：[贪心+排序+双指针（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2234.花园的最大总美丽值

[力扣](https://leetcode.cn/problems/maximum-total-beauty-of-the-gardens/)

花园可以分为三个部分。第一个部分是一开始就有至少target朵花的花园，后续对这些花园也不需要进行任何操作。第二部分是新增了若干朵花之后有了target朵花的花园，第三部分则是最终也没有target朵花的花园。

最终答案是第一部分的花园数目加上第二部分的花园数目，乘以full之后再加上第三部分中每个花园中花的最小值乘以partial。

由于第一个部分是定值，那么只需要想办法确定第二部分有哪些花园，然后再想办法将剩余的话分给第三部分的花园，让第三部分花园中花的最小值最大就行了。

一个自然的想法是应该先将当前花较多的花园变为第二部分的花园，简单的证明是若存在两个花园，拥有的花分别是a和b，且满足a \< b \< target：

1、如果能将a培养到target，那么将b培养成有target朵花的花园，再将a培养成b也必然是可行的。

2、反过来，如果能将b培养到target，则不一定能将a培养到target。

有了这个结论，就可以将当前花数目不足target的花园按花数从小到大进行排序，得到排序后的数组sorted_flowers。然后反向一趟遍历，枚举将哪些花园培养到了target。

接下来的问题则是对于剩下的花，应该如何分配才能使得第三部分花园中花的最小值最大。很明显，每一朵花都要种在当前花数目最少的花园中，但是如果直接模拟这个过程的话时间复杂度太高，需要进行优化。

在这里可以采用上一题相似的做法，先提前预处理出将第三部分花园中最小值变为sorted_flowers[0]、sorted_flowers[1]、...、sorted_flowers[-1]所需要的花的数目。很明显，这个数目是单调不减的，因此在得到这个数目对应的数组后就可以在里面二分，找出当前剩余花的数目可以让第三部分花园中花的最小值变成多少。

需要特别注意的是，有一种情况是将第三部分中所有花园花的数目都变成了第三部分花园中原始花数目的最大值，同时还有剩余的花，此时则需要将剩余的花平均分给第三部分的花园。另外，在这里平均分的时候需要注意第三部分中花园花的数目还有一个上界，即target - 1。

最后附上python代码：

```python
class Solution(object):
    def maximumBeauty(self, flowers, newFlowers, target, full, partial):
        """
        :type flowers: List[int]
        :type newFlowers: int
        :type target: int
        :type full: int
        :type partial: int
        :rtype: int
        """

        sorted_flowers = sorted(flowers)
        need_flowers = []
        full_cnt = 0
        for index in range(len(sorted_flowers)):
            if sorted_flowers[index] >= target:
                full_cnt += 1
            elif len(need_flowers) == 0:
                need_flowers.append(0)
            else:
                need_flowers.append(need_flowers[-1] + index * (sorted_flowers[index] - sorted_flowers[index - 1]))
        
        m = len(need_flowers)
        if m == 0:
            return full_cnt * full

        def find(r):
            if newFlowers >= need_flowers[r]:
                return r
            else:
                l = 0
                while l < r:
                    mid = (l + r + 1) >> 1
                    if newFlowers >= need_flowers[mid]:
                        l = mid
                    else:
                        r = mid - 1
                return l
        
        p = find(m - 1)
        delta = (newFlowers - need_flowers[p]) / (p + 1)
        if sorted_flowers[p] + delta >= target:
            res = full_cnt * full + (target - 1) * partial
        else:
            res = full_cnt * full + (sorted_flowers[p] + delta) * partial

        for index in range(m - 1, 0, -1):
            if newFlowers < target - sorted_flowers[index]:
                return res
            
            newFlowers -= (target - sorted_flowers[index])
            full_cnt += 1
            p = find(index - 1)
            delta = (newFlowers - need_flowers[p]) / (p + 1)
            if sorted_flowers[p] + delta >= target:
                res = max(res, full_cnt * full + (target - 1) * partial)
            else:
                res = max(res, full_cnt * full + (sorted_flowers[p] + delta) * partial)

        if newFlowers >= target - sorted_flowers[0]:
            res = max(res, (full_cnt + 1) * full)
        
        return res
```
