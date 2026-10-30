---
title: "1239. 串联字符串的最大长度"
aliases: ["yiduobo的每日leetcode 1239.串联字符串的最大长度"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/384988920"
zhihu_id: "384988920"
zhihu_title: "yiduobo的每日leetcode 1239.串联字符串的最大长度"
question_id: "1239"
question: "串联字符串的最大长度"
problem_url: "https://leetcode.cn/problems/maximum-length-of-a-concatenated-string-with-unique-characters/"
created: "2021-06-29T12:17:52+08:00"
updated: "2021-06-29T12:17:52+08:00"
upvotes: 0
comments: 0
---

# 1239. 串联字符串的最大长度

> **[yiduobo的每日leetcode 1239.串联字符串的最大长度](https://zhuanlan.zhihu.com/p/384988920) · 知乎 · 2021-06-29 · 赞同 0**
> 力扣：[1239. 串联字符串的最大长度](https://leetcode.cn/problems/maximum-length-of-a-concatenated-string-with-unique-characters/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1239.串联字符串的最大长度

[力扣](https://leetcode-cn.com/problems/maximum-length-of-a-concatenated-string-with-unique-characters/)

由于题目中的字符串中只有小写字母，那么我们可以将所有字符按照二进制编码，即a到z分别对应2^0到2^25。

接下来我们使用一个set储存当前合法的字符串，然后枚举arr中的每个字符串。对于当前字符串s，我们枚举set中的所有字符串t，若s和t没有重复的字符，也就是这两个字符串的编码按位与等于0，那么就可以将s拼接在t后面，并将拼接后的字符串加入到set当中。

枚举完成后，我们只需要检测set中最长的字符串有多长，而这个长度就是num中1的数目，于是可以使用经典的x &\= x - 1来分离出每一个1然后统计。其中的最大值即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxLength(self, arr):
        """
        :type arr: List[str]
        :rtype: int
        """

        num_list = []
        for word in arr:
            num = 0
            flag = True
            for char in word:
                if num & (1 << (ord(char) - 97)):
                    flag = False
                    break
                num |= (1 << (ord(char) - 97))
            
            if flag:
                num_list.append(num)
        
        candidate_set = set([0])
        for num in num_list:
            tmp = set()
            for candidate in candidate_set:
                if candidate & num == 0:
                    tmp.add(candidate | num)
            candidate_set.update(tmp)
        
        res = 0
        for candidate in candidate_set:
            cnt = 0
            while candidate:
                cnt += 1
                candidate &= candidate - 1
            res = max(res, cnt)
        
        return res
```
