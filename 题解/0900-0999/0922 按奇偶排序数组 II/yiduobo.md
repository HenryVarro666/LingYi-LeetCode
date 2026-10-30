---
title: "922. 按奇偶排序数组II"
aliases: ["yiduobo的每日leetcode 922.按奇偶排序数组II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/356171575"
zhihu_id: "356171575"
zhihu_title: "yiduobo的每日leetcode 922.按奇偶排序数组II"
question_id: "922"
question: "按奇偶排序数组 II"
problem_url: "https://leetcode.cn/problems/sort-array-by-parity-ii/"
difficulty: "Easy"
created: "2021-03-10T23:03:18+08:00"
updated: "2021-03-10T23:03:18+08:00"
upvotes: 1
comments: 0
---

# 922. 按奇偶排序数组II

> **[yiduobo的每日leetcode 922.按奇偶排序数组II](https://zhuanlan.zhihu.com/p/356171575) · 知乎 · 2021-03-10 · 赞同 1**
> 力扣：[922. 按奇偶排序数组 II](https://leetcode.cn/problems/sort-array-by-parity-ii/) · Easy · 灵茶山艾府：[双指针，O(1) 空间（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

922.按奇偶排序数组II

[力扣](https://leetcode-cn.com/problems/sort-array-by-parity-ii/)

维护两个指针even和odd，分别表示当前最左边的偶数位上的奇数的下标以及最左边的奇数位上的偶数的下标。当找到一组odd和even时，先交换even和odd上的数，然后继续向后寻找下一组even和odd直到数组末尾，具体为：

1、even初始化为0，当nums[even]为偶数时，则将even向后移动两位，直到nums[even]为奇数或者even到达数组末尾。

2、类似地，odd初始化为1，当nums[odd]为奇数时，则将odd向后移动两位，直到nums[odd]为偶数或者odd到达数组末尾。

3、若even和odd没有到达数组末尾，那么交换nums[even]以及nums[odd]，然后将even和odd分别向后移动两位，然后重复步骤1。

最后附上python代码：

```python
class Solution(object):
    def sortArrayByParityII(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        even = 0
        odd = 1
        while even < len(nums) and odd < len(nums):
            while even < len(nums) and nums[even] % 2 == 0:
                even += 2
            while odd < len(nums) and nums[odd] % 2 == 1:
                odd += 2
            if even < len(nums) and odd < len(nums):
                nums[even], nums[odd] = nums[odd], nums[even]
                even += 2
                odd += 2
        
        return nums
```
