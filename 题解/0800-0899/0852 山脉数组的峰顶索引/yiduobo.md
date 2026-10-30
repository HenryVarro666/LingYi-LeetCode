---
title: "852. 山脉数组的顶峰索引"
aliases: ["yiduobo的每日leetcode 852.山脉数组的顶峰索引"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/四-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/348646801"
zhihu_id: "348646801"
zhihu_title: "yiduobo的每日leetcode 852.山脉数组的顶峰索引"
question_id: "852"
question: "山脉数组的峰顶索引"
problem_url: "https://leetcode.cn/problems/peak-index-in-a-mountain-array/"
difficulty: "Medium"
created: "2021-02-02T23:53:53+08:00"
updated: "2021-02-02T23:53:53+08:00"
upvotes: 0
comments: 0
---

# 852. 山脉数组的顶峰索引

> **[yiduobo的每日leetcode 852.山脉数组的顶峰索引](https://zhuanlan.zhihu.com/p/348646801) · 知乎 · 2021-02-02 · 赞同 0**
> 力扣：[852. 山脉数组的峰顶索引](https://leetcode.cn/problems/peak-index-in-a-mountain-array/) · Medium · 灵茶山艾府：[二分，根据上坡还是下坡判断峰顶位置（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

852.山脉数组的顶峰索引

[力扣](https://leetcode-cn.com/problems/peak-index-in-a-mountain-array/)

O(n)的算法是很容想到的，直接从左到右一趟扫描，找到第一个满足a[i] > a[i + 1]的i即可，不过这里也存在更好的O(logn)的做法。

对于数组中的任意位置a[index]，若a[index] \< a[index + 1]，那么说明index处于山脉的上升部分，因此index以及之前的位置都不可能是答案。同理，若a[index] > a[index + 1]，那么说明index + 1这个位置处于山脉的下降部分，因此index + 1以及之后的位置都不可能是答案。可以发现，通过一次比较我们每次都可以按index为界排除掉一边，于是很自然可以想到二分。每次对于二分的mid，若a[mid] \< a[mid + 1]，那么排除mid以及之前的部分，于是有l \= mid + 1，否则排除掉mid + 1以及之后的部分，于是又r \= mid。

最后附上python代码：

```python
class Solution(object):
    def peakIndexInMountainArray(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        l = 0
        r = len(arr) - 1
        while l < r:
            mid = (l + r) / 2
            if arr[mid] < arr[mid + 1]:
                l = mid + 1
            else:
                r = mid
        
        return l
```
