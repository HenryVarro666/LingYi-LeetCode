---
title: "2109. 向字符串添加空格"
aliases: ["yiduobo的每日leetcode 2109.向字符串添加空格"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/四-双序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/523287615"
zhihu_id: "523287615"
zhihu_title: "yiduobo的每日leetcode 2109.向字符串添加空格"
question_id: "2109"
question: "向字符串添加空格"
problem_url: "https://leetcode.cn/problems/adding-spaces-to-a-string/"
difficulty: "Medium"
rating: 1315
created: "2022-06-02T00:20:07+08:00"
updated: "2022-06-02T00:20:07+08:00"
upvotes: 0
comments: 0
---

# 2109. 向字符串添加空格

> **[yiduobo的每日leetcode 2109.向字符串添加空格](https://zhuanlan.zhihu.com/p/523287615) · 知乎 · 2022-06-02 · 赞同 0**
> 力扣：[2109. 向字符串添加空格](https://leetcode.cn/problems/adding-spaces-to-a-string/) · Medium · 灵茶山艾府：[两种方法：双指针 / 按照空格分割（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2109.向字符串添加空格

[力扣](https://leetcode.cn/problems/adding-spaces-to-a-string/)

遍历字符串，并使用一个数组记录最终答案。

逐个把当前遍历到的字符添加到答案数组当中，若当前下标出现在space中，则在答案数组中添加一个空格。

对于判断下标是否出现在space中的方法，可以将space转化成哈希表，也可以利用排序后的单调性，使用一个指针p记录当前匹配到了space中的那个元素。随着s的向后遍历，p只会变大不会变小，因此就可以在均摊O(1)的时间内找出哪些位置出现在space中。

除了上面的方法外，利用python强悍的语言特性其实更好做。对于space中的两个位置space[index]和space[index + 1]，最终答案需要在这两个位置添加空格，也就是说s[space[index] : space[index + 1] + 1]这一段依然是完整的，那么可以直接遍历space，利用上面这种写法将完整的子串抽出来，然后按空格间隔后拼好就能得到最终答案。

另外需要注意的是，首个子字符串的起点位置是0，而最后一个子字符串的终点位置是s的长度，不要遗漏了这两个子字符串。

最后附上python代码：

```python
class Solution(object):
    def addSpaces(self, s, spaces):
        """
        :type s: str
        :type spaces: List[int]
        :rtype: str
        """

        res = []
        p = 0
        for index in range(len(s)):
            if p < len(spaces) and index == spaces[p]:
                res.append(' ')
                p += 1
            res.append(s[index])
        
        return ''.join(res)
```
