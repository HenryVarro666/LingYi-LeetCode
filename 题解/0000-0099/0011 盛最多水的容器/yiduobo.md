---
title: "11. 盛最多水的容器"
aliases: ["yiduobo的每日leetcode 11.盛最多水的容器"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/滑动窗口与双指针/三-单序列双指针", "题单/LeetCode-热题-100/双指针", "题单/面试经典-150-题/双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/114270250"
zhihu_id: "114270250"
zhihu_title: "yiduobo的每日leetcode 11.盛最多水的容器"
question_id: "11"
question: "盛最多水的容器"
problem_url: "https://leetcode.cn/problems/container-with-most-water/"
difficulty: "Medium"
created: "2020-03-18T21:39:16+08:00"
updated: "2020-03-18T21:39:16+08:00"
upvotes: 0
comments: 0
---

# 11. 盛最多水的容器

> **[yiduobo的每日leetcode 11.盛最多水的容器](https://zhuanlan.zhihu.com/p/114270250) · 知乎 · 2020-03-18 · 赞同 0**
> 力扣：[11. 盛最多水的容器](https://leetcode.cn/problems/container-with-most-water/) · Medium · 灵茶山艾府：[【视频讲解】双指针做法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

11.盛最多水的容器<https://leetcode-cn.com/problems/container-with-most-water/>

可以注意到，这个面积取决于较短的侧边以及下边的长度，那么显然最长的底边就是分别取最左边和最右边。当然，最优解也可能是往内推进了一些，因为虽然此时的底边变短了，但是较短的侧边变长了，那么我们可以从最左和最右开始，往内推进寻找最优解。

设两个侧边分别为h1和h2，底边为l，若满足h1 \<\= h2，那么此时的面积为h1 \* l。

当h2往内部移动时，设此时新的侧边为h2"，新的底边为l"，显然有l" \< l。

那么当h2" \< h1时，面积为h2" \* l"，宽和高都变小了，结果肯定是变小了；当h2" >\= h1时，此时的面积为h1 \* l"，显然也小于原来的h1 \* l。因此当其中某一边较短时，如果往内移动另一边，结果必定是越来越差的，说明往内推进时需要先推进较短的那条侧边。按这个原则往内推进直到无法推进为止，记录下每次推进后的结果即可。

最终的时间复杂度为O(n)。

最后附上python代码：

```python
class Solution(object):
    def maxArea(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        left = 0
        right = len(height) - 1
        ans = 0 
        while left < right:
            ans = max(ans, (right - left) * min(height[left], height[right]))
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return ans
```
