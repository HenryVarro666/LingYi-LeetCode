---
title: "42. 接雨水"
aliases: ["yiduobo的每日leetcode 42.接雨水"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/two-pointers", "leetcode/monotonic-stack", "题单/滑动窗口与双指针", "题单/动态规划", "题单/单调栈", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/滑动窗口与双指针/三-单序列双指针", "题单/动态规划/专题-前后缀分解", "题单/单调栈/二-矩形", "题单/LeetCode-热题-100/双指针", "题单/面试经典-150-题/数组-/-字符串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/123352424"
zhihu_id: "123352424"
zhihu_title: "yiduobo的每日leetcode 42.接雨水"
question_id: "42"
question: "接雨水"
problem_url: "https://leetcode.cn/problems/trapping-rain-water/"
difficulty: "Hard"
created: "2020-04-02T21:45:52+08:00"
updated: "2020-04-02T21:45:52+08:00"
upvotes: 0
comments: 0
---

# 42. 接雨水

> **[yiduobo的每日leetcode 42.接雨水](https://zhuanlan.zhihu.com/p/123352424) · 知乎 · 2020-04-02 · 赞同 0**
> 力扣：[42. 接雨水](https://leetcode.cn/problems/trapping-rain-water/) · Hard · 灵茶山艾府：[【视频】三种方法：前后缀分解/双指针/单调栈（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

42.接雨水<https://leetcode-cn.com/problems/trapping-rain-water/>

这个题目还蛮有意思的。

我的思路是对于其中某一个柱子，设这个柱子高度为h，那么在这个柱子上方能接的水取决于这个柱子左侧最高的柱子highest_left以及右侧最高的柱子highest_right中较矮的那一个，即min(highest_left，highest_right)。如果min(highest_left，highest_right) > h ，说明可以接 min(highest_left，highest_right) - h 的水，否则当前这个柱子无法接水。

另外，由于这里的答案还是取决于矮的那一侧，于是可以参考之前计算面积的那题，使用左右双指针往内扫描的方法来确定highest_left与highest_right。当highest_left \< highest_right时，应该计算当前的left，然后利用left更新highest_left。同理，如果情况反过来，就是计算当前的right，然后利用right更新highest_right。于是，最后的时间复杂度为O(n)。

最后附上python代码：

```python
class Solution(object):
    def trap(self, height):
        """
        :type height: List[int]
        :rtype: int
        """

        left = 0
        right = len(height) - 1
        highest_left = 0
        highest_right = 0
        res = 0

        while left <= right:
            if highest_left < highest_right:
                if height[left] < highest_left:
                    res += highest_left - height[left]
                else:
                    highest_left = height[left]
                left += 1
            else:
                if height[right] < highest_right:
                    res += highest_right - height[right]
                else:
                    highest_right = height[right]
                right -= 1

        return res
```
