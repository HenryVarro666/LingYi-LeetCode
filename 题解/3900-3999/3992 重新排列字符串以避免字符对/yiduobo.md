---
title: "3992. 重新排列字符串以避免字符对"
aliases: ["yiduobo的每日leetcode 3992.重新排列字符串以避免字符对"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/two-pointers", "leetcode/sorting", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2062640659601821837"
zhihu_id: "2062640659601821837"
zhihu_title: "yiduobo的每日leetcode 3992.重新排列字符串以避免字符对"
question_id: "3992"
question: "重新排列字符串以避免字符对"
problem_url: "https://leetcode.cn/problems/rearrange-string-to-avoid-character-pair/"
difficulty: "Easy"
created: "2026-07-20T20:54:41+08:00"
updated: "2026-07-20T20:54:42+08:00"
upvotes: 0
comments: 0
---

# 3992. 重新排列字符串以避免字符对

> **[yiduobo的每日leetcode 3992.重新排列字符串以避免字符对](https://zhuanlan.zhihu.com/p/2062640659601821837) · 知乎 · 2026-07-20 · 赞同 0**
> 力扣：[3992. 重新排列字符串以避免字符对](https://leetcode.cn/problems/rearrange-string-to-avoid-character-pair/) · Easy · 灵茶山艾府：[两种方法：排序 / 双指针（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3992.重新排列字符串以避免字符对

<https://leetcode.cn/problems/rearrange-string-to-avoid-character-pair/description/>

题目给出一个字符串s以及两个不同的小写英文字母x和y。

现在要求重新排列s，使得其中所有的y都处于x左侧。

返回任意一个合法的重新排列后的字符串。

题目只需给出任意合法的字符串，因此处理的方案很多。我在这里选择的是一趟遍历，对于其中的x和y，仅统计出现次数，分别记为cnt_x以及cnt_y，而对于其他的字符，则按原顺序添加到答案中。遍历完成后，往答案中添加cnt_y个y，最后添加cnt_x个x即可。

最后附上python代码：

```python
class Solution(object):
    def rearrangeString(self, s, x, y):
        """
        :type s: str
        :type x: str
        :type y: str
        :rtype: str
        """
        
        cnt_x = 0
        cnt_y = 0
        res = []
        for c in s:
            if c == x:
                cnt_x += 1
            elif c == y:
                cnt_y += 1
            else:
                res.append(c)
        
        res.append(y * cnt_y)
        res.append(x * cnt_x)
        return ''.join(res)
```
