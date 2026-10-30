---
title: "1095. 山脉数组中查找目标值"
aliases: ["yiduobo的每日leetcode 1095.山脉数组中查找目标值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/array", "leetcode/binary-search", "leetcode/interactive", "题单/二分算法", "题单/贪心算法", "题单/二分算法/四-其他", "题单/贪心算法/七-交互题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/373973482"
zhihu_id: "373973482"
zhihu_title: "yiduobo的每日leetcode 1095.山脉数组中查找目标值"
question_id: "1095"
question: "山脉数组中查找目标值"
problem_url: "https://leetcode.cn/problems/find-in-mountain-array/"
difficulty: "Hard"
rating: 1827
created: "2021-05-20T22:25:16+08:00"
updated: "2021-05-20T22:25:16+08:00"
upvotes: 0
comments: 0
---

# 1095. 山脉数组中查找目标值

> **[yiduobo的每日leetcode 1095.山脉数组中查找目标值](https://zhuanlan.zhihu.com/p/373973482) · 知乎 · 2021-05-20 · 赞同 0**
> 力扣：[1095. 山脉数组中查找目标值](https://leetcode.cn/problems/find-in-mountain-array/) · Hard · 灵茶山艾府：[Go 库函数二分](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1095.山脉数组中查找目标值

[力扣](https://leetcode-cn.com/problems/find-in-mountain-array/)

我们可以将山脉数组视为一个凸的函数，有一种经典做法用来寻找这个最值点，称为三分查找。顾名思义，就是在二分查找的基础上，再使用mid和l或者r来进行一次二分，通过判断f[mid]以及f[mid']的大小来修正l和r，从而快速找到最值点。

确定最值点之后，设为p，那么只需要l到p之间进行二分查找，若找到target，那么就返回对应的index，否则还需要再p到r之间再进行二分查找，若找到target那么就返回对应的index，否则返回-1。

由于这里数组长度只有10000，而可以查100次，那么使用二分是绰绰有余的。

最后附上python代码：

```python
# """
# This is MountainArray's API interface.
# You should not implement it, or speculate about its implementation
# """
#class MountainArray(object):
#    def get(self, index):
#        """
#        :type index: int
#        :rtype int
#        """
#
#    def length(self):
#        """
#        :rtype int
#        """

class Solution(object):
    def findInMountainArray(self, target, mountain_arr):
        """
        :type target: integer
        :type mountain_arr: MountainArray
        :rtype: integer
        """

        n = mountain_arr.length()

        l = 0
        r = n - 1
        peak = None
        while l < r - 1:
            mid = (l + r) / 2
            mid_tmp = (mid + r) / 2
            mid_v = mountain_arr.get(mid - 1)
            mid_tmp_v = mountain_arr.get(mid)
            if mid_v > mid_tmp_v:
                r = mid_tmp
            else:
                l = mid
        
        l_v = mountain_arr.get(l)
        r_v = mountain_arr.get(r)
        if l_v > r_v:
            if l_v == target:
                return l
            elif l_v < target:
                return -1
            peak = l
        else:
            if r_v == target:
                return r
            elif l_v < target:
                return -1
            peak = r

        l = 0
        r = peak - 1
        while l <= r:
            mid = (l + r) / 2
            v = mountain_arr.get(mid)
            if v == target:
                return mid
            elif v < target:
                l = mid + 1
            else:
                r = mid - 1

        l = peak + 1
        r = n - 1
        while l <= r:
            mid = (l + r) / 2
            v = mountain_arr.get(mid)
            if v == target:
                return mid
            elif v < target:
                r = mid - 1
            else:
                l = mid + 1
        
        return -1
```
