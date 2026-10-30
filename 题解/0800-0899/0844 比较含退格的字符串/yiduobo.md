---
title: "844. 比较含退格的字符串"
aliases: ["yiduobo的每日leetcode 844.比较含退格的字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/347746330"
zhihu_id: "347746330"
zhihu_title: "yiduobo的每日leetcode 844.比较含退格的字符串"
question_id: "844"
question: "比较含退格的字符串"
problem_url: "https://leetcode.cn/problems/backspace-string-compare/"
created: "2021-01-29T22:56:19+08:00"
updated: "2021-01-29T22:56:19+08:00"
upvotes: 0
comments: 0
---

# 844. 比较含退格的字符串

> **[yiduobo的每日leetcode 844.比较含退格的字符串](https://zhuanlan.zhihu.com/p/347746330) · 知乎 · 2021-01-29 · 赞同 0**
> 力扣：[844. 比较含退格的字符串](https://leetcode.cn/problems/backspace-string-compare/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

844.比较含退格的字符串

[力扣](https://leetcode-cn.com/problems/backspace-string-compare/)

乍一看感觉可以从前往后扫描，用栈来解决。但是可以转换思路，如果从后往前来看，将每个碰到的退格键累计起来，然后碰到正常字符时，若现在累计的退格键大于0，那么就跳过该字符然后将退格键累计次数减一。

两个串同时从后往前进行扫描，然后逐个对比当前处理的不会被删除掉的字母是否相同即可。

最后附上python代码：

```python
class Solution(object):
    def backspaceCompare(self, S, T):
        """
        :type S: str
        :type T: str
        :rtype: bool
        """

        i = len(S) - 1
        j = len(T) - 1
        cnt_s = cnt_t = 0
        while i >= 0 or j >= 0:
            while i >= 0:
                if S[i] == '#':
                    cnt_s += 1
                elif cnt_s == 0:
                    break
                else:
                    cnt_s -= 1
                i -= 1
            while j >= 0:
                if T[j] == '#':
                    cnt_t += 1
                elif cnt_t == 0:
                    break
                else:
                    cnt_t -= 1
                j -= 1
            if i < 0:
                if j < 0:
                    return True
                else:
                    return False
            elif j < 0:
                return False
            elif S[i] != T[j]:
                return False
            else:
                i -= 1
                j -= 1

        return True
```
