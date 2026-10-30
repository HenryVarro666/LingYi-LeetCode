---
title: "1569. 将子数组重新排序得到同一个二叉查找树的方案数"
aliases: ["yiduobo的每日leetcode 1569.将子数组重新排序得到同一个二叉查找树的方案数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/428500270"
zhihu_id: "428500270"
zhihu_title: "yiduobo的每日leetcode 1569.将子数组重新排序得到同一个二叉查找树的方案数"
question_id: "1569"
question: "将子数组重新排序得到同一个二叉查找树的方案数"
problem_url: "https://leetcode.cn/problems/number-of-ways-to-reorder-array-to-get-same-bst/"
created: "2021-11-02T15:29:48+08:00"
updated: "2021-11-02T15:29:48+08:00"
upvotes: 0
comments: 0
---

# 1569. 将子数组重新排序得到同一个二叉查找树的方案数

> **[yiduobo的每日leetcode 1569.将子数组重新排序得到同一个二叉查找树的方案数](https://zhuanlan.zhihu.com/p/428500270) · 知乎 · 2021-11-02 · 赞同 0**
> 力扣：[1569. 将子数组重新排序得到同一个二叉查找树的方案数](https://leetcode.cn/problems/number-of-ways-to-reorder-array-to-get-same-bst/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1569.将子数组重新排序得到同一个二叉查找树的方案数

[力扣](https://leetcode-cn.com/problems/number-of-ways-to-reorder-array-to-get-same-bst/)

观察样例可以发现，对于给出的数组，其首位必然会被当做bst的根节点，那么根据这个节点的大小，就可以将数组中其他的数划分到左子树和右子树中。对于左右子树而言，同样是使用一个数组来进行构造，也就是说可以通过递归来进行求解。

除此之外，在求解得到左右子树的方案后，还需要将二者拼起来。不妨设左右子树中节点的数目分别为l和r，那么实际上就是从l + r个位置中选择l个位置，来放置左子树中的节点，而剩下的节点则归右子树左右，因此一共有C(l + r, r)种组合。

令f[now]表示以now为根节点的子树可形成的方案数，那么就有

f[now] \= f[now.left] \* f[now.right] \* C(l + r, r)

其中l和r分别表示now.left以及now.right中的节点数

对于组合数C的计算，则可以提前预处理出来，即通过C(m, n) \= C(m - 1, n - 1) + C(m - 1, n)来求解。

求解完毕后，得到总的方案数res，此时还需要去除掉题目给出的这一种初始方案，那么最终答案就是res - 1。

最后附上python代码：

```python
class Solution(object):
    def numOfWays(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        c = [[0] * n for _ in range(n)]

        mod = 10 ** 9 + 7
        for i in range(n):
            for j in range(i + 1):
                if j == 0:
                    c[i][j] = 1
                elif j + j > i:
                    c[i][j] = c[i][i - j]
                else:
                    c[i][j] = (c[i - 1][j - 1] + c[i - 1][j]) % mod
        
        return (self.dfs(nums, c, mod) - 1 + mod) % mod
    
    def dfs(self, nums, c, mod):
        if not nums:
            return 1
        
        root = nums[0]
        left = []
        right = []
        for num in nums[1:]:
            if num < root:
                left.append(num)
            else:
                right.append(num)
        
        l_res = self.dfs(left, c, mod)
        r_res = self.dfs(right, c, mod)
        
        res = 1
        res = res * l_res % mod
        res = res * r_res % mod
        res = res * c[len(nums) - 1][len(left)] % mod

        return res
```
