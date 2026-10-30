---
title: "2310. 个位数字为K的整数之和"
aliases: ["yiduobo的每日leetcode 2310.个位数字为K的整数之和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/memoization", "leetcode/math", "leetcode/enumeration", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/555768298"
zhihu_id: "555768298"
zhihu_title: "yiduobo的每日leetcode 2310.个位数字为K的整数之和"
question_id: "2310"
question: "个位数字为 K 的整数之和"
problem_url: "https://leetcode.cn/problems/sum-of-numbers-with-units-digit-k/"
difficulty: "Medium"
rating: 1559
created: "2022-08-19T23:09:14+08:00"
updated: "2022-08-19T23:09:14+08:00"
upvotes: 1
comments: 0
---

# 2310. 个位数字为K的整数之和

> **[yiduobo的每日leetcode 2310.个位数字为K的整数之和](https://zhuanlan.zhihu.com/p/555768298) · 知乎 · 2022-08-19 · 赞同 1**
> 力扣：[2310. 个位数字为 K 的整数之和](https://leetcode.cn/problems/sum-of-numbers-with-units-digit-k/) · Medium · 灵茶山艾府：[枚举答案 + 利用同余性质优化至 O(1) 时间复杂度](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2310.个位数字为K的整数之和

[力扣](https://leetcode.cn/problems/sum-of-numbers-with-units-digit-k/)

首先考虑特殊情况。当num \= 0时，0个个位数为k的整数之和就是0，此时的答案就是0。

接下来是num > 0的情况。

由于这些整数只需要个位相同而其他位上可以任意调配，那么方便起见，可以将所有高位上的数都集中到一个数中。如果问题有解的话，就一定可以写成

(p \* 10 + k) + k + k + ... + k的形式

设后面单独的k一共有cnt个，那么就是

(p \* 10 + k) + cnt \* k \= p \* 10 + (cnt + 1) \* k

在这里cnt满足0 \<\= cnt \<\= 9，因为当cnt大于等于10时，可以按10个k一组并入到p \* 10当中，于是可以从0到9枚举cnt，然后判断当前情况下是否存在合法的p，若存在说明cnt + 1就是题目的答案。若遍历完都没找到合法的cnt，就返回-1。

最后附上python代码：

```python
class Solution(object):
    def minimumNumbers(self, num, k):
        """
        :type num: int
        :type k: int
        :rtype: int
        """

        if num == 0:
            return 0
        
        for cnt in range(10):
            if num >= (cnt + 1) * k and (num - (cnt + 1) * k) % 10 == 0:
                return cnt + 1
        
        return -1
```
