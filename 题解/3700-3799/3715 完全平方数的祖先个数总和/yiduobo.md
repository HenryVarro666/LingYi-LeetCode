---
title: "3715. 完全平方数的祖先个数总和"
aliases: ["yiduobo的每日leetcode 3715.完全平方数的祖先个数总和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/hash-table", "leetcode/math", "leetcode/backtracking", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1962302474481279245"
zhihu_id: "1962302474481279245"
zhihu_title: "yiduobo的每日leetcode 3715.完全平方数的祖先个数总和"
question_id: "3715"
question: "完全平方数的祖先个数总和"
problem_url: "https://leetcode.cn/problems/sum-of-perfect-square-ancestors/"
difficulty: "Hard"
rating: 2235
created: "2025-10-17T00:24:10+08:00"
updated: "2025-10-17T00:24:10+08:00"
upvotes: 2
comments: 0
---

# 3715. 完全平方数的祖先个数总和

> **[yiduobo的每日leetcode 3715.完全平方数的祖先个数总和](https://zhuanlan.zhihu.com/p/1962302474481279245) · 知乎 · 2025-10-17 · 赞同 2**
> 力扣：[3715. 完全平方数的祖先个数总和](https://leetcode.cn/problems/sum-of-perfect-square-ancestors/) · Hard · 灵茶山艾府：[无平方因子核 core + 枚举右维护左（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3715.完全平方数的祖先个数总和

<https://leetcode.cn/problems/sum-of-perfect-square-ancestors/description/>

题目给出一个整数n，以及一颗以节点0为根节点，包含n个节点(编号为0到n - 1)的无向树。这棵树由一个长度为n - 1的二维数组edges表示，其中edges\[i\] \= \[u\[i\], v\[i\]\]，表示在节点u\[i\]和v\[i\]之间由一条无向边。

另外给出一个整数数组nums，其中nums[i]为分配给节点i的正整数。

定义t[i]为节点i的所有祖先节点中，满足nums[i] \* nums[ancestor]为完全平方数的祖先个数，问t[1]到t[n - 1]之和是多少。

题目需要检测的是乘积的完全平方数，那么在计算乘积之前，可以先将参与乘法的两个元素中所有的完全平方因子都去掉，理由是若两个元素x \* y为完全平方数t^2，那么从x或y中去除掉某个完全平方因子p^2后，乘积将变为t^2 / p^2 \= (t / p)^2，依然是完全平方数。这里的隐藏条件是p^2是x或y的因子，那么其必然也是二者乘积t^2的因子，因此t^2必然可以被p^2整除，除法的结果(t / p)^2也必然是完全平方数。

基于上面的结论，就可以想将nums中每个元素的完全平方因子都去掉，即去掉所有的4、9、16、25、...等因子。接下来，对于新得到的nums[i]，若其能与nums[ancestor]相乘得到完全平方数，这里的nums[ancestor]就必须恰好等于nums[i]，也就是说，问题到这里就转化成了对于树中的每个节点，问有多少个祖先节点的值与当前节点相同。

对于这个问题，可以从根节点向下一趟dfs，在dfs过程中使用哈希表cnt记录从根节点到当前节点路径上所有节点的值出现的次数，对于当前节点now，与now值相同的节点数量就是cnt\[nums\[now\]\]，将其累加到答案中，然后将cnt\[nums\[now\]\]的值加上1之后递归计算now的所有孩子节点。需要注意，当计算完now的所有孩子节点并回溯到now之后，则需要将cnt\[nums\[now\]\]再减去1，因为其只应该影响到以now为根节点的子树中的节点，而不应该影响到树中的其他节点。

最后附上python代码：

```python
class Solution(object):
    def sumOfAncestors(self, n, edges, nums):
        """
        :type n: int
        :type edges: List[List[int]]
        :type nums: List[int]
        :rtype: int
        """
        
        power = []
        x = 2
        ma = max(nums)
        while x * x <= ma:
            power.append(x * x)
            x += 1

        for index, v in enumerate(nums):
            for p in power:
                if p > v:
                    break
                while v % p == 0:
                    v //= p
            
            nums[index] = v
        
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)
        
        cnt = {}
        global res
        res = 0
        def dfs(now, fa):
            global res
            res += cnt.get(nums[now], 0)
            cnt[nums[now]] = cnt.get(nums[now], 0) + 1
            for nxt in g[now]:
                if nxt == fa:
                    continue
                
                dfs(nxt, now)
            
            cnt[nums[now]] -= 1
        
        dfs(0, -1)
        return res
```
