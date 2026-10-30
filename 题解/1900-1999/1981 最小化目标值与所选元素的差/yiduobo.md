---
title: "1981. 最小化目标值与所选元素的差"
aliases: ["yiduobo的每日leetcode 1981.最小化目标值与所选元素的差"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/dp", "leetcode/dp-2", "题单/动态规划", "题单/动态规划/三-背包"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/498111643"
zhihu_id: "498111643"
zhihu_title: "yiduobo的每日leetcode 1981.最小化目标值与所选元素的差"
question_id: "1981"
question: "最小化目标值与所选元素的差"
problem_url: "https://leetcode.cn/problems/minimize-the-difference-between-target-and-chosen-elements/"
difficulty: "Medium"
rating: 2010
created: "2022-04-14T02:44:32+08:00"
updated: "2022-04-14T02:44:32+08:00"
upvotes: 0
comments: 0
---

# 1981. 最小化目标值与所选元素的差

> **[yiduobo的每日leetcode 1981.最小化目标值与所选元素的差](https://zhuanlan.zhihu.com/p/498111643) · 知乎 · 2022-04-14 · 赞同 0**
> 力扣：[1981. 最小化目标值与所选元素的差](https://leetcode.cn/problems/minimize-the-difference-between-target-and-chosen-elements/) · Medium · 灵茶山艾府：[每组恰好选一个的分组背包 + 常数优化至 40ms](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1981.最小化目标值与所选元素的差

[力扣](https://leetcode-cn.com/problems/minimize-the-difference-between-target-and-chosen-elements/)

经典的动态规划问题，令f[i][j]表示前i行中，以第i行的数字结尾时能否选出和为j的数字组合，那么对于f[i][j]，就可以枚举第i行的所有数num，若f[i - 1][j - num]为true，就可以得到f[i][j]为true。

动态规划完成后，只需要从target开始同时向上和向下进行枚举答案num，若某一时刻满足f[n - 1][num]为true，说明可以选出一种和为num的数字组合，此时的答案就是abs(target - num)。

具体实现上，我换了一种写法。令f[i]表示前i行中，以第i行的数字结尾时能选出的数字和的集合，那么此时为了得到f[i]，就需要将f[i - 1]中的数字和与第i行的说有数进行组合，并将和加入到f[i]中。

动态规划完成后，则可以枚举f[n - 1]中的所有数字，找出其中与target最接近的。

上面两种方法的状态转移都只与上一轮有关，因此可以使用滚动数组来优化掉一维。

最后附上python代码：

```python
class Solution(object):
    def minimizeTheDifference(self, mat, target):
        """
        :type mat: List[List[int]]
        :type target: int
        :rtype: int
        """

        m = len(mat)

        f = set()
        for num in mat[0]:
            f.add(num)

        for i in range(1, m):
            g = f.copy()
            f = set()
            for num in mat[i]:
                for j in g:
                    f.add(j + num)

        res = None
        for num in f:
            if res is None or res > abs(num - target):
                res = abs(num - target)
        
        return res
```
