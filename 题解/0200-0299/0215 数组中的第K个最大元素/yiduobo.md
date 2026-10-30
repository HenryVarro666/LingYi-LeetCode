---
title: "215. 数组中的第K个最大元素"
aliases: ["yiduobo的每日leetcode 215.数组中的第K个最大元素"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/quickselect", "leetcode/random", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/五-其他递归/分治", "题单/LeetCode-热题-100/堆", "题单/面试经典-150-题/堆"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/148151993"
zhihu_id: "148151993"
zhihu_title: "yiduobo的每日leetcode 215.数组中的第K个最大元素"
question_id: "215"
question: "数组中的第K个最大元素"
problem_url: "https://leetcode.cn/problems/kth-largest-element-in-an-array/"
difficulty: "Medium"
created: "2020-06-13T23:40:24+08:00"
updated: "2020-06-13T23:40:24+08:00"
upvotes: 1
comments: 0
---

# 215. 数组中的第K个最大元素

> **[yiduobo的每日leetcode 215.数组中的第K个最大元素](https://zhuanlan.zhihu.com/p/148151993) · 知乎 · 2020-06-13 · 赞同 1**
> 力扣：[215. 数组中的第K个最大元素](https://leetcode.cn/problems/kth-largest-element-in-an-array/) · Medium · 灵茶山艾府：[O(n) 快速选择算法，附常见问题解答（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

215.数组中的第K个最大元素<https://leetcode-cn.com/problems/kth-largest-element-in-an-array/>

最简单的做法当然是直接一趟排序然后输出第k大的数即可，不过这样做的时间复杂度是O(nlogn)的，还可以继续优化。

考虑最常见的快速排序，选择分割点后，将数组分成两个部分然后递归继续排序。很明显，我们要找的第k大的数只会属于其中某一个部分，那么，于是每次只需要递归计算其中一个部分就行了。如果分割点选择恰当的话，理论上的时间复杂度应该是O(n)的。

具体做法为：

1、选择分割点x，按快速排序的做法将数组分为两个部分，分别是小于x的部分和大于x的部分，同时可以得知这两个部分的长度l1与l2。

2、对于k与l1、l2的关系，就能知道第k大的数位于哪个部分，继续递归计算该部分即可。

我在这里方便起见用的取中快排，并不是最稳妥的做法。另外在快排的写法上对于判断等于分割点x的时候有些特殊处理，所以最后判断k所在位置时需要特别判断第k大的数就是x的情况。

最后附上python代码：

```python
class Solution(object):
    def findKthLargest(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        return self.search(nums, 0, len(nums) - 1, len(nums) - k + 1)

    def search(self, nums, left, right, k):
        #print left, right, k
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
