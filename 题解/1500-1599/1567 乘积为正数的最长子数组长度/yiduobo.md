---
title: "1567. 乘积为正数的最长子数组长度"
aliases: ["yiduobo的每日leetcode 1567.乘积为正数的最长子数组长度"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/428317290"
zhihu_id: "428317290"
zhihu_title: "yiduobo的每日leetcode 1567.乘积为正数的最长子数组长度"
question_id: "1567"
question: "乘积为正数的最长子数组长度"
problem_url: "https://leetcode.cn/problems/maximum-length-of-subarray-with-positive-product/"
created: "2021-11-02T00:22:28+08:00"
updated: "2021-11-02T00:22:28+08:00"
upvotes: 0
comments: 0
---

# 1567. 乘积为正数的最长子数组长度

> **[yiduobo的每日leetcode 1567.乘积为正数的最长子数组长度](https://zhuanlan.zhihu.com/p/428317290) · 知乎 · 2021-11-02 · 赞同 0**
> 力扣：[1567. 乘积为正数的最长子数组长度](https://leetcode.cn/problems/maximum-length-of-subarray-with-positive-product/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1567.乘积为正数的最长子数组长度

[力扣](https://leetcode-cn.com/problems/maximum-length-of-subarray-with-positive-product/)

由于题目要求最终乘积为正数，因此零必然不能出现在答案当中，也可以认为令将原始数组划分成了若干不含零的子数组，需要对这些子数组分别求其中乘积为正数的最长子数组长度，而最终答案就是其中长度的最大值。

接下来考察如何处理不含零的数组。为了使得最终答案为正数，因此最终答案中含有的负数数目必须为偶数个，那么这里可以看做是某种特殊的前缀问题。即对于数组中的某段前缀，若其中负数的个数为偶数个，那么这段前缀的乘积就是正数；若其中负数的个数为奇数个，那么只需要排除掉以数组中首个奇数所在位置为结尾的前缀，那么剩下的子数组中含有的负数个数就是偶数个了。于是可以一趟扫描，记录下当前前缀中负数的个数cnt，以及奇数首次出现的下标neg_pos，那么对于当前位置index而言：

1、若当前位置上的数为偶数，那么无需更新cnt。若cnt为偶数，说明当前前缀就是一个备选答案，此时应该使用index来更新答案；若cnt为奇数，说明需要排除掉首个奇数，因此使用index - neg_pos + 1来更新答案。

2、若当前位置是的数为奇数，那么应当将cnt加上1。同样地，若cnt为偶数，则使用index来更新答案；当cnt为奇数时则略有不同，此时还需要额外考虑仅有index位置上这一个奇数的情况，即cnt等于1的情况。此时无法找出以index为结尾的合法子数组，因此无需更新答案，但是需要将neg_pos更新为index。若cnt大于1，则与情况1类似，同样是排除掉首个奇数，使用index - neg_pos + 1来更新答案。

我在具体实现时没有真正对数组进行分离，而是储存了当前子数组的起点，此时需要特别注意边界上的加一或者减一不要弄错了。

最后附上python代码：

```python
class Solution(object):
    def getMaxLen(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        neg_pos = None
        cnt = 0
        res = 0
        l = -1
        for index, num in enumerate(nums):
            if num == 0:
                neg_pos = None
                cnt = 0
                l = index
            elif num > 0:
                if cnt % 2 == 0:
                    res = max(res, index - l)
                else:
                    res = max(res, index - neg_pos)
            else:
                cnt += 1
                if cnt % 2 == 0:
                    res = max(res, index - l)
                elif cnt == 1:
                    neg_pos = index
                else:
                    res = max(res, index - neg_pos)
        
        return res
```
