---
title: "344. 反转字符串"
aliases: ["yiduobo的每日leetcode 344.反转字符串"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/two-pointers", "leetcode/string", "leetcode/bian-li", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/163263680"
zhihu_id: "163263680"
zhihu_title: "yiduobo的每日leetcode 344.反转字符串"
question_id: "344"
question: "反转字符串"
problem_url: "https://leetcode.cn/problems/reverse-string/"
difficulty: "Easy"
created: "2020-07-23T20:44:53+08:00"
updated: "2020-07-23T20:44:53+08:00"
upvotes: 0
comments: 0
---

# 344. 反转字符串

> **[yiduobo的每日leetcode 344.反转字符串](https://zhuanlan.zhihu.com/p/163263680) · 知乎 · 2020-07-23 · 赞同 0**
> 力扣：[344. 反转字符串](https://leetcode.cn/problems/reverse-string/) · Easy · 灵茶山艾府：[三种写法：双指针/单指针/库函数（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

344.反转字符串<https://leetcode-cn.com/problems/reverse-string/>

比较基础的题目，直接按中心位置交换两侧字符即可。

最后附上python代码：

```python
class Solution(object):
    def reverseString(self, s):
        """
        :type s: List[str]
        :rtype: None Do not return anything, modify s in-place instead.
        """

        for index in range(len(s) / 2):
            s[index], s[len(s) - index - 1] = s[len(s) - index - 1], s[index]
```
