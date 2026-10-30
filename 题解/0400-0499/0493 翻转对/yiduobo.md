---
title: "493. 翻转对"
aliases: ["yiduobo的每日leetcode 493.翻转对"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/255116550"
zhihu_id: "255116550"
zhihu_title: "yiduobo的每日leetcode 493.翻转对"
question_id: "493"
question: "翻转对"
problem_url: "https://leetcode.cn/problems/reverse-pairs/"
created: "2020-09-19T20:06:40+08:00"
updated: "2020-09-19T20:06:40+08:00"
upvotes: 0
comments: 0
---

# 493. 翻转对

> **[yiduobo的每日leetcode 493.翻转对](https://zhuanlan.zhihu.com/p/255116550) · 知乎 · 2020-09-19 · 赞同 0**
> 力扣：[493. 翻转对](https://leetcode.cn/problems/reverse-pairs/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

493.翻转对<https://leetcode-cn.com/problems/reverse-pairs/>

题目描述与逆序对十分类似，差别之处在于逆序对求的是i \< j时，nums[i] > nums[j]的数量，而这里稍微升级了一下，求的是i \< j时，nums[i] > nums[j] \* 2的数量，因此具体的做法也可以照搬求逆序对的做法，使用归并排序来做。

具体来说就是对于nums中的l到r这一段，设mid \= (l + r) / 2：

首先递归求解l到mid以及mid + 1到r中的翻转对数量，同时对这两段进行归并排序。

接下来，需要求解的就是对于l到mid之间的i以及mid + 1到r之间的j，存在多少对i和j使得nums[i] > nums[j] \* 2。若存在一组i和j满足nums[i] > nums[j] \* 2，那么对于所有的k，若mid \<\= k \< j，那么因为在步骤1中已经将mid + 1到r这一段排好序了，那么就有

nums[i] > nums[j] \* 2 >\= nums[k] \* 2

即nums[i]可以同nums[mid]，nums[mid + 1]，...，nums[j]都形成翻转对。

此时的任务就变成了对于所有的nums[i]，找出最小的j，使得nums[j] \* 2 >\= nums[i]。

又因为l到mid这一段也是排好序了的，若此时有nums[j] \* 2 >\= nums[i]，对于nums[i + 1]而言，满足nums[j'] \* 2 >\= nums[i + 1]的最小的j'一定大于等于j，因此每次在寻找j的时候可以从上一个j的位置开始往后寻找，所以这个过程的只需要一趟扫描即可完成。

在计算好翻转对的个数之后，最后还需要对l到r这一段进行普通的归并排序，为更上层区间的计算做准备。

最后附上python代码，其中第一个while是计算翻转对的数量，第二个while是二路归并：

```python
class Solution(object):
    def reversePairs(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        if not nums:
            return 0

        return self.mergeSort(nums, 0, len(nums) - 1)

    def mergeSort(self, nums, l, r):
        if l == r:
            return 0

        mid = (l + r) / 2
        res = self.mergeSort(nums, l, mid) + self.mergeSort(nums, mid + 1, r)

        i = l
        j = mid + 1
        while i <= mid or j <= r:
            if i <= mid:
                if j <= r and nums[i] > nums[j] * 2:
                    j += 1
                else:
                    i += 1
                    res += j - mid - 1
            else:
                j += 1
        
        i = l
        j = mid + 1
        tmp = []
        while i <= mid or j <= r:
            if i <= mid:
                if j > r or nums[i] <= nums[j]:
                    tmp.append(nums[i])
                    i += 1
                else:
                    tmp.append(nums[j])
                    j += 1
            else:
                tmp.append(nums[j])
                j += 1
                
        for index, num in enumerate(tmp):
            nums[index + l] = num

        return res
```
