---
title: "856. 括号的分数"
aliases: ["yiduobo的每日leetcode 856.括号的分数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/348911231"
zhihu_id: "348911231"
zhihu_title: "yiduobo的每日leetcode 856.括号的分数"
question_id: "856"
question: "括号的分数"
problem_url: "https://leetcode.cn/problems/score-of-parentheses/"
created: "2021-02-05T23:56:51+08:00"
updated: "2021-02-05T23:56:51+08:00"
upvotes: 0
comments: 0
---

# 856. 括号的分数

> **[yiduobo的每日leetcode 856.括号的分数](https://zhuanlan.zhihu.com/p/348911231) · 知乎 · 2021-02-05 · 赞同 0**
> 力扣：[856. 括号的分数](https://leetcode.cn/problems/score-of-parentheses/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

856.括号的分数

[力扣](https://leetcode-cn.com/problems/score-of-parentheses/)

对于一个括号字符串，我们可以分情况进行讨论：

1、若整个串长度为2：

说明此时字符串就是'()'，那么返回1

2、字符串的首字符必然是'('，那么我们可以寻找其配对的右括号的位置：

2-1）若其匹配的右括号是最后一个字符：

说明此时字符串必然是'(XXXXX)'的形式，因此我们可以递归求解其中的XXXXX，然后将其结果乘以2返回

2-2）若其匹配的右括号不是最后一个字符：

说明此时字符串必然是'(XXXXX)YYYYY'的形式，因此我们可以递归求解其中的(XXXXX)和YYYYY，然后返回二者之和

到了这里，就可以很容易的按照上面分情况讨论的结果设计出一种递归的算法了。

但是需要注意的是，这种做法对于极端数据是不太友好的，例如'(((())))'，实际上每次都需要扫描内部重叠的字符串，浪费了很多操作，是一种O(n^2)的做法。

注意到这里只有乘以2以及加和这两种操作，那么对于一个嵌套了k层之后的简单闭合括号'()'，其分数计算方式应该是

(((((1 + other[k]) \* 2 + other[k - 1]) \* 2) + ...)) + other[1]) \* 2

其中other表示字符串中同一层其他括号的分数

如果我们将这个式子打开，那么就可以发现对于第k层的每个简单括号，其都将为答案添加2^k的得分，而这里的k正是当前从左到右扫描过程中未闭合左括号的数量。于是现在就有了一种更好的做法，从左往右开始进行一趟扫描：

1、若当前字符为左括号：

将cnt加上1，表示左括号嵌套的层数加一

2、若当前字符为右括号：

将cnt减去1，表示左括号嵌套的层数减一。同时若上一个字符为左括号，那么此时出现了一组嵌套cnt层的简单闭合括号，因此还需要将答案加上2^cnt

最后附上python代码：

```python
class Solution(object):
    def scoreOfParentheses(self, S):
        """
        :type S: str
        :rtype: int
        """

        cnt = 0
        res = 0
        for index, char in enumerate(S):
            if char == '(':
                cnt += 1
            else:
                cnt -= 1
                if S[index - 1] == '(':
                    res += (1 << cnt)
        
        return res
```
