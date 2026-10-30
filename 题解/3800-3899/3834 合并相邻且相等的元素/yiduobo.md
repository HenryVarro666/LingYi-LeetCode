---
title: "3834. 合并相邻且相等的元素"
aliases: ["yiduobo的每日leetcode 3834.合并相邻且相等的元素"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/simulation", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2003933960540012673"
zhihu_id: "2003933960540012673"
zhihu_title: "yiduobo的每日leetcode 3834.合并相邻且相等的元素"
question_id: "3834"
question: "合并相邻且相等的元素"
problem_url: "https://leetcode.cn/problems/merge-adjacent-equal-elements/"
difficulty: "Medium"
rating: 1429
created: "2026-02-08T21:00:58+08:00"
updated: "2026-02-08T21:00:58+08:00"
upvotes: 1
comments: 1
---

# 3834. 合并相邻且相等的元素

> **[yiduobo的每日leetcode 3834.合并相邻且相等的元素](https://zhuanlan.zhihu.com/p/2003933960540012673) · 知乎 · 2026-02-08 · 赞同 1**
> 力扣：[3834. 合并相邻且相等的元素](https://leetcode.cn/problems/merge-adjacent-equal-elements/) · Medium · 灵茶山艾府：[用栈模拟，两种写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3834.合并相邻且相等的元素

<https://leetcode.cn/problems/merge-adjacent-equal-elements/description/>

题目给出一个整数数组nums。

若nums中存在两个相邻且相等的元素，那么就需要选择数组中最左侧的这对相邻元素，并使用它们的和来替换它们。重复此过程直到数组中没有相邻且相等的元素位置。

问执行完操作后得到的最终数组是什么。

由于题目要求是选择最左侧的元素对进行操作，那么不妨设当前最左侧的相等相邻元素为nums[p]以及nums[p - 1]，那么在这二者合并为nums[p] \* 2之后，其需要先尝试与nums[p - 2]进行合并，当无法合并时，再继续往后考虑nums[p + 1]以及之后的元素。

也就是说，对于最左侧的相等相邻元素而言，其并不需要考虑后续的元素，因此在这里可以通过栈来模拟这个合并过程，理由是栈中可以储存当前元素所有左侧剩余的元素，而右侧的元素暂时无需考虑，另一方面，在合并时也是逐个往前尝试合并，相当于某种先进后出。

基于上面的结论，就可以使用一个栈来储存遍历且合并后得到的数组，接下来一趟遍历，对于当前元素v，若栈非空且v与栈顶元素相同，则将栈顶元素弹出并将v更新为v \* 2，表示得到的数组最后一个元素与v是最左侧的相等相邻元素，需要进行合并。重复此过程直到栈为空或者v与栈顶元素不同为止，接下来将v加入到栈中，然后继续向后遍历即可。遍历完成后，栈中储存的即为最终的数组。

最后附上python代码：

```python
class Solution(object):
    def mergeAdjacent(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        
        stack = []
        for v in nums:
            while stack and stack[-1] == v:
                stack.pop()
                v += v
            
            stack.append(v)
        
        return stack
```
