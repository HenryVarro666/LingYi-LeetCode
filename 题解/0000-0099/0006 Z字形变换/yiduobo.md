---
title: "6. Z字形变换"
aliases: ["yiduobo的每日leetcode 6.Z字形变换"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/113207239"
zhihu_id: "113207239"
zhihu_title: "yiduobo的每日leetcode 6.Z字形变换"
question_id: "6"
question: "Z字形变换"
problem_url: "https://leetcode.cn/problems/zigzag-conversion/"
created: "2020-03-14T19:54:37+08:00"
updated: "2020-03-14T19:54:37+08:00"
upvotes: 0
comments: 0
---

# 6. Z字形变换

> **[yiduobo的每日leetcode 6.Z字形变换](https://zhuanlan.zhihu.com/p/113207239) · 知乎 · 2020-03-14 · 赞同 0**
> 力扣：[6. Z字形变换](https://leetcode.cn/problems/zigzag-conversion/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

6.Z字形变换<https://leetcode-cn.com/problems/zigzag-conversion/>

找规律的题目。

注意到题目说的虽然是Z字形变换，但是实际上按照竖钩的形式进行划分会更加清晰。例如第二个样例LEETCODEISHIRING，变换之后为

L D R

E O E I I

E C I H N

T S G

对于每个竖钩而言，竖线上共有numRows个字符，钩子上共有numRows - 2个字符，那么每个部分一共有numRows \* 2 - 2个字符。令mod \= numRows \* 2 - 2，那么对于一个长度为len(s)的串，一共就有k \= (len(s) - 1) / mod + 1个部分。

对于每个部分，竖线上的字符在原字符串中的位置为index \* mod + row，其中index代表当前是第几个竖钩，row代表当前是第几行(从0开始到numRows - 1)。钩子上则需要注意此时在原串中靠前的字符是从下往上生成的，因此在原串中的位置为index \* mod + mod - row。

现在已经知道变换后的每个字符在原串中对应的位置，那么两重循环numRows与k，依次计算每个对应字符的位置然后加到答案中即可。

简单起见，先单独处理第0行，然后处理中间1到numRows - 2这些带钩子的行，最后再单独处理numRows - 1行。

最后附上python代码：

```python
class Solution(object):
    def convert(self, s, numRows):
        """
        :type s: str
        :type numRows: int
        :rtype: str
        """

        if numRows == 1:
            return s

        res = ''
        mod = numRows * 2 - 2
        length = len(s)

        k = (length - 1) / mod + 1

        for index in range(k):
            res = res + s[index * mod]
        
        for row in range(1, numRows - 1):
            for index in range(k):
                pos = index * mod + row
                if pos < length:
                    res += s[pos]
                pos = index * mod + mod - row
                if pos < length:
                    res += s[pos]

        for index in range(k):
            pos = index * mod + numRows - 1
            if pos < length:
                res += s[pos]

        return res
```
