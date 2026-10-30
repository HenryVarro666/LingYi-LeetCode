---
title: "1619. 删除某些元素后的数组均值"
aliases: ["yiduobo的每日leetcode 1619.删除某些元素后的数组均值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/435760210"
zhihu_id: "435760210"
zhihu_title: "yiduobo的每日leetcode 1619.删除某些元素后的数组均值"
question_id: "1619"
question: "删除某些元素后的数组均值"
problem_url: "https://leetcode.cn/problems/mean-of-array-after-removing-some-elements/"
created: "2021-11-20T23:40:37+08:00"
updated: "2021-11-20T23:40:37+08:00"
upvotes: 0
comments: 0
---

# 1619. 删除某些元素后的数组均值

> **[yiduobo的每日leetcode 1619.删除某些元素后的数组均值](https://zhuanlan.zhihu.com/p/435760210) · 知乎 · 2021-11-20 · 赞同 0**
> 力扣：[1619. 删除某些元素后的数组均值](https://leetcode.cn/problems/mean-of-array-after-removing-some-elements/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1619.删除某些元素后的数组均值

[力扣](https://leetcode-cn.com/problems/mean-of-array-after-removing-some-elements/)

由于数据规模不大，直接对arr进行排序，然后去头去尾求平均是可行的做法，时间复杂度位O(nlogn)。除此之外，还存在更好的做法。

不妨设k \= n / 20，题目就是要求去除掉arr中前k小的数以及前k大的数。那么可以先找出题目中第k小的数以及第k大的数，然后一趟遍历，根据arr中的数与这两个数的大小关系来决定是否需要去除。

当然，求解第k大的数也可以认为是求解arr中第n - k小的数，那么实际上就是需要找出一种方法可以高效求解数组中第k小的数，之前有一题恰好就是这个问题，但是记不清楚题号了。

具体做法简单来说就是利用快排选择中间数的思路，根据当前剩余数组中小于mid的数的数目以及k的大小判断第k小的数落在了mid的哪一边，然后只递归求解这一边，这样一来，就可以在O(n)的时间复杂度内找到这个数了。

最后附上python代码：

```python
class Solution(object):
    def trimMean(self, arr):
        """
        :type arr: List[int]
        :rtype: float
        """

        n = len(arr)
        k = n / 20
        l = self.search(arr, 0, n - 1, k)
        r = self.search(arr, 0, n - 1, n - k + 1)
        cnt_l = cnt_r = 0
        tot = 0.0
        for num in arr:
            if num < l:
                cnt_l += 1
            elif num > r:
                cnt_r += 1
            else:
                tot += num

        return (tot - (k - cnt_l) * l - (k - cnt_r) * r) / (n - k - k)

        
    def search(self, arr, l, r, k):
        if l == r:
            return arr[l]

        mid = arr[(l + r) / 2]
        i = l
        j = r
        while i <= j:
            while i <= r and arr[i] < mid:
                i += 1
            while j >= l and arr[j] > mid:
                j -= 1
            if i <= j:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
                j -= 1

        if j - l + 1 >= k:
            return self.search(arr, l, j, k)
        elif i - l >= k:
            return arr[l + k - 1]
        else:
            return self.search(arr, i, r, k - (i - l))
```
