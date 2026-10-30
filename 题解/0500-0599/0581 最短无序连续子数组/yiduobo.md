---
title: "581. 最短无序连续子数组"
aliases: ["yiduobo的每日leetcode 581.最短无序连续子数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/266886883"
zhihu_id: "266886883"
zhihu_title: "yiduobo的每日leetcode 581.最短无序连续子数组"
question_id: "581"
question: "最短无序连续子数组"
problem_url: "https://leetcode.cn/problems/shortest-unsorted-continuous-subarray/"
created: "2020-10-19T22:59:18+08:00"
updated: "2020-10-19T22:59:18+08:00"
upvotes: 0
comments: 0
---

# 581. 最短无序连续子数组

> **[yiduobo的每日leetcode 581.最短无序连续子数组](https://zhuanlan.zhihu.com/p/266886883) · 知乎 · 2020-10-19 · 赞同 0**
> 力扣：[581. 最短无序连续子数组](https://leetcode.cn/problems/shortest-unsorted-continuous-subarray/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

581.最短无序连续子数组<https://leetcode-cn.com/problems/shortest-unsorted-continuous-subarray/>

首先，对于数组中的任意逆序对nums[i]，nums[j]，其中i \< j，那么最终答案(x, y)必然要满足x \<\= i \< j \<\= y，否则nums[i]和nums[j]这一对逆序对就无法得到修正。因此，我们需要找到所有逆序对中最左侧的数和最右侧的数，这个区间就是最终的答案。

对于找最左侧和最右侧的逆序对中的数，可以使用单调栈来处理，以找最左侧的数为例：

维护一个单调栈，然后从左往右一趟扫描。

若当前栈为空或者栈顶元素大于当前元素，那么栈顶元素与当前元素就是一组逆序对，此时可以用栈顶元素在数组中的下标来更新最左侧逆序对的下标。另外，其他栈中的元素也有可能与当前元素形成逆序对，因此需要不断弹栈直到栈顶元素小于等于当前元素为止。

当栈顶元素小于等于当前元素时，栈中就没有任何元素可以与当前元素形成逆序对了，因此将当前元素也压入栈中留给后续元素使用即可。

找最右侧元素也是类似，不过需要从右往左进行一趟扫描，同时需要注意栈中元素与当前元素大小关系的转变。

若最后能找到最左侧的逆序对中的数的位置，那么一定存在最右侧的逆序对中的数的位置，二者相减即为答案，否则整个数组本来就是有序的，最终答案为0。

最后附上python代码：

```python
class Solution(object):
    def findUnsortedSubarray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        stack = [0]
        left = None
        for index in range(1, len(nums)):
            while stack and nums[stack[-1]] > nums[index]:
                if left is None or left > stack[-1]:
                    left = stack[-1]
                stack.pop()
            stack.append(index)
        
        stack = [len(nums) - 1]
        right = None
        for index in range(len(nums) - 2, -1, -1):
            while stack and nums[stack[-1]] < nums[index]:
                if right is None or right < stack[-1]:
                    right = stack[-1]
                stack.pop()
            stack.append(index)
        
        if left is None:
            return 0
        else:
            return right - left + 1
```
