---
title: "3769. 二进制反射排序"
aliases: ["yiduobo的每日leetcode 3769.二进制反射排序"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/sorting", "题单/位运算", "题单/位运算/一-基础题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1981133347578221751"
zhihu_id: "1981133347578221751"
zhihu_title: "yiduobo的每日leetcode 3769.二进制反射排序"
question_id: "3769"
question: "二进制反射排序"
problem_url: "https://leetcode.cn/problems/sort-integers-by-binary-reflection/"
difficulty: "Easy"
rating: 1364
created: "2025-12-09T21:05:09+08:00"
updated: "2025-12-09T21:05:10+08:00"
upvotes: 1
comments: 0
---

# 3769. 二进制反射排序

> **[yiduobo的每日leetcode 3769.二进制反射排序](https://zhuanlan.zhihu.com/p/1981133347578221751) · 知乎 · 2025-12-09 · 赞同 1**
> 力扣：[3769. 二进制反射排序](https://leetcode.cn/problems/sort-integers-by-binary-reflection/) · Easy · 灵茶山艾府：[库函数写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3769.二进制反射排序

[3769. 二进制反射排序 - 力扣（LeetCode）](https://leetcode.cn/problems/sort-integers-by-binary-reflection/description/)

题目给出一个整数数组nums。

二进制反射指的是对于一个正整数，将其二进制表示按顺序反转，然后将得到的二进制数转换为十进制的结果。

现在要求按nums中每个元素的二进制反射值的升序对数组进行排序，如果反射值相同，则按原数字大小排序。

问排序后的nums是什么。

先对nums一趟遍历，按照题目描述计算出每个nums[index]对应的反射值r[index]，接下来以r[index]为第一关键字，nums[index]为第二关键字对nums进行排序即可。

最后附上python代码：

```python
class Solution(object):
    def sortByReflection(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        
        r = {}
        for v in set(nums):
            digits = []
            x = v
            while x:
                digits.append(x % 2)
                x //= 2
            
            x = 0
            for d in digits:
                x = x * 2 + d
            
            r[v] = x
        
        return sorted(nums, key=lambda d:(r[d], d))
```
