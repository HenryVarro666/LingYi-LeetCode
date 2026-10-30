---
title: "823. 带因子的二叉树"
aliases: ["yiduobo的每日leetcode 823.带因子的二叉树"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/di-tui", "题单/动态规划", "题单/动态规划/其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/344115361"
zhihu_id: "344115361"
zhihu_title: "yiduobo的每日leetcode 823.带因子的二叉树"
question_id: "823"
question: "带因子的二叉树"
problem_url: "https://leetcode.cn/problems/binary-trees-with-factors/"
difficulty: "Medium"
rating: 1900
created: "2021-01-18T22:27:55+08:00"
updated: "2021-01-18T22:27:55+08:00"
upvotes: 0
comments: 0
---

# 823. 带因子的二叉树

> **[yiduobo的每日leetcode 823.带因子的二叉树](https://zhuanlan.zhihu.com/p/344115361) · 知乎 · 2021-01-18 · 赞同 0**
> 力扣：[823. 带因子的二叉树](https://leetcode.cn/problems/binary-trees-with-factors/) · Medium · 灵茶山艾府：[从记忆化搜索到递推，教你一步步思考动态规划！（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

823.带因子的二叉树

[力扣](https://leetcode-cn.com/problems/binary-trees-with-factors/)

动态规划的题目。由于这里可以使用的因子都大于1，那么对于一棵树而言，如果其具有左右孩子，那么左右孩子的值必然是小于等于根节点的值的。基于这一点，我们可以将arr先从小到大进行排序，然后令f[i]表示以arr[i]为根节点的数有多少种形态。

对于f[i]，其根节点值为arr[i]，那么我们可以枚举arr[0]到arr[i - 1]，设当前枚举到arr[j]，若arr[i] % arr[j] \= 0，且arr[i] / arr[j]也在arr当中，说明可以使用arr[j]以及arr[i] / arr[j]作为左右子树的根节点，因此有

f\[i\] +\= f\[j\] \* f\[pos\[arr\[i\] / arr\[j\]\]

其中pos\[arr\[i\] / arr\[j\]\]表示arr\[i\] / arr\[j\]在arr中的位置

在枚举完arr[0]到arr[i - 1]后，不要忘了arr[i]单独一个节点也能形成一棵树，因此还需要将f[i]加上1。

在求解完所有的f之后，最终答案就是f数组之和。

在枚举arr的过程中，简单起见可以只枚举平方小于等于arr[i]的arr[j]，然后在累加到f[i]时乘上2。不过需要注意的是这里如果arr[j]等于arr[i] / arr[j]，说明左右子树不能交换，所以在这种情况下不能乘上2。

最后附上python代码：

```python
class Solution(object):
    def numFactoredBinaryTrees(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        mod = 10 ** 9 + 7
        arr = sorted(arr)
        pos_dict = {}
        for index, num in enumerate(arr):
            pos_dict[num] = index
        f = [1]
        n = len(arr)
        for i in range(1, n):
            f.append(0)
            now = arr[i]
            for j in range(0, i):
                if arr[j] ** 2 <= now and now % arr[j] == 0:
                    tmp = now / arr[j]
                    if tmp in pos_dict:
                        pos = pos_dict[tmp]
                        if tmp == arr[j]:
                            f[i] += f[j] ** 2
                        else:
                            f[i] += f[pos] * f[j] * 2
                        f[i] %= mod
            f[i] = (f[i] + 1) % mod
        
        return sum(f) % mod
```
