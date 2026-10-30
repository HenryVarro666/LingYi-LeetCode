---
title: "442. 数组中重复的数据"
aliases: ["yiduobo的每日leetcode 442.数组中重复的数据"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/205550018"
zhihu_id: "205550018"
zhihu_title: "yiduobo的每日leetcode 442.数组中重复的数据"
question_id: "442"
question: "数组中重复的数据"
problem_url: "https://leetcode.cn/problems/find-all-duplicates-in-an-array/"
created: "2020-08-29T21:40:05+08:00"
updated: "2020-08-29T21:40:05+08:00"
upvotes: 1
comments: 0
---

# 442. 数组中重复的数据

> **[yiduobo的每日leetcode 442.数组中重复的数据](https://zhuanlan.zhihu.com/p/205550018) · 知乎 · 2020-08-29 · 赞同 1**
> 力扣：[442. 数组中重复的数据](https://leetcode.cn/problems/find-all-duplicates-in-an-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

442.数组中重复的数据<https://leetcode-cn.com/problems/find-all-duplicates-in-an-array/>

题目保证a中元素在1到n之间，与之前某题很像，于是可以采用类似的方法，将a[index]哈希到index - 1这个位置上。具体做法为一趟扫描，不断交换a[a[index] - 1]与a[index]直到a[index - 1]位置上的数等于a[index]为止。

完成上面的步骤之后，对于所有出现一次的数a[p]，其必然等于p + 1。而对于出现两次的数，由于某个数占据了对应的位置，那么另一个数就必然不满足a[p] \= p + 1，于是可以统计a[p]不等于p + 1出现的次数，即为最终的答案。

对于交换这个步骤而言，虽然看上去是二重循环，但是每次交换必然使得某个数被交换到最终位置，因此最终的时间复杂度还是O(n)。

最后附上python代码：

```python
class Solution(object):
    def findDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        for index in range(len(nums)):
            while nums[nums[index] - 1] != nums[index]:
                nums[nums[index] - 1], nums[index] = nums[index], nums[nums[index] - 1]
        
        res = []
        for index, num in enumerate(nums):
            if num != index + 1:
                res.append(num)

        return res
```
