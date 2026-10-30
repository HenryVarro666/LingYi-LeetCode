---
title: "3524. 求出数组的X值I"
aliases: ["yiduobo的每日leetcode 3524.求出数组的X值I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1902571292093289698"
zhihu_id: "1902571292093289698"
zhihu_title: "yiduobo的每日leetcode 3524.求出数组的X值I"
question_id: "3524"
question: "求出数组的 X 值 I"
problem_url: "https://leetcode.cn/problems/find-x-value-of-array-i/"
difficulty: "Medium"
rating: 2008
created: "2025-05-10T19:49:40+08:00"
updated: "2025-05-10T19:49:40+08:00"
upvotes: 0
comments: 0
---

# 3524. 求出数组的X值I

> **[yiduobo的每日leetcode 3524.求出数组的X值I](https://zhuanlan.zhihu.com/p/1902571292093289698) · 知乎 · 2025-05-10 · 赞同 0**
> 力扣：[3524. 求出数组的 X 值 I](https://leetcode.cn/problems/find-x-value-of-array-i/) · Medium · 灵茶山艾府：[子数组 DP + 刷表法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3524.求出数组的X值I

[3524. 求出数组的 X 值 I - 力扣（LeetCode）](https://leetcode.cn/problems/find-x-value-of-array-i/description/)

题目给出一个由正整数组成的数组nums，以及一个正整数k。其中nums的长度不超过10^5，其中元素值的取值范围在1到10^9之间，同时k的取值范围在1到5之间。

接下来可以对nums执行一次操作，移除掉任意不重叠的前缀和后缀，移除的前缀或后缀可以为空，但是要求移除后的nums非空。

要求找出所有的nums的x值，x值指的是剩余的nums中元素的乘积模k的余数为x的移除方案数。

返回一个大小为k的数组result，其中result[x]表示nums的x值。

题目中描述的操作，实际上就是取出nums中的某个子数组，因此题目实际上问的是nums中有多少个子数组，其乘积模k的结果为x。

由于题目中k的取值范围不大，因此可以直接使用动态规划进行求解。

令f[index][x]表示以nums[index]结尾的子数组中，乘积模k余x的子数组数量是多少。那么对于f[index]：

1、首先需要初始化所有的f[index][x]为0

2、接下来可以将f[index][nums[index] % k]加上1，表示nums[index]这个元素单独形成的子数组

3、另外，也可以尝试将nums[index]接在以nums[index - 1]结束的子数组后面，因此在这里还需要枚举f[index - 1]中的所有x，那么就可以将f[index - 1][x]累加到f[index][x \* nums[index] % k]中

得到f[index]后，将其中的每一项分别累加到答案中即可。

另外注意到f的每一轮结果都只与上一轮有关，因此在这里可以使用滚动数组优化掉index这一维。

最后附上python代码：

```python
class Solution(object):
    def resultArray(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        
        f = [0] * k
        res = [0] * k
        for v in nums:
            g = f[:]
            f = [0] * k
            f[v % k] += 1
            for x, pre in enumerate(g):
                f[x * v % k] += pre
        
            for x in range(k):
                res[x] += f[x]

        return res
```
