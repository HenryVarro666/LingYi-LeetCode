---
title: "769. 最多能完成排序的块"
aliases: ["yiduobo的每日leetcode 769.最多能完成排序的块"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/339375072"
zhihu_id: "339375072"
zhihu_title: "yiduobo的每日leetcode 769.最多能完成排序的块"
question_id: "769"
question: "最多能完成排序的块"
problem_url: "https://leetcode.cn/problems/max-chunks-to-make-sorted/"
created: "2020-12-24T23:35:13+08:00"
updated: "2020-12-24T23:35:13+08:00"
upvotes: 0
comments: 0
---

# 769. 最多能完成排序的块

> **[yiduobo的每日leetcode 769.最多能完成排序的块](https://zhuanlan.zhihu.com/p/339375072) · 知乎 · 2020-12-24 · 赞同 0**
> 力扣：[769. 最多能完成排序的块](https://leetcode.cn/problems/max-chunks-to-make-sorted/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

769.最多能完成排序的块

[力扣](https://leetcode-cn.com/problems/max-chunks-to-make-sorted/)

768题是769题的升级版，因此这里先做769题。

题目要求分块排序后最终的排序结果依然是0到n - 1，我们从左往右开始，首先考虑arr[0]。

对于arr[0]，其在数组中的最终位置应该就是arr[0]，那么我们至少要将0到arr[0]这一段划在一起，才能保证arr[0]能顺利归位。那么在0到arr[0]这一段当中，若所有的数都小于等于arr[0]，那么这就是一段合法的划分；若其中某个数大于arr[0]，设其为arr[x]，那么此时arr[x]必然是没法归位的，因此需要将这一段划分扩展到arr[x]，然后继续考察从arr[0] + 1到arr[x]这一段中最大的数是否小于等于arr[x]。若依然有某个数超出范围，那么就重复这个过程，直到满足条件为止。

设此时扩展到的范围是0到arr[k]，那么这k + 1个数中必然恰好是0到k，于是可以从k + 1开始继续往后进行划分。

最后附上python代码：

```python
class Solution(object):
    def maxChunksToSorted(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        res = 0
        n = len(arr)
        now = 0
        while now < n:
            end_pos = arr[now]
            max_num = 0
            while True:
                max_num = 0
                for index in range(now, end_pos + 1):
                    max_num = max(max_num, arr[index])
                if max_num == end_pos:
                    res += 1
                    now = end_pos + 1
                    break
                else:
                    end_pos = max_num
        
        return res
```
