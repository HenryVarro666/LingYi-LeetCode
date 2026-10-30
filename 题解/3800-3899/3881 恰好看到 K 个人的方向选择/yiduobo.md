---
title: "3881. 恰好看到k个人的方向选择"
aliases: ["yiduobo的每日leetcode 3881.恰好看到k个人的方向选择"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser", "leetcode/math", "leetcode/combinatorics", "题单/数学算法", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2022069175477094187"
zhihu_id: "2022069175477094187"
zhihu_title: "yiduobo的每日leetcode 3881.恰好看到k个人的方向选择"
question_id: "3881"
question: "恰好看到 K 个人的方向选择"
problem_url: "https://leetcode.cn/problems/direction-assignments-with-exactly-k-visible-people/"
difficulty: "Medium"
rating: 1761
created: "2026-03-30T22:07:00+08:00"
updated: "2026-03-30T22:07:03+08:00"
upvotes: 1
comments: 0
---

# 3881. 恰好看到k个人的方向选择

> **[yiduobo的每日leetcode 3881.恰好看到k个人的方向选择](https://zhuanlan.zhihu.com/p/2022069175477094187) · 知乎 · 2026-03-30 · 赞同 1**
> 力扣：[3881. 恰好看到 K 个人的方向选择](https://leetcode.cn/problems/direction-assignments-with-exactly-k-visible-people/) · Medium · 灵茶山艾府：[脑筋急转弯，答案与 pos 无关（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3881.恰好看到K个人的方向选择

<https://leetcode.cn/problems/direction-assignments-with-exactly-k-visible-people/description/>

题目给出三个整数n、pos以及k，其中n不超过10^5，k和pos都在0到n - 1之间。

现在有n个人排成一排，下标从0到n - 1。每个人都必须独立地选择一个方向，若选择L，那么只有这个人右边的人可以看到他，反之若选择R，那么就只有这个人左边的人可以看到他。

那么对于一个位于pos的人而言，所有index \< pos的人只有选择L时，位于pos的这个人才可以看到这个人，同理，所有index > pos的人只有选择R时，位于pos的这个人才可以看到这个人。

现在要求计算可以让位于pos的人恰好看到k个人的方案数，答案对10^9 + 7取模。

对于一个位于pos的人，其左侧一共有0到pos - 1这一共pos个空位，其右侧一共有pos + 1到n - 1这一共n - 1 - pos个空位。为了让位于pos的人可以恰好看到k个人，那么就需要从左侧选出left个空位，让这些空位上的人选择L，左侧其他的人选择R，然后从右侧选出k - left个空位，让这些空位上的人选择R，其他的人选择L。

更进一步的，在可以枚举所有可行的left，然后计算C(pos, left) \* C(n - 1 - pos, right)并累加到答案中。这里left的取值上下界分贝为min(k, pos)以及max(k - (n - 1 - pos), 0)。其中上界很好理解，下界中的k - (n - 1 - pos)，表示即使右侧所有人都选择R可以被看见，为了凑足k个人，左侧还需要有k - (n - 1 - pos)个人被看见。

接下来就是计算组合数学的部分了。由于本题的数据规模较大还需要取模，那么在这里就必须预处理出阶乘以及阶乘的逆元来帮助计算组合数。逆元相关的部分可以参考之前的3405题，这里就不展开了。

[yiduobo的每日leetcode 3405.统计恰好有K个相等相邻元素的数组数目](https://zhuanlan.zhihu.com/p/31401526455)

需要特别注意的是，在累加完得到答案之后，还需要将最终答案乘以2，理由是位于pos的这个人可以选L也可以选R。

最后附上python代码：

```python
class Solution(object):
    def countVisiblePeople(self, n, pos, k):
        """
        :type n: int
        :type pos: int
        :type k: int
        :rtype: int
        """
        
        left_slot = pos
        right_slot = n - pos - 1
        ma = max(left_slot, right_slot)

        fac = [1, 1]
        mod = 10 ** 9 + 7
        for v in range(2, ma + 1):
            fac.append(fac[-1] * v % mod)
        
        inv = [1, 1]
        inv_fac = [1, 1]
        for v in range(2, ma + 1):
            inv.append((mod - mod // v) * inv[mod % v] % mod)
            inv_fac.append(inv_fac[-1] * inv[-1] % mod)
        
        def C(m, k):
            v = fac[m] * inv_fac[k] % mod * inv_fac[m - k] % mod
            return v

        left_mi = max(0, k - right_slot)
        left_ma = min(left_slot, k)
        res = 0
        for left in range(left_mi, left_ma + 1):
            right = k - left
            res = (res + C(left_slot, left) * C(right_slot, right) % mod) % mod
        
        return res * 2 % mod
```
