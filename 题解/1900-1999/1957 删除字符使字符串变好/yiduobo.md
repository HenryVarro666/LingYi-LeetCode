---
title: "1957. 删除字符使字符串变好"
aliases: ["yiduobo的每日leetcode 1957.删除字符使字符串变好"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/492775547"
zhihu_id: "492775547"
zhihu_title: "yiduobo的每日leetcode 1957.删除字符使字符串变好"
question_id: "1957"
question: "删除字符使字符串变好"
problem_url: "https://leetcode.cn/problems/delete-characters-to-make-fancy-string/"
difficulty: "Easy"
rating: 1358
created: "2022-04-04T00:23:07+08:00"
updated: "2022-04-04T00:23:07+08:00"
upvotes: 0
comments: 0
---

# 1957. 删除字符使字符串变好

> **[yiduobo的每日leetcode 1957.删除字符使字符串变好](https://zhuanlan.zhihu.com/p/492775547) · 知乎 · 2022-04-04 · 赞同 0**
> 力扣：[1957. 删除字符使字符串变好](https://leetcode.cn/problems/delete-characters-to-make-fancy-string/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1957.删除字符使字符串变好

[力扣](https://leetcode-cn.com/problems/delete-characters-to-make-fancy-string/)

比较基础的题目，直接一趟遍历，使用一个数组来储存留下来的字符。若当前字符与答案中的最后一个以及倒数第二个字符都相同，那么就不将该字符加入到答案中。遍历完成后，将答案数组转换回字符串返回即可。

最后附上python代码：

```python
class Solution(object):
    def makeFancyString(self, s):
        """
        :type s: str
        :rtype: str
        """

        res = []
        for char in s:
            if len(res) >= 2 and res[-1] == char and res[-2] == char:
                continue
            res.append(char)
        
        return ''.join(res)
```
