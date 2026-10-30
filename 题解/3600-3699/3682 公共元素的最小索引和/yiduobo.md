---
title: "3682. 公共元素的最小索引和"
aliases: ["yiduobo的每日leetcode 3682.公共元素的最小索引和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1953238660670550296"
zhihu_id: "1953238660670550296"
zhihu_title: "yiduobo的每日leetcode 3682.公共元素的最小索引和"
question_id: "3682"
question: "公共元素的最小索引和"
problem_url: "https://leetcode.cn/problems/minimum-index-sum-of-common-elements/"
created: "2025-09-25T22:59:34+08:00"
updated: "2025-09-25T22:59:36+08:00"
upvotes: 0
comments: 0
---

# 3682. 公共元素的最小索引和

> **[yiduobo的每日leetcode 3682.公共元素的最小索引和](https://zhuanlan.zhihu.com/p/1953238660670550296) · 知乎 · 2025-09-25 · 赞同 0**
> 力扣：[3682. 公共元素的最小索引和](https://leetcode.cn/problems/minimum-index-sum-of-common-elements/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3682.公共元素的最小索引和

[3682. 公共元素的最小索引和 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-index-sum-of-common-elements/description/)

题目给出两个整数数组nums1和nums2，长度都为n。若nums1[i]与nums2[j]相同，则定义(i, j)为好数对。要求找出所有可能的好数对中i + j的最小索引和。若不存在，则返回-1。

首先对nums1进行一趟遍历，使用哈希表记录nums1中每种元素首次出现的位置，接下来再对nums2进行一趟遍历，使用当前元素在哈希表中记录的下标与当前下标之和更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def minimumSum(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """
        
        p = {}
        for index, v in enumerate(nums1):
            if v not in p:
                p[v] = index
        
        res = -1
        for index, v in enumerate(nums2):
            if v in p and (res == -1 or res > index + p[v]):
                res = index + p[v]
        
        return res
```
