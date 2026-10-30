---
title: "1998. 数组的最大公因数排序"
aliases: ["yiduobo的每日leetcode 1998.数组的最大公因数排序"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/union-find", "题单/常用数据结构", "题单/数学算法", "题单/常用数据结构/七-并查集", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/501430933"
zhihu_id: "501430933"
zhihu_title: "yiduobo的每日leetcode 1998.数组的最大公因数排序"
question_id: "1998"
question: "数组的最大公因数排序"
problem_url: "https://leetcode.cn/problems/gcd-sort-of-an-array/"
difficulty: "Hard"
rating: 2429
created: "2022-04-19T21:42:43+08:00"
updated: "2022-04-19T21:42:43+08:00"
upvotes: 0
comments: 0
---

# 1998. 数组的最大公因数排序

> **[yiduobo的每日leetcode 1998.数组的最大公因数排序](https://zhuanlan.zhihu.com/p/501430933) · 知乎 · 2022-04-19 · 赞同 0**
> 力扣：[1998. 数组的最大公因数排序](https://leetcode.cn/problems/gcd-sort-of-an-array/) · Hard · 灵茶山艾府：[并查集+分组排序](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1998.数组的最大公因数排序

[力扣](https://leetcode-cn.com/problems/gcd-sort-of-an-array/)

题目可以让数值不互质的两个位置上的数进行交换，那么一个自然的想法就是把数值不互质的位置之间连上边，就可以得到若干个连通分量。对于同一个连通分量中的位置，是可以任意排布顺序的，因为在执行时只需要先将各个桥两侧的数位置换到位，然后再逐步置换到最终位置。

接下来的问题就是如何判断联通，在这里只需要对每个数分解质因数，然后利用并查集将具有相同质因子的数位合并到一起。

至于分解质因数，则可以使用筛法先找出每个数的最小质因子然后迭代求解。

最后附上python代码：

```python
class Solution(object):
    def gcdSort(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        max_num = max(nums)
        prime = range(max_num + 1)

        x = 2
        while x * x <= max_num:
            now = x + x
            while now <= max_num:
                if prime[now] == now:
                    prime[now] = x
                now += x
            x += 1

        fa = range(max_num + 1)
        for num in nums:
            now = num
            while now > 1:
                self.union(num, prime[now], fa)
                now /= prime[now]
        
        for index, num in enumerate(sorted(nums)):
            if num != nums[index] and self.find(num, fa) != self.find(nums[index], fa):
                return False

        return True

    def union(self, x, y, fa):
        fa_x = self.find(x, fa)
        fa_y = self.find(y, fa)
        if fa_x != fa_y:
            if fa_x < fa_y:
                fa[fa_x] = fa_y
            else:
                fa[fa_y] = fa_x
    
    def find(self, x, fa):
        if fa[x] != x:
            fa[x] = self.find(fa[x], fa)
        
        return fa[x]
```
