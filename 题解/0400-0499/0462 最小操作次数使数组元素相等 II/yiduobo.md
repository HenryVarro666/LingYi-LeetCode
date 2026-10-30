---
title: "462. 最少移动次数使数组元素相等II"
aliases: ["yiduobo的每日leetcode 462.最少移动次数使数组元素相等II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/quickselect", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/222957788"
zhihu_id: "222957788"
zhihu_title: "yiduobo的每日leetcode 462.最少移动次数使数组元素相等II"
question_id: "462"
question: "最小操作次数使数组元素相等 II"
problem_url: "https://leetcode.cn/problems/minimum-moves-to-equal-array-elements-ii/"
difficulty: "Medium"
created: "2020-09-07T20:18:26+08:00"
updated: "2020-09-07T20:18:26+08:00"
upvotes: 0
comments: 0
---

# 462. 最少移动次数使数组元素相等II

> **[yiduobo的每日leetcode 462.最少移动次数使数组元素相等II](https://zhuanlan.zhihu.com/p/222957788) · 知乎 · 2020-09-07 · 赞同 0**
> 力扣：[462. 最小操作次数使数组元素相等 II](https://leetcode.cn/problems/minimum-moves-to-equal-array-elements-ii/) · Medium · 灵茶山艾府：[中位数贪心及其证明（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

462.最少移动次数使数组元素相等II <https://leetcode-cn.com/problems/minimum-moves-to-equal-array-elements-ii/>

这一题的关键在于确定所有数应该移动到哪个数上去。

首先考察两个数a、b的情况，不妨设a \< b，最终移动到x，那么移动的步数为

|a - x| + |b - x|

此时x的取值有三种情况：

1、x \< a：此时最终步数为a - x + b - x \= a + b - 2x > a + b - 2a \= b - a

2、a \<\= x \<\= b：此时最终步数为x -a + b - x \= b - a

3、b \< x：此时最终步数为x - a + x - b \= 2x - a - b > 2b - a - b \= b - a

可以发现，对比下来只有当x取值在a到b之间时消耗的步数才最少。

那么不妨设此时数组已经排好序，那么两两一组考察数组的头尾元素，就有

当取值在nums[0]到nums[-1]之间时，移动nums[0]和nums[-1]的步数之和最少

当取值在nums[1]到nums[-2]之间时，移动nums[1]和nums[-2]的步数之和最少

。。。

若数组长度为奇数，那么当取值为nums[len / 2]时，就无须移动nums[len / 2]，若数组长度为偶数，那么当取值为nums[len / 2]到nums[len / 2 + 1]之间时，移动nums[len / 2]和nums[len / 2 + 1]的步数之和最少

于是就可以得出一个结论，将所有数移动到nums[len / 2]时，所需的步数之和最少。于是题目现在就转化为了对于一个n个数的数组，如何求其中位数是多少。这个问题可以用之前215题同样的做法进行处理（传送门在这里[yiduobo：yiduobo的每日leetcode 215.数组中的第K个最大元素](https://zhuanlan.zhihu.com/p/148151993)），而这里的K就是(n + 1) / 2，最终的时间复杂度为O(n)。

最后附上python代码：

```python
import random
class Solution(object):
    def minMoves2(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        final_num = self.search(nums, 0, len(nums) - 1, (len(nums) + 1) / 2)
        res = 0
        for num in nums:
            res += abs(num - final_num)

        return res

    def search(self, nums, left, right, k):
        if left == right:
            return nums[left]

        mid = nums[(left + right) / 2]
        i = left
        j = right
        while i <= j:
            while i <= right and nums[i] < mid:
                i += 1
            while j >= left and nums[j] > mid:
                j -= 1
            if i <= j:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
                j -= 1

        if j - left + 1 >= k:
            return self.search(nums, left, j, k)
        elif i - left >= k:
            return nums[left + k - 1]
        else:
            return self.search(nums, i, right, k - (i - left))
```
