---
title: "704. 二分查找"
aliases: ["yiduobo的每日leetcode 704.二分查找"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/一-二分查找"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/320153798"
zhihu_id: "320153798"
zhihu_title: "yiduobo的每日leetcode 704.二分查找"
question_id: "704"
question: "二分查找"
problem_url: "https://leetcode.cn/problems/binary-search/"
difficulty: "Easy"
created: "2020-11-29T18:50:49+08:00"
updated: "2020-11-29T18:50:49+08:00"
upvotes: 0
comments: 0
---

# 704. 二分查找

> **[yiduobo的每日leetcode 704.二分查找](https://zhuanlan.zhihu.com/p/320153798) · 知乎 · 2020-11-29 · 赞同 0**
> 力扣：[704. 二分查找](https://leetcode.cn/problems/binary-search/) · Easy · 灵茶山艾府：[二分查找总是写不对？一个视频讲透！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

704.二分查找

[力扣](https://leetcode-cn.com/problems/binary-search/)

没有任何变形的二分查找问题，直接按经典的做法来做即可。

最后附上python代码：

```python
class Solution(object):
    def search(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """

        l = 0
        r = len(nums) - 1
        while l <= r:
            mid = (l + r) >> 1
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                l = mid + 1
            else:
                r = mid - 1
        
        return -1
```
