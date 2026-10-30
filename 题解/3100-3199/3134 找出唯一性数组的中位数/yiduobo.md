---
title: "3134. 找出唯一性数组的中位数"
aliases: ["yiduobo的每日leetcode 3134.找出唯一性数组的中位数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/binary-search", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/二分算法", "题单/滑动窗口与双指针/二-不定长滑动窗口", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/702526240"
zhihu_id: "702526240"
zhihu_title: "yiduobo的每日leetcode 3134.找出唯一性数组的中位数"
question_id: "3134"
question: "找出唯一性数组的中位数"
problem_url: "https://leetcode.cn/problems/find-the-median-of-the-uniqueness-array/"
difficulty: "Hard"
rating: 2451
created: "2024-06-10T01:09:42+08:00"
updated: "2024-06-10T01:09:42+08:00"
upvotes: 1
comments: 0
---

# 3134. 找出唯一性数组的中位数

> **[yiduobo的每日leetcode 3134.找出唯一性数组的中位数](https://zhuanlan.zhihu.com/p/702526240) · 知乎 · 2024-06-10 · 赞同 1**
> 力扣：[3134. 找出唯一性数组的中位数](https://leetcode.cn/problems/find-the-median-of-the-uniqueness-array/) · Hard · 灵茶山艾府：[二分答案+滑动窗口（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3134.找出唯一性数组的中位数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-median-of-the-uniqueness-array/description/)

题目给出一个数组nums，接下来对于nums的所有非空子数组，将每个子数组中不同元素的数量收集起来，然后从小到大排序，形成一个新的数组，称之唯一性数组。问这个唯一性数组的中位数是多少。中位数指的是唯一性数组正中间的元素，如果唯一性数组的长度为偶数，那么选择正中间那两个数中较小的那个作为中位数。

不妨设nums的长度为n，那么对于nums的所有子数组，其中有n个长度为1的子数组，n - 1个长度为2的子数组，...，1个长度为n的子数组，因此一共有m \= (1 + n) \* n // 2个子数组。由于n的规模很大，因此逐个枚举这m个子数组并计算不同元素的数组从而得到唯一性数组是行不通的，必须进行优化。

由于m已经确定，那么唯一性数组的中位数对应的下标也可以确定。更进一步的，唯一性数组中大于等于中位数的元素数目必然要大于等于m // 2，也就是说在这里可以尝试利用二分法来寻找这个中位数。对于当前的mid，检测唯一性数组中大于等于mid的元素数目是否大于等于m // 2，如果不满足，那么说明当前的mid太大了，需要修改二分的上界为mid - 1，否则需要修改二分的下界为mid。

接下来的问题如何计算唯一性数组中大于等于mid的元素数目。对于这个问题，实际上问的是nums中有多少个不同元素数目大于等于mid的子数组，而对于这个问题，则可以参考之前的340题，采用变长滑动窗口进行求解。

对于每一轮操作，先向右移动窗口右边界p，直到p来到数组末尾或者窗口nums[index : p]中包含mid个不同元素为止，那么所有左边界为index，右边界处于p - 1到n - 1之间的子数组中包含的不同元素数目都大于等于mid，即一共有n - p + 1个合法的子数组。最后，将左边界index向后移动，然后继续考虑下一轮操作即可。

最后附上python代码：

```python
class Solution(object):
    def medianOfUniquenessArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        m = (n + 1) * n // 2

        left = 1
        right = n

        while left < right:
            mid = (left + right + 1) // 2
            freq = {}
            p = 0
            cnt = 0

            for index, v in enumerate(nums):
                while p < n and len(freq) < mid:
                    freq[nums[p]] = freq.get(nums[p], 0) + 1
                    p += 1

                if len(freq) < mid:
                    break

                cnt += n - p + 1
                freq[v] -= 1
                if freq[v] == 0:
                    freq.pop(v)

            if cnt <= m // 2:
                right = mid - 1
            else:
                left = mid
        
        return left
```
