---
title: "3270. 求出数字答案"
aliases: ["yiduobo的每日leetcode 3270.求出数字答案"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/764994136"
zhihu_id: "764994136"
zhihu_title: "yiduobo的每日leetcode 3270.求出数字答案"
question_id: "3270"
question: "求出数字答案"
problem_url: "https://leetcode.cn/problems/find-the-key-of-the-numbers/"
difficulty: "Easy"
created: "2024-09-30T00:47:06+08:00"
updated: "2024-09-30T00:47:06+08:00"
upvotes: 1
comments: 1
---

# 3270. 求出数字答案

> **[yiduobo的每日leetcode 3270.求出数字答案](https://zhuanlan.zhihu.com/p/764994136) · 知乎 · 2024-09-30 · 赞同 1**
> 力扣：[3270. 求出数字答案](https://leetcode.cn/problems/find-the-key-of-the-numbers/) · Easy · 灵茶山艾府：[遍历数位，不用字符串（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3270.求出数字答案

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-key-of-the-numbers/description/)

题目给出三个正整数nums1、nums2、nums3，要求构造出一个4位数key，key的每一位都是nums1、nums2、nums3对应数位的最小值，若数位不够则视为补充了前导0。

直接从高到低将三个数逐位分离，取最小值拼接就行了。具体实现上，可以按1000、100、10、1的顺序遍历，对于当前遍历到的数值d，通过先除以d后对d取模的操作可以分离出nums1、nums2、nums3对应的数位以及剩余的数，取对应数位中的最小值再乘以d，累加后即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def generateKey(self, num1, num2, num3):
        """
        :type num1: int
        :type num2: int
        :type num3: int
        :rtype: int
        """

        res = 0
        for d in [1000, 100, 10, 1]:
            res += d * min(num1 // d, num2 // d, num3 // d)
            num1 %= d
            num2 %= d
            num3 %= d
        
        return res
```
