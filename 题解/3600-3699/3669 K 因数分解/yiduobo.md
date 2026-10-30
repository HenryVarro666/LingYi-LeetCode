---
title: "3669. K因数分解"
aliases: ["yiduobo的每日leetcode 3669.K因数分解"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/math", "leetcode/combinatorics", "leetcode/number-theory", "题单/链表-二叉树与回溯", "题单/数学算法", "题单/链表-二叉树与回溯/四-回溯", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1950330029822150442"
zhihu_id: "1950330029822150442"
zhihu_title: "yiduobo的每日leetcode 3669.K因数分解"
question_id: "3669"
question: "K 因数分解"
problem_url: "https://leetcode.cn/problems/balanced-k-factor-decomposition/"
difficulty: "Medium"
rating: 1917
created: "2025-09-20T01:48:12+08:00"
updated: "2025-09-20T01:48:13+08:00"
upvotes: 0
comments: 0
---

# 3669. K因数分解

> **[yiduobo的每日leetcode 3669.K因数分解](https://zhuanlan.zhihu.com/p/1950330029822150442) · 知乎 · 2025-09-20 · 赞同 0**
> 力扣：[3669. K 因数分解](https://leetcode.cn/problems/balanced-k-factor-decomposition/) · Medium · 灵茶山艾府：[暴搜 + 排除等效冗余 + 最优性剪枝（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3669.K因数分解

[3669. K 因数分解 - 力扣（LeetCode）](https://leetcode.cn/problems/balanced-k-factor-decomposition/description/)

题目给出两个整数n和k，其中n不超过10^5，k在2到5之间。现在要求将n恰好拆分为k个正整数的乘积，使得这些正整数的最大值与最小值之间的差值尽可能的小。

直观感觉上没有太好的算法，不过好在n和k的规模不大，可以考虑使用回溯法暴力求解。

虽然不好直接得到最优解，但是得到一个较优解却是很容易的。对于最开始的情况，最理想的情况自然是分解出来的每个元素都恰好是n的k次方根，这样一来答案就为0了。即使无法达成，在这里选择一个尽量靠近k次方根的因数，也可以得到一个较优解。因此在这里可以从n的k次方根开始向下遍历所有因子进行尝试，这样一来在一开始就可以得到一个较优解，方便在计算过程中进行最优性剪枝。

另一方面，在计算时也可以强制约定因子按照从小到大的顺序排列，过滤掉重复计算的情况。

加上以上的剪枝之后，回溯法就可以轻松解决本题了。

最后附上python代码：

```python
class Solution(object):
    def minDifference(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: List[int]
        """
        
        global best
        global res
        res = [1, n]
        best = n - 1

        def search(now, r):
            if len(now) == k - 1:
                if r >= now[-1]:
                    global best
                    global res
                    if r - now[0] < best:
                        best = r - now[0]
                        res = now[:]
                        res.append(r)
                return
            
            ma = int(r ** (1.0 / (k - len(now)))) + 1

            for v in range(ma, 0, -1):
                if r % v == 0 and (not now or now[-1] <= v):
                    now.append(v)
                    search(now, r // v)
                    now.pop()
        
        search([], n)
        return res
```
