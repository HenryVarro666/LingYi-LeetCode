---
title: "27. 移除元素"
aliases: ["yiduobo的每日leetcode 27.移除元素"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/stack", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/面试经典-150-题", "题单/滑动窗口与双指针/三-单序列双指针", "题单/面试经典-150-题/数组-/-字符串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/117636994"
zhihu_id: "117636994"
zhihu_title: "yiduobo的每日leetcode 27.移除元素"
question_id: "27"
question: "移除元素"
problem_url: "https://leetcode.cn/problems/remove-element/"
difficulty: "Easy"
created: "2020-03-26T23:00:15+08:00"
updated: "2020-03-26T23:00:15+08:00"
upvotes: 0
comments: 0
---

# 27. 移除元素

> **[yiduobo的每日leetcode 27.移除元素](https://zhuanlan.zhihu.com/p/117636994) · 知乎 · 2020-03-26 · 赞同 0**
> 力扣：[27. 移除元素](https://leetcode.cn/problems/remove-element/) · Easy · 灵茶山艾府：[用栈思考，原地实现（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

27.移除元素<https://leetcode-cn.com/problems/remove-element/>

不知道怎么形容的题目。

与上题一样，如果允许使用额外空间，那么使用一个res记录答案，依次扫描nums中的数，如果不等于val则加入到res中即可。同样的，如果把res直接重叠到nums中也不会影响到最后的答案，因此从头开始扫描，找到不等于的val的数就从头部开始覆盖nums中的数即可。

最后附上python代码：

```python
class Solution(object):
    def removeElement(self, nums, val):
        """
        :type nums: List[int]
        :type val: int
        :rtype: int
        """

        if not nums:
            return 0

        now = 0
        for num in nums:
            if num != val:
                nums[now] = num
                now += 1

        return now
```
