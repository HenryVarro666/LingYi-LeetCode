---
title: "345. 反转字符串中的元音字母"
aliases: ["yiduobo的每日leetcode 345.反转字符串中的元音字母"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/163540344"
zhihu_id: "163540344"
zhihu_title: "yiduobo的每日leetcode 345.反转字符串中的元音字母"
question_id: "345"
question: "反转字符串中的元音字母"
problem_url: "https://leetcode.cn/problems/reverse-vowels-of-a-string/"
created: "2020-07-24T23:17:52+08:00"
updated: "2020-07-24T23:17:52+08:00"
upvotes: 0
comments: 0
---

# 345. 反转字符串中的元音字母

> **[yiduobo的每日leetcode 345.反转字符串中的元音字母](https://zhuanlan.zhihu.com/p/163540344) · 知乎 · 2020-07-24 · 赞同 0**
> 力扣：[345. 反转字符串中的元音字母](https://leetcode.cn/problems/reverse-vowels-of-a-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

345.反转字符串中的元音字母<https://leetcode-cn.com/problems/reverse-vowels-of-a-string/>

比较基础的题目。记录下字符串中元音字母的位置，然后根据位置前后两两交换即可。

最后附上python代码：

```python
class Solution(object):
    def reverseVowels(self, s):
        """
        :type s: str
        :rtype: str
        """

        pos_list = []
        for index, char in enumerate(s):
            if char in ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']:
                pos_list.append(index)
        
        reverse_len = len(pos_list)

        res = list(s)
        for index in range(reverse_len/2):
            res[pos_list[index]], res[pos_list[reverse_len - index - 1]] = res[pos_list[reverse_len - index - 1]], res[pos_list[index]]

        return ''.join(res)
```
