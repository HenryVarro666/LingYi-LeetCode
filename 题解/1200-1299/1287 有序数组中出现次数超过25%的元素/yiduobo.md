---
title: "1287. 有序数组中出现次数超过25%的元素"
aliases: ["yiduobo的每日leetcode 1287.有序数组中出现次数超过25%的元素"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/一-二分查找"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/389076726"
zhihu_id: "389076726"
zhihu_title: "yiduobo的每日leetcode 1287.有序数组中出现次数超过25%的元素"
question_id: "1287"
question: "有序数组中出现次数超过25%的元素"
problem_url: "https://leetcode.cn/problems/element-appearing-more-than-25-in-sorted-array/"
difficulty: "Easy"
created: "2021-07-12T22:42:49+08:00"
updated: "2021-07-12T22:42:49+08:00"
upvotes: 0
comments: 0
---

# 1287. 有序数组中出现次数超过25%的元素

> **[yiduobo的每日leetcode 1287.有序数组中出现次数超过25%的元素](https://zhuanlan.zhihu.com/p/389076726) · 知乎 · 2021-07-12 · 赞同 0**
> 力扣：[1287. 有序数组中出现次数超过25%的元素](https://leetcode.cn/problems/element-appearing-more-than-25-in-sorted-array/) · Easy · 灵茶山艾府：[O(log n) 做法，只需两次二分查找（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1287.有序数组中出现次数超过25%的元素

[力扣](https://leetcode-cn.com/problems/element-appearing-more-than-25-in-sorted-array/)

注意到题目给出的数组已经排好序了，那么说明相等的元素在数组中是连续的，因此可以记录下当前统计的元素值now以及该元素出现的次数cnt，然后从头开始一趟扫描，对于当前元素num，若now等于num，那么将cnt加上1，否则将now置为num，并将cnt重置为1。

若某一时刻cnt \* 4大于数组长度，说明now就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def findSpecialInteger(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        n = len(arr)
        if n == 1:
            return arr[0]
        now = arr[0]
        cnt = 1
        for num in arr[1:]:
            if now == num:
                cnt += 1
                if cnt * 4 > n:
                    return now
            else:
                now = num
                cnt = 1
```
