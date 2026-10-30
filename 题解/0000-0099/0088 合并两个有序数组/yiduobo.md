---
title: "88. 合并两个有序数组"
aliases: ["yiduobo的每日leetcode 88.合并两个有序数组"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/面试经典-150-题", "题单/滑动窗口与双指针/四-双序列双指针", "题单/面试经典-150-题/数组-/-字符串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/134184056"
zhihu_id: "134184056"
zhihu_title: "yiduobo的每日leetcode 88.合并两个有序数组"
question_id: "88"
question: "合并两个有序数组"
problem_url: "https://leetcode.cn/problems/merge-sorted-array/"
difficulty: "Easy"
created: "2020-04-25T20:49:18+08:00"
updated: "2020-04-25T20:49:18+08:00"
upvotes: 0
comments: 0
---

# 88. 合并两个有序数组

> **[yiduobo的每日leetcode 88.合并两个有序数组](https://zhuanlan.zhihu.com/p/134184056) · 知乎 · 2020-04-25 · 赞同 0**
> 力扣：[88. 合并两个有序数组](https://leetcode.cn/problems/merge-sorted-array/) · Easy · 灵茶山艾府：[倒序双指针：为什么倒序就一定能避免覆盖？（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

88.合并两个有序数组<https://leetcode-cn.com/problems/merge-sorted-array/>

比较基础的题目。

由于题目保证了nums1中空间充足，那么我们可以从后往前，每次将nums1[n - 1]与nums2[m - 1]中较大的数加入到nums1的now \= m + n - 1这个位置上，同时更新m、n以及now即可。

最后附上python代码：

```python
class Solution(object):
    def merge(self, nums1, m, nums2, n):
        """
        :type nums1: List[int]
        :type m: int
        :type nums2: List[int]
        :type n: int
        :rtype: None Do not return anything, modify nums1 in-place instead.
        """

        now = m + n - 1
        while now >= 0:
            if m == 0:
                nums1[now] = nums2[n - 1]
                n -= 1
            elif n == 0:
                nums1[now] = nums1[m - 1]
                m -= 1
            else:
                if nums1[m - 1] <= nums2[n - 1]:
                    nums1[now] = nums2[n - 1]
                    n -= 1
                else:
                    nums1[now] = nums1[m - 1]
                    m -= 1
            now -= 1
```
