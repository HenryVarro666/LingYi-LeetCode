---
title: "496. 下一个更大元素I"
aliases: ["yiduobo的每日leetcode 496.下一个更大元素I"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/stack", "leetcode/hash-table", "leetcode/monotonic-stack", "题单/单调栈", "题单/单调栈/一-单调栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/257283167"
zhihu_id: "257283167"
zhihu_title: "yiduobo的每日leetcode 496.下一个更大元素I"
question_id: "496"
question: "下一个更大元素 I"
problem_url: "https://leetcode.cn/problems/next-greater-element-i/"
difficulty: "Easy"
created: "2020-09-21T21:16:26+08:00"
updated: "2020-09-21T21:16:26+08:00"
upvotes: 1
comments: 0
---

# 496. 下一个更大元素I

> **[yiduobo的每日leetcode 496.下一个更大元素I](https://zhuanlan.zhihu.com/p/257283167) · 知乎 · 2020-09-21 · 赞同 1**
> 力扣：[496. 下一个更大元素 I](https://leetcode.cn/problems/next-greater-element-i/) · Easy · 灵茶山艾府：[【视频】单调栈的两种写法，附单调栈题单（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

496.下一个更大元素I <https://leetcode-cn.com/problems/next-greater-element-i/>

虽然题目描述中出现了两个数组，但是仔细看题可以发现要求实际上只需要先用dict保存第一个所有元素在第二个数组中的位置，剩下的工作就都是在第二个数组中完成了。

那么现在问题就变成了对于一个数组，找出其中所有元素下一个更大元素的位置，这个问题可以用单调栈来处理。具体来说就是从后往前扫描整个数组，并用一个栈将可能成为答案的数保存起来。

首先，数组的最后一个元素没有下一个元素了，因此其对应的答案应该是-1，同时将其压入栈中。

接下来往前扫描，若当前元素大于栈顶元素，那么此时的栈顶元素位置比当前元素更靠后，且值更小，说明栈顶元素不可能再成为答案，应当将其弹出。重复此过程直到栈为空或者栈顶元素大于当前元素。如果是后面这种情况，那么说明当前元素的下一个更大元素就是栈顶元素，否则为-1。最后，将当前元素压入栈顶，然后继续往前扫描即可。

最后附上python代码：

```python
class Solution(object):
    def nextGreaterElement(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """

        if not nums2:
            return [-1] * len(nums1)

        if not nums1:
            return []

        stack = [len(nums2) - 1]
        pos_list = [-1]
        pos_dict = {nums2[-1] : len(nums2) - 1}
        for index in range(len(nums2) - 1, -1, -1):
            while stack and nums2[index] >= nums2[stack[-1]]:
                stack.pop()
            if stack:
                pos_list.append(nums2[stack[-1]])
            else:
                pos_list.append(-1)
            stack.append(index)
            pos_dict[nums2[index]] = index

        res = []
        for num in nums1:
            if num not in pos_dict:
                res.append(-1)
            else:
                res.append(pos_list[len(nums2) - pos_dict[num]])

        return res
```
