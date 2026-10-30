---
title: "2459. 通过移动项目到空白区域来排序数组"
aliases: ["yiduobo的每日leetcode 2459.通过移动项目到空白区域来排序数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/631990003"
zhihu_id: "631990003"
zhihu_title: "yiduobo的每日leetcode 2459.通过移动项目到空白区域来排序数组"
question_id: "2459"
question: "通过移动项目到空白区域来排序数组"
problem_url: "https://leetcode.cn/problems/sort-array-by-moving-items-to-empty-space/"
created: "2023-05-25T03:25:48+08:00"
updated: "2023-05-25T03:25:48+08:00"
upvotes: 0
comments: 0
---

# 2459. 通过移动项目到空白区域来排序数组

> **[yiduobo的每日leetcode 2459.通过移动项目到空白区域来排序数组](https://zhuanlan.zhihu.com/p/631990003) · 知乎 · 2023-05-25 · 赞同 0**
> 力扣：[2459. 通过移动项目到空白区域来排序数组](https://leetcode.cn/problems/sort-array-by-moving-items-to-empty-space/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2459.通过移动项目到空白区域来排序数组

[力扣](https://leetcode.cn/problems/sort-array-by-moving-items-to-empty-space/)

不妨先考虑题目的简化版本：如果不需要通过空白区域来交换数字的话应该怎么计算交换次数。

对于没有处于正确位置上的数，其占位路径必然能形成一个环，例如a的位置被b占据了，b的位置被c占据了，这样类推下去最终一定会回到某个数的位置被a占据了。对于这样一个环，若其长度为k，那么需要的交换次数就是k - 1。

回到本题。由于交换需要环中包含空白区域，因此对于一个长度为k的环，若其包含空白区域，那么其交换次数不变，依然是k - 1；若其不包含空白区域，就需要先进行一次额外操作，将环中某个数与空白区域交换，在完成其他数字的交换后再将其换回来，因此其所需的交换次数就是在k - 1的基础上再加上2，也就是k + 1。

根据这个结论，就只需找出数组中所有的错位环，然后根据环的长度以及0所在的位置更新答案了。

另外需要注意的是，题目的合法排列可以是从0到n - 1，或者显示1到n - 1，然后最后为0。对于这两种方案需要分开进行处理，而具体的处理方法依照上面算法描述的进行就可以了。

最后附上python代码：

```python
class Solution(object):
    def sortArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)

        def check():
            vis = set()
            cnt = 0
            zero_flag = False

            for index in range(n):
                if index not in vis and target[nums[index]] != index:
                    vis.add(index)
                    cnt += 1
                    p = target[nums[index]]
                    while p not in vis:
                        vis.add(p)
                        p = target[nums[p]]
                        cnt += 1
                    
                    if not zero_flag and target[0] in vis:
                        cnt -= 1
                        zero_flag = True
                    else:
                        cnt += 1                        

            return cnt

        target = {}
        for index in range(n):
            target[index] = index
        res = check()

        for index in range(1, n):
            target[index] = index - 1
        target[0] = n - 1
        res = min(res, check())

        return res
```
