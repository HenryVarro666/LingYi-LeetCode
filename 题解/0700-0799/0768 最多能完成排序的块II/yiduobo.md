---
title: "768. 最多能完成排序的块II"
aliases: ["yiduobo的每日leetcode 768.最多能完成排序的块II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/339634563"
zhihu_id: "339634563"
zhihu_title: "yiduobo的每日leetcode 768.最多能完成排序的块II"
question_id: "768"
question: "最多能完成排序的块II"
problem_url: "https://leetcode.cn/problems/max-chunks-to-make-sorted-ii/"
created: "2020-12-26T00:21:14+08:00"
updated: "2020-12-26T00:21:14+08:00"
upvotes: 0
comments: 0
---

# 768. 最多能完成排序的块II

> **[yiduobo的每日leetcode 768.最多能完成排序的块II](https://zhuanlan.zhihu.com/p/339634563) · 知乎 · 2020-12-26 · 赞同 0**
> 力扣：[768. 最多能完成排序的块II](https://leetcode.cn/problems/max-chunks-to-make-sorted-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

768.最多能完成排序的块II

[力扣](https://leetcode-cn.com/problems/max-chunks-to-make-sorted-ii/)

769题的升级版，这里可能出现重复的元素，因此需要优先进行排序，确定每个数的最低排位。这里的最低排位指的是其在排序完成的数组中所处的最靠前的位置。

得到这个位置之后，就可以沿用上一题的从头开始扩展的做法

[yiduobo：yiduobo的每日leetcode 769.最多能完成排序的块](https://zhuanlan.zhihu.com/p/339375072)

不过这里有一点不同的是，在扩展的过程中可能会遇到相同的数字，此时只需将右边界往右移动一位兼容这个相同的数字即可。

最后附上python代码：

```python
class Solution(object):
    def maxChunksToSorted(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        rate_dict = {}
        for index, num in enumerate(sorted(arr)):
            if num not in rate_dict:
                rate_dict[num] = index

        res = 0
        n = len(arr)
        now = 0
        while now < n:
            end_pos = rate_dict[arr[now]]
            max_num = arr[now]
            now += 1
            while now <= end_pos:
                if arr[now] == max_num:
                    end_pos += 1
                elif arr[now] > max_num:
                    max_num = arr[now]
                    end_pos = rate_dict[max_num]
                now += 1
            res += 1
        
        return res
```
