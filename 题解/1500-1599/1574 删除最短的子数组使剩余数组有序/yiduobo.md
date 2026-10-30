---
title: "1574. 删除最短的子数组使剩余数组有序"
aliases: ["yiduobo的每日leetcode 1574.删除最短的子数组使剩余数组有序"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/sliding-window", "leetcode/tu-jie", "leetcode/dong-hua", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/429097060"
zhihu_id: "429097060"
zhihu_title: "yiduobo的每日leetcode 1574.删除最短的子数组使剩余数组有序"
question_id: "1574"
question: "删除最短的子数组使剩余数组有序"
problem_url: "https://leetcode.cn/problems/shortest-subarray-to-be-removed-to-make-array-sorted/"
difficulty: "Medium"
rating: 1932
created: "2021-11-03T20:35:05+08:00"
updated: "2021-11-03T20:35:05+08:00"
upvotes: 0
comments: 0
---

# 1574. 删除最短的子数组使剩余数组有序

> **[yiduobo的每日leetcode 1574.删除最短的子数组使剩余数组有序](https://zhuanlan.zhihu.com/p/429097060) · 知乎 · 2021-11-03 · 赞同 0**
> 力扣：[1574. 删除最短的子数组使剩余数组有序](https://leetcode.cn/problems/shortest-subarray-to-be-removed-to-make-array-sorted/) · Medium · 灵茶山艾府：[【图解】两种双指针写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1574.删除最短的子数组使剩余数组有序

[力扣](https://leetcode-cn.com/problems/shortest-subarray-to-be-removed-to-make-array-sorted/)

题目要求删掉一个子数组，使得剩下的子数组是单调不减的。那么同样是先考察边界情况。若一开始数组就是单调不减的，那么答案就是0。

接下来考察一般情况，设数组总长度为n。方便起见，不妨认为题目是要删去一个子数组，使得剩下的数满足单调不减，且剩下的数最多。将这个数记为res，那么在求解完毕后，只需要将n - res返回即为题目所求。

可以明确的是，一旦数组中出现了逆序对，那么必然要删去其中之一。而一旦出现了两处逆序对，那么最初的逆序对以及最后的逆序对之间的部分都必须全部删去。

于是可以先从头向后一趟扫描，找出第一处逆序对的位置l。然后从后向前一趟扫描，找出最后一处逆序对的位置r。此时就有两种兜底的方案，即保留0到l之间的数，或者保留r到n - 1之间的数，于是此时应该用l + 1和n - r之间的较大值先更新res。

接下来，可以明确已经删去了l + 1到r - 1之间的部分，接下来左侧0到l的部分是单调不减的，同样右侧r到n - 1的部分也是单调不减的，但是如果将二者拼起来，则可能出现前半部分中某些数大于后半部分中某些数的情况。也就是说，对于0到l中的某个位置i，必须找出r到n - 1之间的某个位置j，使得其满足arr[i] \<\= arr[j]，那么此时将0到i，以及j到n - 1拼接起来，就是一种备选答案。

可以发现，实际上这就是一个二路归并的场景。由于两边都具有单调性，那么随着i的增大，下一个j的位置必然是在当前j的后面的。于是可以初始化i为0，j为r，若某一时刻的arr[i] \<\= arr[j]，那么使用i + 1 + n - j来更新res，并将i向后移动；若arr[i] > arr[j]，那么将j向后移动。重复这个过程直到i到达l + 1或者j到达n位置。

求得res后，返回n - res即可。

最后附上python代码：

```python
class Solution(object):
    def findLengthOfShortestSubarray(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        l = 1
        n = len(arr)
        while l < n and arr[l] >= arr[l - 1]:
            l += 1
        
        if l == n:
            return 0
        
        l -= 1

        r = n - 2
        while r >= 0 and arr[r] <= arr[r + 1]:
            r -= 1

        r += 1

        res = max(l + 1, n - r)

        i = 0
        j = r
        while i <= l and j < n:
            if arr[i] <= arr[j]:
                res = max(res, i + 1 + n - j)
                i += 1
            else:
                j += 1
        
        return n - res
```
