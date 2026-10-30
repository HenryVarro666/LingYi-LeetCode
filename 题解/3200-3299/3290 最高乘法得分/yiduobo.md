---
title: "3290. 最高乘法得分"
aliases: ["yiduobo的每日leetcode 3290.最高乘法得分"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/四-经典线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/898484275"
zhihu_id: "898484275"
zhihu_title: "yiduobo的每日leetcode 3290.最高乘法得分"
question_id: "3290"
question: "最高乘法得分"
problem_url: "https://leetcode.cn/problems/maximum-multiplication-score/"
difficulty: "Medium"
rating: 1692
created: "2024-10-10T03:45:48+08:00"
updated: "2024-10-10T03:45:48+08:00"
upvotes: 2
comments: 0
---

# 3290. 最高乘法得分

> **[yiduobo的每日leetcode 3290.最高乘法得分](https://zhuanlan.zhihu.com/p/898484275) · 知乎 · 2024-10-10 · 赞同 2**
> 力扣：[3290. 最高乘法得分](https://leetcode.cn/problems/maximum-multiplication-score/) · Medium · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推到空间优化！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3290.最高乘法得分

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-multiplication-score/description/)

题目给出一个大小为4的整数数组a以及一个大小至少为4的整数数组b。现在要求从b中选出四个下标i\[0\]、i\[1\]、i\[2\]、i\[3\]，满足i\[0\] \< i\[1\] \< i\[2\] \< i\[3\]，且a\[0\] \* b\[i\[0\]\] + a\[1\] \* b\[i\[1\]\] + a\[2\] \* b\[i\[2\]\] + a\[3\] \* b\[i\[3\]\]最大。问最大的得分是多少。

经典的动态规划问题，令

f\[index\]表示从b\[0\]到b\[index\]中选出i\[0\]可以得到的最大a\[0\] \* b\[i\[0\]\]

g\[index\]表示从b\[0\]到b\[index\]中选出i\[0\]和i\[1\]可以得到的最大a\[0\] \* b\[i\[0\]\] + a\[1\] \* b\[i\[1\]\]

h[index]、t[index]则分别对应到从b[0]到b[index]选出前三项以及全部四项时的最大得分

那么对于以上四种状态表示：

1、对于f[index]，如果选择b[index]，那么得分就是a[0] \* b[index]，如果不选，就是延续之前的f[index - 1]，于是就有f[index] \= max(f[index - 1], a[0] \* b[index])

2、对于g\[index\]，如果选择b\[index\]作为b\[i\[1\]\]，那么得分就是f\[index - 1\] + a\[1\] \* b\[i\[1\]\]，在这里选择的前提是f\[index - 1\]存在。另外如果不选择b\[index\]，那么就是延续之前的g\[index - 1\]，于是就有g\[index\] \= max(g\[index - 1\], f\[index - 1\] + a\[1\] \* b\[index\])。

3、对于h[index]，与g[index]相同，有h[index] \= max(h[index - 1], g[index - 1] + a[2] \* b[index])

4、对于t[index]，也是一样的处理方法，有t[index] \= max(t[index - 1], h[index - 1] + a[3] \* b[index])

只需一趟遍历，计算出以上四个数组，答案记为t[-1]。

另外注意到这里每一轮的状态之和上一轮有关，因此可以使用变量迭代省去数组的空间。需要注意的是使用变量迭代时需要按照t、h、g、f的顺序来更新，因为t、h、g依赖的都是上一轮的h、g、f，不能先更新被依赖的项。

最后附上python代码：

```python
class Solution(object):
    def maxScore(self, a, b):
        """
        :type a: List[int]
        :type b: List[int]
        :rtype: int
        """

        f = g = h = t = None
        for v in b:
            if h is not None:
                x = v * a[3] + h
                if t is None or x > t:
                    t = x
            
            if g is not None:
                x = v * a[2] + g
                if h is None or x > h:
                    h = x
            
            if f is not None:
                x = v * a[1] + f
                if g is None or x > g:
                    g = x
            
            x = v * a[0]
            if f is None or x > f:
                f = x
        
        return t
```
