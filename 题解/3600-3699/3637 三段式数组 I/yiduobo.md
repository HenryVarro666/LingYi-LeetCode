---
title: "3637. 三段式数组I"
aliases: ["yiduobo的每日leetcode 3637.三段式数组I"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/simulation", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1947100736996483241"
zhihu_id: "1947100736996483241"
zhihu_title: "yiduobo的每日leetcode 3637.三段式数组I"
question_id: "3637"
question: "三段式数组 I"
problem_url: "https://leetcode.cn/problems/trionic-array-i/"
difficulty: "Easy"
created: "2025-09-05T01:02:35+08:00"
updated: "2025-09-05T01:02:35+08:00"
upvotes: 1
comments: 1
---

# 3637. 三段式数组I

> **[yiduobo的每日leetcode 3637.三段式数组I](https://zhuanlan.zhihu.com/p/1947100736996483241) · 知乎 · 2025-09-05 · 赞同 1**
> 力扣：[3637. 三段式数组 I](https://leetcode.cn/problems/trionic-array-i/) · Easy · 灵茶山艾府：[两种写法，推广到多个拐弯的一般情况（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3637.三段式数组I

[3637. 三段式数组 I - 力扣（LeetCode）](https://leetcode.cn/problems/trionic-array-i/description/)

题目给出一个长度为n的整数数组nums。若存在索引0 \< p \< q \< n - 1，使得数组满足nums[0: p + 1]严格递增，nums[p: q + 1]严格递减，nums[q:]严格递增，那么就称其为三段式数组。问nums是否为三段式数组。

由于题目中的划分需要将所有的数组元素都包含进来，那么只需从0开始向后遍历，来寻找对应的p。对于当前的p，若nums[p + 1] > nums[p]，就将p向后移动，直到p来到数组末尾或者不满足条件。

若p一步都没动过，说明不存在递增的第一段，直接返回false。否则就从p开始向后遍历，寻找对应的q。对于当前的q，若nums[q + 1] \< nums[q]，就将q向后移动，直到q来到数组末尾或者不满足条件。

若q一步都没动过，说明不存在递减的第二段，直接返回false，否则就从q + 1开始向后遍历，检测最后这一段中的每个元素是否大于上一个元素，若都满足，说明p和q就是要找的那两个索引，应该返回true，否则返回false。

最后附上python代码：

```python
class Solution(object):
    def isTrionic(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        
        p = 0
        while p + 1 < len(nums) and nums[p + 1] > nums[p]:
            p += 1
        
        if p == 0:
            return False
        
        q = p
        while q + 1 < len(nums) and nums[q + 1] < nums[q]:
            q += 1
        
        if q == p or q == len(nums) - 1:
            return False
        
        pre = nums[q]
        for v in nums[q + 1:]:
            if v <= pre:
                return False
            pre = v
            
        return True
```
