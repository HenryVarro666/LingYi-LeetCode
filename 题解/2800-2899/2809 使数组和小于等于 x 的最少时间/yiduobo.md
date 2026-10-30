---
title: "2809. 使数组和小于等于x的最少时间"
aliases: ["yiduobo的每日leetcode 2809.使数组和小于等于x的最少时间"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/math", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/657929690"
zhihu_id: "657929690"
zhihu_title: "yiduobo的每日leetcode 2809.使数组和小于等于x的最少时间"
question_id: "2809"
question: "使数组和小于等于 x 的最少时间"
problem_url: "https://leetcode.cn/problems/minimum-time-to-make-array-sum-at-most-x/"
difficulty: "Hard"
rating: 2979
created: "2023-09-23T07:03:48+08:00"
updated: "2023-09-23T07:03:48+08:00"
upvotes: 1
comments: 0
---

# 2809. 使数组和小于等于x的最少时间

> **[yiduobo的每日leetcode 2809.使数组和小于等于x的最少时间](https://zhuanlan.zhihu.com/p/657929690) · 知乎 · 2023-09-23 · 赞同 1**
> 力扣：[2809. 使数组和小于等于 x 的最少时间](https://leetcode.cn/problems/minimum-time-to-make-array-sum-at-most-x/) · Hard · 灵茶山艾府：[教你一步步思考本题！（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2809.使数组和小于等于x的最少时间

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-time-to-make-array-sum-at-most-x/description/)

首先可以明确几点：

1、同一个位置上不会进行多次清空操作，这是因为情况会让数组值变为0，这也就意味着前面的情况操作是无效的，而每过一秒数组和必然是越来越大，这就相当于浪费了前面的清空操作

2、基于上面这一点，就可以确定如果存在答案t，那么t一定是小于等于n的，也就是最多让数组中每个位置都情况一次，因此就可以枚举这个最后答案t，计算在时刻t最小的数组和是多少

3、对于时刻t的最小数组和，实际上就是要找出t个执行清空操作的位置p[1]、p[1]、...、p[t]，使得式子

(nums1\[p\[1\]\] + nums2\[p\[1\]\]) + (nums1\[p\[2\]\] + nums2\[p\[2\]\] \* 2) + ... + (nums1\[p\[t\]\] + nums2\[p\[t\]\] \* t)

的值最大。将式子整理一下，就是

(nums1\[p\[1\]\] + nums1\[p\[2\]\] + ... + nums1\[p\[t\]\]) + (nums2\[p\[1\]\] + nums2\[p\[2\]\] \* 2 + ... + nums2\[p\[t\]\] \* t)

这个式子分为两个部分，其中前面部分取决于选择的p的位置，而后面的部分则隐藏了一个结论，就是nums2\[p\[1\]\] \<\= nums2\[p\[2\]\] \<\= ... \<\= nums2\[p\[t\]\]。若有两个位置不满足这个不等式，那么只需交换这两个位置，此时前半部分的值不变，后半部分则会变得更大，因此是更优的。对应到具体的操作上也很好理解，就是表示nums2小的先清空，num2大的后清空。

根据上面这几点，就可以先将nums1和nums2综合起来按照nums2的值从小到大进行排序，然后通过动态规划计算出在时刻t清空t的位置的最大和。令f[i][j]表示前i个位置中，清空j个位置的收益，那么首先有边界f[i][0] \= 0，也就是一个都不清空的情况。接下来对于j > 0的f[i][j]：

1、可以不清空第i个位置，那么就有f[i][j] \= max(f[i][j], f[i - 1][j])

2、如果选择清空第i个位置，由于这个位置的nums2目前是最大的，因此必然是在最后一轮情况nums2[i]，这也就意味着是在第j轮清空的位置i，于是就有f[i][j] \= max(f[i][j], f[i - 1][j - 1] + nums1[i] + nums2[i] \* j)

计算完成后，从1到n枚举最终答案t，那么在时刻t数组之和就应该是sum(nums1) + sum(nums2) \* t - f[n][t]，若某一时刻t对应的数组和小于等于x，那么t就是答案。若不存在这样的t，那么说明无解，返回-1即可。

另外，注意到f的状态只与上一轮有关，因此在这里可以通过倒序更新省去i这一维。

最后附上python代码：

```python
class Solution(object):
    def minimumTime(self, nums1, nums2, x):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :type x: int
        :rtype: int
        """

        sorted_nums = sorted(zip(nums2, nums1))
        f = [0] * (len(sorted_nums) + 1)
        for i, (new, old) in enumerate(sorted_nums):
            for j in range(i + 1, 0, -1):
                f[j] = max(f[j], f[j - 1] + old + new * j)
        
        now = sum(nums1)
        s = sum(nums2)
        for index, v in enumerate(f):
            if now - v <= x:
                return index
            now += s
        
        return -1
```
