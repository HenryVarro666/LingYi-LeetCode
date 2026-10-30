---
title: "1370. 上升下降字符串"
aliases: ["yiduobo的每日leetcode 1370.上升下降字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/400477210"
zhihu_id: "400477210"
zhihu_title: "yiduobo的每日leetcode 1370.上升下降字符串"
question_id: "1370"
question: "上升下降字符串"
problem_url: "https://leetcode.cn/problems/increasing-decreasing-string/"
created: "2021-08-16T23:17:44+08:00"
updated: "2021-08-16T23:17:44+08:00"
upvotes: 1
comments: 0
---

# 1370. 上升下降字符串

> **[yiduobo的每日leetcode 1370.上升下降字符串](https://zhuanlan.zhihu.com/p/400477210) · 知乎 · 2021-08-16 · 赞同 1**
> 力扣：[1370. 上升下降字符串](https://leetcode.cn/problems/increasing-decreasing-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1370.上升下降字符串

[力扣](https://leetcode-cn.com/problems/increasing-decreasing-string/)

比较基础的题目，做法多种多样。我在这里采用的做法是使用两个栈分别维护正向和反向的剩余字符数目。

首先统计字符串中各个字符出现的次数，然后将这些字符以及次数按z到a的顺序压入栈f中，那么f的顶部就是最小的字符。

我们逐个弹出f中的字符，并将对应的字符加入到答案中，同时将对应的次数减1。若次数大于0，那么我们将其压入到反向栈g中。

f弹空后，我们就得到了一轮正序的字符串，同时此时的栈g中储存的就是反向的字符以及对应的次数。

同样地，我们逐个弹出g中字符，将其对应的字符加入到答案中，同时将对应的次数减1。若次数大于0，那么我们将其压入到正向栈f中。

重复上面的过程，直到某一时刻两个栈都为空。

最后附上python代码：

```python
class Solution(object):
    def sortString(self, s):
        """
        :type s: str
        :rtype: str
        """

        char_dict = {}
        for char in s:
            char_dict[char] = char_dict.get(char, 0) + 1
        
        f = []
        g = []
        for index in range(26, 0, -1):
            char = chr(index + 96)
            if char in char_dict:
                f.append([char, char_dict[char]])
            
        
        res = []
        flag = True
        while True:
            if flag:
                while f:
                    char, num = f[-1]
                    f.pop()
                    res.append(char)
                    if num > 1:
                        g.append([char, num - 1])
                
                if not g:
                    break
            else:
                while g:
                    char, num = g[-1]
                    g.pop()
                    res.append(char)
                    if num > 1:
                        f.append([char, num - 1])
            
                if not f:
                    break

            flag = not flag
            
        return ''.join(res)
```
