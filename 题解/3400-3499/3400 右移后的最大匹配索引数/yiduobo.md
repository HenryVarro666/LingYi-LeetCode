---
title: "3400. 右移后的最大匹配索引数"
aliases: ["yiduobo的每日leetcode 3400.右移后的最大匹配索引数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/30903315255"
zhihu_id: "30903315255"
zhihu_title: "yiduobo的每日leetcode 3400.右移后的最大匹配索引数"
question_id: "3400"
question: "右移后的最大匹配索引数"
problem_url: "https://leetcode.cn/problems/maximum-number-of-matching-indices-after-right-shifts/"
created: "2025-03-18T00:07:30+08:00"
updated: "2025-03-18T00:07:30+08:00"
upvotes: 1
comments: 0
---

# 3400. 右移后的最大匹配索引数

> **[yiduobo的每日leetcode 3400.右移后的最大匹配索引数](https://zhuanlan.zhihu.com/p/30903315255) · 知乎 · 2025-03-18 · 赞同 1**
> 力扣：[3400. 右移后的最大匹配索引数](https://leetcode.cn/problems/maximum-number-of-matching-indices-after-right-shifts/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3400.右移后的最大匹配索引数

[3400. 右移后的最大匹配索引数 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-number-of-matching-indices-after-right-shifts/description/)

题目给出两个长度相同的整数数组nums1和nums2，数组的长度不超过3000。若nums1[i]与nums2[i]相等，则认为下标i是匹配的。

现在需要计算对nums1执行任意次右移操作后，与nums2的最大匹配下标数量是多少。右移指的是将下标i的元素移动到(i + 1) % n。

首先可以明确的是，右移的轮次必然小于数组的长度n，因为右移n次相当于无事发生。又由于题目的数据规模并不大，那么就可以直接暴力枚举右移的轮次rnd，然后针对每个rnd检测有多少个下标可以匹配。

对于当前枚举到的rnd，接下来初始化匹配数为0，然后对nums1进行一趟遍历。对于当前遍历到的nums1[index]，其右移rnd轮后的下标为(index + rnd) % n，因此需要对比nums1[index]与nums2[(index + rnd) % n]是否相等，若相等则将匹配数加上1。遍历完nums1后，使用匹配数更新答案，然后继续考察下一个rnd即可。

最后附上python代码：

```python
class Solution(object):
    def maximumMatchingIndices(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """
        
        n = len(nums1)
        res = 0

        for rnd in range(n):
            hit = 0
            for index in range(n):
                target = (index + rnd) % n
                if nums1[index] == nums2[target]:
                    hit += 1
            res = max(res, hit)
        
        return res
```
