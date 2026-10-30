---
title: "2934. 最大化数组末位元素的最少操作次数"
aliases: ["yiduobo的每日leetcode 2934.最大化数组末位元素的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/690781872"
zhihu_id: "690781872"
zhihu_title: "yiduobo的每日leetcode 2934.最大化数组末位元素的最少操作次数"
question_id: "2934"
question: "最大化数组末位元素的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-maximize-last-elements-in-arrays/"
difficulty: "Medium"
rating: 1803
created: "2024-04-05T05:34:58+08:00"
updated: "2024-04-05T05:34:58+08:00"
upvotes: 1
comments: 0
---

# 2934. 最大化数组末位元素的最少操作次数

> **[yiduobo的每日leetcode 2934.最大化数组末位元素的最少操作次数](https://zhuanlan.zhihu.com/p/690781872) · 知乎 · 2024-04-05 · 赞同 1**
> 力扣：[2934. 最大化数组末位元素的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-maximize-last-elements-in-arrays/) · Medium · 灵茶山艾府：[只有两种情况（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2934.最大化数组末位元素的最少操作次数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-maximize-last-elements-in-arrays/description/)

由于题目中的交换操作只能在相同下标处进行，那么如果有解，最终答案的nums1[-1]和nums2[-1]要么不变，要么交换，因此可以分别检测这两种情况能否得到合法的答案，如果可以最少的操作次数是多少。

对于确定好的数组末位，分别设为v1和v2，那么就是题目就是要求通过交换nums1和nums2中相同下标的数，使得nums1中的数都小于等于v1，num2中的数都小于等于v2。于是可以一趟遍历，对于当前的nums1[i]和nums2[i]，若nums1[i] \<\= v1且nums2[i] \<\= v2，那么不需要交换；若nums1[i] \<\= v2且num2[i] \<\= v1，那么执行交换后可以满足，此时需要进行交换并更新交换次数；而对于其他情况，无论是否交换都不行。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        def calc(v1, v2):
            s = 0
            for i in range(len(nums1) - 1):
                if nums1[i] <= v1 and nums2[i] <= v2:
                    continue
                if nums1[i] <= v2 and nums2[i] <= v1:
                    s += 1
                else:
                    return -1
            return s

        s1 = calc(nums1[-1], nums2[-1])
        s2 = calc(nums2[-1], nums1[-1])
        if s1 == -1:
            if s2 == -1:
                return -1
            else:
                return s2 + 1
        elif s2 == -1:
            return s1
        else:
            return min(s1, s2 + 1)
```
