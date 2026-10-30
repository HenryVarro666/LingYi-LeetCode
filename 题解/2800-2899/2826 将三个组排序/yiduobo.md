---
title: "2826. 将三个组排序"
aliases: ["yiduobo的每日leetcode 2826.将三个组排序"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/四-经典线性-DP", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/659083667"
zhihu_id: "659083667"
zhihu_title: "yiduobo的每日leetcode 2826.将三个组排序"
question_id: "2826"
question: "将三个组排序"
problem_url: "https://leetcode.cn/problems/sorting-three-groups/"
difficulty: "Medium"
rating: 1721
created: "2023-09-29T22:32:10+08:00"
updated: "2023-09-29T22:32:10+08:00"
upvotes: 0
comments: 0
---

# 2826. 将三个组排序

> **[yiduobo的每日leetcode 2826.将三个组排序](https://zhuanlan.zhihu.com/p/659083667) · 知乎 · 2023-09-29 · 赞同 0**
> 力扣：[2826. 将三个组排序](https://leetcode.cn/problems/sorting-three-groups/) · Medium · 灵茶山艾府：[三种方法：LIS / 多维 DP / 合法子序列 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2826.将三个组排序

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/sorting-three-groups/description/)

题目中的将三个组排序，实际上就是要让所有的1在数组的最左边，所有的2在数组的中间，所有的3在数组的最右边，也就是说最终会得到一个单调不减的数组。为了使得修改的次数最少，就是要让不进行修改的位置最多，那么本题实际上就是要找出原数组中的一个最长的不减子序列，然后基于这个子序列就可以构造出美丽数组了。

问题到了这里就变成了经典的最长不减子序列问题，对于本题的数据规模，使用贪心法或者动态规划都是可行的。

最后附上python代码：

```python
class Solution(object):
    def minimumOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        f = [nums[0]]
        for v in nums[1:]:
            if v >= f[-1]:
                f.append(v)
            else:
                left = 0
                right = len(f) - 1
                while left < right:
                    mid = (left + right) / 2
                    if f[mid] > v:
                        right = mid
                    else:
                        left = mid + 1
                
                f[left] = v
        
        return len(nums) - len(f)
```
