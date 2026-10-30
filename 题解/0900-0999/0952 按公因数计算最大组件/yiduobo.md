---
title: "952. 按公因数计算最大组件"
aliases: ["yiduobo的每日leetcode 952.按公因数计算最大组件"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/359962111"
zhihu_id: "359962111"
zhihu_title: "yiduobo的每日leetcode 952.按公因数计算最大组件"
question_id: "952"
question: "按公因数计算最大组件"
problem_url: "https://leetcode.cn/problems/largest-component-size-by-common-factor/"
created: "2021-03-25T23:50:42+08:00"
updated: "2021-03-25T23:50:42+08:00"
upvotes: 0
comments: 0
---

# 952. 按公因数计算最大组件

> **[yiduobo的每日leetcode 952.按公因数计算最大组件](https://zhuanlan.zhihu.com/p/359962111) · 知乎 · 2021-03-25 · 赞同 0**
> 力扣：[952. 按公因数计算最大组件](https://leetcode.cn/problems/largest-component-size-by-common-factor/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

952.按公因数计算最大组件

[力扣](https://leetcode-cn.com/problems/largest-component-size-by-common-factor/)

首先很自然可以想到直接按照题目描述构图，两两枚举A中的数，然后判断二者的最大公约数是否大于1，若大于1则在二者之间连上一条边，构好图之后对图进行染色即可。

但是这里的A中最多有20000个数，直接两两枚举构图时间上肯定吃不消。再仔细分析题目给出的A[i]和A[j]有大于1的公约数这一条件，可以将这里所说的公约数进一步拆解，也就是当A[i]和A[j]有质数公约数时二者连上一条边。设当前有一个质数x，那么对于x的各种倍数，它们都有x这样一个质数公约数，也就是说这些数最终将被染上一个颜色，而此时则可以利用并查集进行高效的合并。

注意到A中的数字最多到100000，那么我们可以利用筛法，逐个枚举质数x，然后将x所有倍数通过并查集进行合并。设当前处理到x的某个倍数y，若y当前没有父亲，则设y的父亲为x，否则将y与x的父亲进行合并。

遍历完成后，遍历每个数，统计每个数父亲出现的次数，最多的次数即为答案。

最后附上python代码：

```python
class Solution(object):
    def largestComponentSize(self, A):
        """
        :type A: List[int]
        :rtype: int
        """

        fa = {1 : 1}
        max_num = 0
        for num in A:
            max_num = max(max_num, num)
            fa[num] = num

        prime = [True] * (max_num + 1)
        
        now = 2
        while now <= max_num:
            if prime[now]:
                if now not in fa:
                    fa[now] = now
                tmp = now + now
                while tmp <= max_num:
                    prime[tmp] = False
                    if tmp in fa:
                        self.union(now, tmp, fa)
                    tmp += now
            
            if now == 2:
                now = 3
            else:
                now += 2
        
        fa_cnt = {}
        for num in A:
            now_fa = self.get(num, fa)
            fa_cnt[now_fa] = fa_cnt.get(now_fa, 0) + 1

        return max(fa_cnt.values())
    
    def get(self, now, fa):
        if now != fa[now]:
            fa[now] = self.get(fa[now], fa)
        
        return fa[now]
    
    def union(self, x, y, fa):
        fa_x = self.get(x, fa)
        fa_y = self.get(y, fa)
        if fa_x < fa_y:
            fa[fa_y] = fa_x
        else:
            fa[fa_x] = fa_y
```
