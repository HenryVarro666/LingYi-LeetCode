---
title: "3814. 预算下的最大总容量"
aliases: ["yiduobo的每日leetcode 3814.预算下的最大总容量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/two-pointers", "leetcode/binary-search", "leetcode/sorting", "leetcode/monotonic-stack", "题单/滑动窗口与双指针", "题单/单调栈", "题单/滑动窗口与双指针/三-单序列双指针", "题单/单调栈/一-单调栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1996991773264859919"
zhihu_id: "1996991773264859919"
zhihu_title: "yiduobo的每日leetcode 3814.预算下的最大总容量"
question_id: "3814"
question: "预算下的最大总容量"
problem_url: "https://leetcode.cn/problems/maximum-capacity-within-budget/"
difficulty: "Medium"
rating: 1796
created: "2026-01-22T00:58:18+08:00"
updated: "2026-01-22T00:58:23+08:00"
upvotes: 1
comments: 2
---

# 3814. 预算下的最大总容量

> **[yiduobo的每日leetcode 3814.预算下的最大总容量](https://zhuanlan.zhihu.com/p/1996991773264859919) · 知乎 · 2026-01-22 · 赞同 1**
> 力扣：[3814. 预算下的最大总容量](https://leetcode.cn/problems/maximum-capacity-within-budget/) · Medium · 灵茶山艾府：[三种方法：二分查找/双指针/单调栈（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3814.预算下的最大总容量

<https://leetcode.cn/problems/maximum-capacity-within-budget/description/>

题目给出两个长度为n的整数数组costs和capacity，其中costs[index]和capacity[index]分别表示第index台机器的购买成本以及性能容量。

另外给出一个整数budget，现在可以选择至多两台不同的机器，使得所选机器的总成本严格小于budget。

问可能得到的最大总容量是多少。

由于至多可以选择两条不同的机器，那么就意味着最终的方案可能是只选择一台，或者选择两台不同的。

对于前面这种情况，显然应该选择成本小于budget的机器中，capacity最大的，只需一趟遍历就可以找出应该选择哪台机器。

对于后面这种情况，则需要先保证costs之和不超过budget，再保证capacity最大。对于两数之和不大于指定数的问题，一种经典做法是先将这些数从小到大进行排序，接下来对于一个costs[index]，不妨设可以与其配对的最大值为costs[p]，那么对于costs[index + 1]而言，可以配对的最大值costs[p']，其中的p'必然小于等于p。也就是说随着index的增大，其对应的p是单调不增的，而与capacity[index]配对的最优值，则是capacity[0]到capacity[p]之间的最大值。需要注意的是，若这里的最大值就是capacity[index]自身，那么就应该取次大值。

可以发现，这是一个前缀最大值与次大值的问题，于是可以在按照costs从小到大排序后，先对capacity进行一趟遍历，计算出capacity的前缀最大值以及次大值。接下来再遍历costs，对于当前的costs[index]：

1、若其小于budget，则使用对应的capacity[index]来更新答案

2、另一方面，在上一轮的基础上找到当前index对应的p，满足costs[index] + costs[p] \< budget，且p最大，此时若capacity到p为止的前缀最大值等于capacity[index]，就是用前缀次大值加上capacity[index]来更新答案，否则使用前缀最大值加上capacity[index]来更新答案

最后附上python代码：

```python
class Solution(object):
    def maxCapacity(self, costs, capacity, budget):
        """
        :type costs: List[int]
        :type capacity: List[int]
        :type budget: int
        :rtype: int
        """
        
        info = sorted(zip(costs, capacity))
        first = [info[0][1]]
        second = [None]

        for _, ca in info[1:]:
            if ca > first[-1]:
                second.append(first[-1])
                first.append(ca)
            elif second[-1] is None or ca > second[-1]:
                first.append(first[-1])
                second.append(ca)
            else:
                first.append(first[-1])
                second.append(second[-1])
        
        p = len(info) - 1
        res = 0
        for index, (co, ca) in enumerate(info):
            if co >= budget:
                break
            res = max(res, ca)
            while p > index and info[p][0] + co >= budget:
                p -= 1

            if p > index:
                if first[p] != ca:
                    res = max(res, first[p] + ca)
                else:
                    res = max(res, second[p] + ca)
        
        return res
```
