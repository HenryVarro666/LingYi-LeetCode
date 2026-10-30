---
title: "1. 两数之和"
aliases: ["yiduobo的每日leetcode 1.两数之和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/enumeration", "题单/常用数据结构", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/常用数据结构/零-常用枚举技巧", "题单/LeetCode-热题-100/哈希", "题单/面试经典-150-题/哈希表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/112037601"
zhihu_id: "112037601"
zhihu_title: "yiduobo的每日leetcode 1.两数之和"
question_id: "1"
question: "两数之和"
problem_url: "https://leetcode.cn/problems/two-sum/"
difficulty: "Easy"
created: "2020-03-09T22:40:38+08:00"
updated: "2020-03-10T21:07:56+08:00"
upvotes: 2
comments: 0
---

# 1. 两数之和

> **[yiduobo的每日leetcode 1.两数之和](https://zhuanlan.zhihu.com/p/112037601) · 知乎 · 2020-03-09 · 赞同 2**
> 力扣：[1. 两数之和](https://leetcode.cn/problems/two-sum/) · Easy · 灵茶山艾府：[【动画】从两数之和中，我们可以学到什么？（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1.两数之和<https://leetcode-cn.com/problems/two-sum/>

## **O(n^2)的做法**

直接二重循环判断两数的和是否符合要求就行了。

## O(nlogn)的做法

O(nlogn)的做法利用到了有序数组的性质。

对于一个**数字从小到大排列**的数组a，我们从i \= 0， j \= len - 1开始考察，不妨设答案两数为x，y，且x\<\=y，那么一定满足a[i] \<\= x \<\= y \<\= a[j]。

现在比较a[i] + a[j]与target：

**情况1，**a[i] + a[j] \= target**：**

此时的a[i]即为x，a[j]即为y。

**情况2，** a[i] + a[j] \< target**：**

由y \<\= a[j]得出a[i] + y \<\= a[i] + a[j]，那么接下来有

a[i] + y \<\= a[i] + a[j] \< target \= x + y，可以得出a[i] \< x，因此一定满足a[i + 1] \<\= x \<\= y \<\= a[j]，接下来继续考察a[i + 1] + a[j]。

**情况3，** a[i] + a[j] > target**：**

由x >\= a[i]得出x + a[j] >\= a[i] + a[j]，那么接下来有

x + a[j] >\= a[i] + a[j] > target \= x + y， 可以得出a[j] > y，因此一定满足a[i] \<\= x \<\= y \<\= a[j - 1]，接下来继续考察a[i] + a[j - 1]。

可以发现，每次比较，可以认为是**从i到j中找出两个满足条件的数**，变成了**i + 1到j中，或者i到j - 1中找出两个满足条件的数**。每次比较问题的规模减少1，因此比较的过程的为O(n)，加上排序的复杂度O(nlogn)，因此最终的时间复杂度为O(nlogn)。

最后附上python的代码：

```python
class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        sorted_list = sorted([[x, index] for index, x in enumerate(nums)], key=lambda d:d[0])
        left = 0
        right = len(sorted_list) - 1
        while True:
            if sorted_list[left][0] + sorted_list[right][0] == target:
                return[sorted_list[left][1], sorted_list[right][1]]
            elif sorted_list[left][0] + sorted_list[right][0] > target:
                right -= 1
            else:
                left += 1
```
