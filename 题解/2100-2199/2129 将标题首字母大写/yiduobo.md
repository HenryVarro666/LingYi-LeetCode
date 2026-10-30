---
title: "2129. 将标题首字母大写"
aliases: ["yiduobo的每日leetcode 2129.将标题首字母大写"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/526721150"
zhihu_id: "526721150"
zhihu_title: "yiduobo的每日leetcode 2129.将标题首字母大写"
question_id: "2129"
question: "将标题首字母大写"
problem_url: "https://leetcode.cn/problems/capitalize-the-title/"
difficulty: "Easy"
created: "2022-06-10T00:10:59+08:00"
updated: "2022-06-10T00:11:17+08:00"
upvotes: 0
comments: 0
---

# 2129. 将标题首字母大写

> **[yiduobo的每日leetcode 2129.将标题首字母大写](https://zhuanlan.zhihu.com/p/526721150) · 知乎 · 2022-06-10 · 赞同 0**
> 力扣：[2129. 将标题首字母大写](https://leetcode.cn/problems/capitalize-the-title/) · Easy · 灵茶山艾府：[简洁写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2129.将标题首字母大写

[力扣](https://leetcode.cn/problems/capitalize-the-title/)

题目的需求是将字符串中长度大于等于3的单词的首字母变为大写，字符串的其余字符变为小写，那么最直观的做法就是将字符串的单词先分离出来，然后通过判断单词长度决定应该如何处理单词，最后再将单词拼回去。

不过注意到题目保证了单词间仅有一个空格连接，那么完全可以通过相邻空格的下标之差来判断空格之间单词的长度，同时可以通过上一个空格的下标得到该单词首字母在答案中的下标，此时就得到了一种只需一趟遍历的做法。

使用一个变量last记录上一个空格的位置，初始化为-1，然后从头开始向后遍历字符串。对于当前字符title[index]：

1、若title[index]为大写字母，先将其转化成小写字母

2、无论title[index]是什么都将其加入到答案数组中

3、若title[index]为空格，同时有index - last > 3，那么说明last和index之间的单词长度大于等于3，因此需要将该单词的首字母，也就是对应到答案数组中last + 1这个下标的字符变为大写。另外，无论是否满足index - last > 3，都需要将last更新为index

遍历完成后，需要特别注意不要遗漏了最后一个单词长度的判断。

最后附上python代码：

```python
class Solution(object):
    def capitalizeTitle(self, title):
        """
        :type title: str
        :rtype: str
        """

        res = []
        last = -1
        for index, char in enumerate(title):
            if char >= 'A' and char <= 'Z':
                char = chr(ord(char) + 32)
            res.append(char)
            if char == ' ':
                if index - last > 3:
                    res[last + 1] = chr(ord(res[last + 1]) - 32)
                last = index
        
        index += 1
        if index - last > 3:
            res[last + 1] = chr(ord(res[last + 1]) - 32)

        return ''.join(res)
```
