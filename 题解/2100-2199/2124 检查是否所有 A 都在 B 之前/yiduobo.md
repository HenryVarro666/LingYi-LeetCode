---
title: "2124. 检查是否所有A都在B之前"
aliases: ["yiduobo的每日leetcode 2124.检查是否所有A都在B之前"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/brainteaser", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/525661305"
zhihu_id: "525661305"
zhihu_title: "yiduobo的每日leetcode 2124.检查是否所有A都在B之前"
question_id: "2124"
question: "检查是否所有 A 都在 B 之前"
problem_url: "https://leetcode.cn/problems/check-if-all-as-appears-before-all-bs/"
difficulty: "Easy"
created: "2022-06-07T23:24:20+08:00"
updated: "2022-06-07T23:24:20+08:00"
upvotes: 0
comments: 0
---

# 2124. 检查是否所有A都在B之前

> **[yiduobo的每日leetcode 2124.检查是否所有A都在B之前](https://zhuanlan.zhihu.com/p/525661305) · 知乎 · 2022-06-07 · 赞同 0**
> 力扣：[2124. 检查是否所有 A 都在 B 之前](https://leetcode.cn/problems/check-if-all-as-appears-before-all-bs/) · Easy · 灵茶山艾府：[简洁写法：不出现 ba 即可](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2124.检查是否所有A都在B之前

[力扣](https://leetcode.cn/problems/check-if-all-as-appears-before-all-bs/)

比较基础的题目。使用一个变量b_flag记录当前是否有b出现过，初始化为false，接下来从左向右一趟遍历。若当前字符为a且b_flag为true，那么说明有b出现在当前的a之前，此时直接返回false。若当前字符为b，那么就置b_flag为true。若最终能遍历完整个字符串，那么就返回true。

最后附上python代码：

```python
class Solution(object):
    def checkString(self, s):
        """
        :type s: str
        :rtype: bool
        """

        b_flag = False
        for char in s:
            if char == 'a' and b_flag:
                return False
            elif char == 'b':
                b_flag = True

        return True
```
