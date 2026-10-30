---
title: "3883. 统计满足数位和数组的非递减数组数目"
aliases: ["yiduobo的每日leetcode 3883.统计满足数位和数组的非递减数组数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/two-pointers", "leetcode/dynamic-programming", "leetcode/prefix-sum", "题单/动态规划", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2022429312976953950"
zhihu_id: "2022429312976953950"
zhihu_title: "yiduobo的每日leetcode 3883.统计满足数位和数组的非递减数组数目"
question_id: "3883"
question: "统计满足数位和数组的非递减数组数目"
problem_url: "https://leetcode.cn/problems/count-non-decreasing-arrays-with-given-digit-sums/"
difficulty: "Hard"
rating: 2172
created: "2026-03-31T22:03:36+08:00"
updated: "2026-03-31T22:03:37+08:00"
upvotes: 1
comments: 0
---

# 3883. 统计满足数位和数组的非递减数组数目

> **[yiduobo的每日leetcode 3883.统计满足数位和数组的非递减数组数目](https://zhuanlan.zhihu.com/p/2022429312976953950) · 知乎 · 2026-03-31 · 赞同 1**
> 力扣：[3883. 统计满足数位和数组的非递减数组数目](https://leetcode.cn/problems/count-non-decreasing-arrays-with-given-digit-sums/) · Hard · 灵茶山艾府：[两种方法：前缀和优化 DP / 双指针优化 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3883.统计满足数位和数组的非递减数组数目

<https://leetcode.cn/problems/count-non-decreasing-arrays-with-given-digit-sums/description/>

一个标题里面竟然出现了四个数字，也不知道丢给大模型会不会数不清楚里面数的数量。

题目给出一个长度为n的整数数组digitSum，其中n的大小不超过1000，且数组中元素的大小在0到50之间。

对于一个长度为n的整数数组arr，若其满足以下条件，则称其为有效的：

- 数组中的所有元素大小都在0到5000之间
- 数组是非递减的
- 对于其中任意下标index，arr[index]的数位和都恰好等于digitSum[index]

问不同的有效数组的数目。

由于题目中arr的长度以及其中元素的上限都不大，在这里就可以采用二维的动态规划来进行求解。具体来说，令f[index][v]表示arr已经填充了arr[0]到arr[index]且目前填充的前缀有效，同时arr[index]值为v时合法的填充方案数，那么f[index][v]：

1、若v的数位和不等于digitSum[index]，那么就有f[index][v] \= 0

2、否则其只需要满足非递减就行了，也就是说前一个数arr[index - 1]的取值必须小于等于v，那么就有

f[index][v] \= f[index - 1][0] + f[index - 1][1] + ... + f[index - 1][v]

注意到这种情况下转移方程式一个前缀和的形式，那么就可以设置一个前缀和数组pre，其中pre[index]表示f[index]的前缀和，那么转移方程就可以写成f[index][v] \= pre[index - 1][v]。在计算完所有的f[index]后，只需一趟遍历，就可以计算出对应的pre[index]。

全部计算完成后，pre[-1][-1]即为最终答案。

还有一个小优化是可以在计算之前先遍历0到5000，计算出每种元素的数位和并记录在哈希表candidate中，其中candidate\[s\]表示数位和为s的元素列表。那么在动态规划的计算中，就可以只遍历candidate\[digitSum\[index\]\]，而不需要遍历完整的0到5000。

另外注意到f的计算只依赖于上一轮的pre，而pre的计算只依赖于本轮的f，因此在这里可以让f和pre互相迭代从而省去index这一维。

最后附上python代码：

```python
class Solution(object):
    def countArrays(self, digitSum):
        """
        :type digitSum: List[int]
        :rtype: int
        """
        
        candidate = {}
        for v in range(5001):
            s = 0
            x = v
            while x:
                s += x % 10
                x //= 10
            
            if s not in candidate:
                candidate[s] = []
            candidate[s].append(v)

        pre = [1] * 5001
        mod = 10 ** 9 + 7
        for s in digitSum:
            f = [0] * 5001
            if s in candidate:
                for v in candidate[s]:
                    f[v] = pre[v]
            pre[0] = f[0]
            for v in range(1, 5001):
                pre[v] = pre[v - 1] + f[v]
                if pre[v] >= mod:
                    pre[v] -= mod

        return pre[-1]
```
