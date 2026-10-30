---
title: "1054. 距离相等的条形码"
aliases: ["yiduobo的每日leetcode 1054.距离相等的条形码"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/372115473"
zhihu_id: "372115473"
zhihu_title: "yiduobo的每日leetcode 1054.距离相等的条形码"
question_id: "1054"
question: "距离相等的条形码"
problem_url: "https://leetcode.cn/problems/distant-barcodes/"
created: "2021-05-13T21:39:15+08:00"
updated: "2021-05-13T21:39:15+08:00"
upvotes: 0
comments: 0
---

# 1054. 距离相等的条形码

> **[yiduobo的每日leetcode 1054.距离相等的条形码](https://zhuanlan.zhihu.com/p/372115473) · 知乎 · 2021-05-13 · 赞同 0**
> 力扣：[1054. 距离相等的条形码](https://leetcode.cn/problems/distant-barcodes/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1054.距离相等的条形码

[力扣](https://leetcode-cn.com/problems/distant-barcodes/)

之前似乎也做过类似的题目。为了使得相同的条形码不相邻，那么我们每一轮都应该尽可能地使用掉当前剩下条形码中数目最多的那一种。当然，不能连续两次都是用同样的条形码，因此可以两个条形码为一组，每次从条形码中选出剩余数量最多以及第二多我的那两种即可。

一个简单的证明是对于当前选择的这一组条形码(A, B)，下一次选择时B的数量是不可能超过A的数量的，因此无需担心下一次选择时选出形如(B, X)的条形码对。由于题目保证有解，因此这个做法是成立的。

具体实现上，可以使用一个堆维护每种条形码的数量，若堆的大小大于等于2，那么将堆中最大的两个数弹出，将对应的条形码加入答案之后将这个数目减1，若数目不为0则将其再重新加入到堆中。

最后附上python代码：

```python
class Solution(object):
    def rearrangeBarcodes(self, barcodes):
        """
        :type barcodes: List[int]
        :rtype: List[int]
        """

        num_dict = {}
        for num in barcodes:
            num_dict[num] = num_dict.get(num, 0) + 1
        
        heap = [[-x[1], x[0]] for x in num_dict.items()]
        heapq.heapify(heap)

        res = []
        while heap:
            if len(heap) < 2:
                res.append(heap[0][1])
                break
            
            cnt1, num1 = heapq.heappop(heap)
            cnt2, num2=  heapq.heappop(heap)
            res.append(num1)
            res.append(num2)

            cnt1 += 1
            if cnt1 < 0:
                heapq.heappush(heap, [cnt1, num1])
            
            cnt2 += 1
            if cnt2 < 0:
                heapq.heappush(heap, [cnt2, num2])
        
        return res
```
