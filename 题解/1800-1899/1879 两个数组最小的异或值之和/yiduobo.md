---
title: "1879. 两个数组最小的异或值之和"
aliases: ["yiduobo的每日leetcode 1879.两个数组最小的异或值之和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "leetcode/bitmask", "题单/动态规划", "题单/图论算法", "题单/动态规划/九-状态压缩-DP-状压-DP", "题单/图论算法/八-网络流"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/476346921"
zhihu_id: "476346921"
zhihu_title: "yiduobo的每日leetcode 1879.两个数组最小的异或值之和"
question_id: "1879"
question: "两个数组最小的异或值之和"
problem_url: "https://leetcode.cn/problems/minimum-xor-sum-of-two-arrays/"
difficulty: "Hard"
rating: 2145
created: "2022-03-05T18:52:26+08:00"
updated: "2022-03-05T18:52:27+08:00"
upvotes: 0
comments: 0
---

# 1879. 两个数组最小的异或值之和

> **[yiduobo的每日leetcode 1879.两个数组最小的异或值之和](https://zhuanlan.zhihu.com/p/476346921) · 知乎 · 2022-03-05 · 赞同 0**
> 力扣：[1879. 两个数组最小的异或值之和](https://leetcode.cn/problems/minimum-xor-sum-of-two-arrays/) · Hard · 灵茶山艾府：[状压 DP](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1879.两个数组最小的异或值之和

[力扣](https://leetcode-cn.com/problems/minimum-xor-sum-of-two-arrays/)

题目的数据规模比较小，可以使用状态压缩动态规划去做，不过如果从图论的角度来看这个问题，会有更好的做法。将nums1中和nums2中的每个数都视为图中的一个节点，接下来将nums1中的每个数与nums2中的每个数都连上一条边，边的权重就是两个数的异或值，那么此时的目标就是从中选出n条边，要求图中的每个点只能使用一次，且这些边的权重和最小。

这是一个典型的二分图最优匹配问题，经典的做法有KM算法，当然也可以使用费用流建模来求解。

我在这里采用的是费用流建模：

1、从源向nums1中的每个点连接一条边，容量为1费用为0，表示nums1中的每个点都只能使用一次，且这个选择的过程不会产生费用

2、从nums2中的每个点向汇点连接一条边，同样是容量为1费用为0，表示nums2中的每个点只能使用一次，这个选择同样不会产生费用

3、从nums1中的每个点向nums2中的每个点连接一条边，容量为1，费用则是两个数的异或值，表示这条边只能使用一次，同时做出这个选择的代价就是这两个数的异或值

此时执行费用流，可以满足每个点都被使用且仅被使用一次，同时最终权重之和最小对应了异或值之和最小。

最后附上python代码：

```python
class Solution(object):
    def minimumXORSum(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        n = len(nums1)
        c = {x : {} for x in range(n + n + 2)}
        v = {x : {} for x in range(n + n + 2)} 
        s = n + n
        t = n + n + 1
        for i in range(n):
            c[s][i] = 1
            c[i][s] = 0
            v[s][i] = 0
            v[i][s] = 0

            c[i + n][t] = 1
            v[i + n][t] = 0
            c[t][i + n] = 0
            v[t][i + n] = 0

            for j in range(n):
                c[i][j + n] = 1
                c[j + n][i] = 0
                v[i][j + n] = nums1[i] ^ nums2[j]
                v[j + n][i] = -(nums1[i] ^ nums2[j])

        res = 0
        while True:
            l = 0
            r = 1
            dis = [None] * (n + n + 2)
            dis[s] = 0
            q = [s]
            fa = {}
            used = set([s])

            while l < r:
                now = q[l]
                l += 1
                used.remove(now)
                for next in c[now]:
                    if c[now][next] > 0 and (dis[next] is None or dis[next] > dis[now] + v[now][next]):
                        dis[next] = dis[now] + v[now][next]
                        fa[next] = now
                        if next not in used:
                            used.add(next)
                            r += 1
                            q.append(next)

            if dis[t] is not None:
                res += dis[t]
                now = t
                while now != s:
                    c[fa[now]][now] -= 1
                    c[now][fa[now]] += 1
                    now = fa[now]
            else:
                break

        return res
```
