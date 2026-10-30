---
title: "961. 重复N次的元素"
aliases: ["yiduobo的每日leetcode 961.重复N次的元素"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/math", "leetcode/random", "leetcode/randomized", "题单/数学算法", "题单/数学算法/六-随机算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/360867234"
zhihu_id: "360867234"
zhihu_title: "yiduobo的每日leetcode 961.重复N次的元素"
question_id: "961"
question: "在长度 2N 的数组中找出重复 N 次的元素"
problem_url: "https://leetcode.cn/problems/n-repeated-element-in-size-2n-array/"
difficulty: "Easy"
rating: 1162
created: "2021-03-29T22:47:23+08:00"
updated: "2021-03-29T22:47:23+08:00"
upvotes: 0
comments: 0
---

# 961. 重复N次的元素

> **[yiduobo的每日leetcode 961.重复N次的元素](https://zhuanlan.zhihu.com/p/360867234) · 知乎 · 2021-03-29 · 赞同 0**
> 力扣：[961. 在长度 2N 的数组中找出重复 N 次的元素](https://leetcode.cn/problems/n-repeated-element-in-size-2n-array/) · Easy · 灵茶山艾府：[四种方法：哈希集合/摩尔投票/邻近元素/随机（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

961.重复N次的元素

[力扣](https://leetcode-cn.com/problems/n-repeated-element-in-size-2n-array/)

这一题有各式各样的做法。

最简单的自然是使用一个dict储存每个数出现的次数，然后找出出现次数最多的。

另外也可以每次从数组中随机选一个数，然后判断这个数是否为答案。由于每次选中答案的概率都是0.5，那么在20次尝试后依然找不到答案的概率就已经低到1/1048576了，因此可以认为在有限次尝试内必然可以找到答案。

另外，可以考虑两个答案之间的间距。由于答案占所有数字的一半，那么两个连续答案之间的距离的最小值必然是小于等于2的，而这个2也只会出现在最特殊的情况即X A B X这种形式当中。证明也很简单，若当前两个连续答案之间的距离的最小值为2，为了塞下尽可能多的x，那么此时必然是形如

X A B X C D X ... X

此时就有(n / 2 - 1) \* 3 + 1 \= n，可以解得n \= 4

于是我们可以从0到2枚举二者的间距x，然后对比每个数与其间隔为x的数是否相等。若相等那么就找到了答案。

最后附上python代码：

```python
class Solution(object):
    def repeatedNTimes(self, A):
        """
        :type A: List[int]
        :rtype: int
        """

        for i in range(1, 4):
            for j in range(len(A) - i):
                if A[j] == A[j + i]:
                    return A[j]
```
