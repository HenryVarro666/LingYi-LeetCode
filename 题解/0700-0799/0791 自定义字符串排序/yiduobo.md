---
title: "791. 自定义字符串排序"
aliases: ["yiduobo的每日leetcode 791.自定义字符串排序"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/341603178"
zhihu_id: "341603178"
zhihu_title: "yiduobo的每日leetcode 791.自定义字符串排序"
question_id: "791"
question: "自定义字符串排序"
problem_url: "https://leetcode.cn/problems/custom-sort-string/"
created: "2021-01-03T22:31:48+08:00"
updated: "2021-01-03T22:31:48+08:00"
upvotes: 1
comments: 0
---

# 791. 自定义字符串排序

> **[yiduobo的每日leetcode 791.自定义字符串排序](https://zhuanlan.zhihu.com/p/341603178) · 知乎 · 2021-01-03 · 赞同 1**
> 力扣：[791. 自定义字符串排序](https://leetcode.cn/problems/custom-sort-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

791.自定义字符串排序

[力扣](https://leetcode-cn.com/problems/custom-sort-string/)

比较基础的题目。对于T中的每个字符，若其没有出现在S中，那么就直接将该字符加入到答案中，否则将该字符加入到一个list中。处理完成后，对于这个list按S中字符出现的顺序进行排序，这一步也只需要简单的重载比较函数即可。

最后附上python代码：

```python
class Solution(object):
    def customSortString(self, S, T):
        """
        :type S: str
        :type T: str
        :rtype: str
        """

        order_dict = {}
        for index, char in enumerate(S):
            order_dict[char] = index
        
        res = ''
        char_list = []
        for char in T:
            if char not in order_dict:
                res += char
            else:
                char_list.append(char)
        
        return res + ''.join(sorted(char_list, key=lambda d:order_dict[d]))
```
