---
title: "465. 最优账单平衡"
aliases: ["yiduobo的每日leetcode 465.最优账单平衡"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/dynamic-programming", "leetcode/bitmask", "leetcode/dp", "leetcode/dp-2", "题单/动态规划", "题单/动态规划/九-状态压缩-DP-状压-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/599992626"
zhihu_id: "599992626"
zhihu_title: "yiduobo的每日leetcode 465.最优账单平衡"
question_id: "465"
question: "最优账单平衡"
problem_url: "https://leetcode.cn/problems/optimal-account-balancing/"
difficulty: "Hard"
created: "2023-01-19T03:25:43+08:00"
updated: "2023-01-19T03:25:43+08:00"
upvotes: 1
comments: 0
---

# 465. 最优账单平衡

> **[yiduobo的每日leetcode 465.最优账单平衡](https://zhuanlan.zhihu.com/p/599992626) · 知乎 · 2023-01-19 · 赞同 1**
> 力扣：[465. 最优账单平衡](https://leetcode.cn/problems/optimal-account-balancing/) · Hard · 灵茶山艾府：[子集状压 DP，附视频讲解（Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

465.最优账单平衡

[力扣](https://leetcode.cn/problems/optimal-account-balancing/)

对于多人间清账的问题，日常的一种做法就是各算各的。例如打牌，每个人都算自己赢了或者输了多少，然后对应地给钱或者收钱就行了。不过本题有所区别的地方是，只能点对点给钱，而不是把钱放出来各自找零。

到了这里，问题就转化成了给出一个数组，其中所有元素总和为零，现在要将其分为若干个部分，要求每个部分中的元素之和也为零，同时分出来的部分数量尽量多。在这里要求分出来部分尽量多的理由是对于每个部分，若这个部分中有k个元素，那么需要进行点对点交易的次数是k - 1次，也就是节省了一次。

对于上面这个问题，应该是不存在多项式算法的，只能采用dfs。

具体实现上，可以先将所有人分成给钱和收钱这两个部分，同时在dfs过程中记录当前部分的账目总和。若总和为负，那么就选择一个收钱的人加入，反过来则选择一个给钱的人加入。在这两种情况下，无论总和如何变化，都需要将总的交易次数加上1。

另外，还有一种特殊情况是当前部分的账目总和为零，说明上一个部分的账平了，可以划分出去，此时可以从剩下的人中任意选择一位加入到当前的部分，同时不需要更新最终答案，因为此时并没有新的交易产生。

最后分手python代码：

```python
class Solution(object):
    def minTransfers(self, transactions):
        """
        :type transactions: List[List[int]]
        :rtype: int
        """

        pos = {}
        neg = {}
        v = {}
        for x, y, z in transactions:
            if x not in v:
                v[x] = 0
            if y not in v:
                v[y] = 0
            v[x] -= z
            v[y] += z
        
        n = 0
        for u in v:
            if v[u] == 0:
                continue
            n += 1
            if v[u] > 0:
                pos[v[u]] = pos.get(v[u], 0) + 1
            else:
                neg[v[u]] = neg.get(v[u], 0) + 1

        global res
        res = n

        def dfs(level, now, cnt, pos, neg):
            global res
            if level == n:
                res = min(res, cnt)
                return

            if now == 0:
                delta = 0
            else:
                delta = 1

            if now <= 0:
                for num in pos:
                    if pos[num] > 0:
                        pos[num] -= 1
                        dfs(level + 1, now + num, cnt + delta, pos, neg)
                        pos[num] += 1
            else:
                for num in neg:
                    if neg[num] > 0:
                        neg[num] -= 1
                        dfs(level + 1, now + num, cnt + delta, pos, neg)
                        neg[num] += 1
        
            

        dfs(0, 0, 0, pos, neg)
        return res
```
