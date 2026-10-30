---
title: "1618. 找出适应屏幕的最大字号"
aliases: ["yiduobo的每日leetcode 1618.找出适应屏幕的最大字号"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/618814728"
zhihu_id: "618814728"
zhihu_title: "yiduobo的每日leetcode 1618.找出适应屏幕的最大字号"
question_id: "1618"
question: "找出适应屏幕的最大字号"
problem_url: "https://leetcode.cn/problems/maximum-font-to-fit-a-sentence-in-a-screen/"
created: "2023-04-02T01:44:38+08:00"
updated: "2023-04-02T01:44:38+08:00"
upvotes: 0
comments: 0
---

# 1618. 找出适应屏幕的最大字号

> **[yiduobo的每日leetcode 1618.找出适应屏幕的最大字号](https://zhuanlan.zhihu.com/p/618814728) · 知乎 · 2023-04-02 · 赞同 0**
> 力扣：[1618. 找出适应屏幕的最大字号](https://leetcode.cn/problems/maximum-font-to-fit-a-sentence-in-a-screen/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1618.找出适应屏幕的最大字号

[力扣](https://leetcode.cn/problems/maximum-font-to-fit-a-sentence-in-a-screen/)

字号越大，所需的高度和宽度也就越大，而字号大小已经排好序了，因此可以使用二分法来寻找合法的最大字号。对于当前二分到的字号fonts[mid]，首先要求该字号的高度不超过h，若满足，那么就需要遍历text，累加每个字符在当前字号下的宽度，若这个宽度之和不超过w，那么说明当前的字号是合法的，因此需要更新二分的下界为mid，否则就需要更新二分的上界为mid - 1。

最后附上python代码：

```python
# """
# This is FontInfo's API interface.
# You should not implement it, or speculate about its implementation
# """
#class FontInfo(object):
#    Return the width of char ch when fontSize is used.
#    def getWidth(self, fontSize, ch):
#        """
#        :type fontSize: int
#        :type ch: char
#        :rtype int
#        """
# 
#    def getHeight(self, fontSize):
#        """
#        :type fontSize: int
#        :rtype int
#        """
class Solution(object):
    def maxFont(self, text, w, h, fonts, fontInfo):
        """
        :type text: str
        :type w: int
        :type h: int
        :type fonts: List[int]
        :type fontInfo: FontInfo
        :rtype: int
        """

        def check(f_size):
            if fontInfo.getHeight(f_size) > h:
                return False

            s = 0
            for char in text:
                s += fontInfo.getWidth(f_size, char)
            
            return s <= w
        
        if not check(fonts[0]):
            return -1
        
        left, right = 0, len(fonts) - 1
        while left < right:
            mid = (left + right + 1) / 2
            if check(fonts[mid]):
                left = mid
            else:
                right = mid - 1
        
        return fonts[left]
```
