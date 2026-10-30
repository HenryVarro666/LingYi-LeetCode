---
title: "282. 给表达式添加运算符"
aliases: ["yiduobo的每日leetcode 282.给表达式添加运算符"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/153507740"
zhihu_id: "153507740"
zhihu_title: "yiduobo的每日leetcode 282.给表达式添加运算符"
question_id: "282"
question: "给表达式添加运算符"
problem_url: "https://leetcode.cn/problems/expression-add-operators/"
created: "2020-07-02T22:12:44+08:00"
updated: "2020-07-02T22:12:44+08:00"
upvotes: 0
comments: 0
---

# 282. 给表达式添加运算符

> **[yiduobo的每日leetcode 282.给表达式添加运算符](https://zhuanlan.zhihu.com/p/153507740) · 知乎 · 2020-07-02 · 赞同 0**
> 力扣：[282. 给表达式添加运算符](https://leetcode.cn/problems/expression-add-operators/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

282.给表达式添加运算符<https://leetcode-cn.com/problems/expression-add-operators/>

乍一看也是动态规划的题目，f[i][j]表示i到j这一段可以形成的所有计算结果，然后使用path记录状态的转移过程。不过后来发现，这个状态标识在遇到乘法时不太好处理，例如样例中的'123'，其中f[0][1]可以通过1 + 2得到3，但是f[0][2]并不能通过f[0][1]的3乘上f[2][2]的3得到9，因为这里运算优先级出现了问题。

一种可能的解决方案是先进行一次动态规划，在这里只计算乘法，并将其保存起来。之后再进行一次动态规划，此时只能进行加法或者减法，但是可以直接利用上一轮中乘法的结果。由于乘法在这里优先级是绝对最高的，因此这个做法应该是ok的。

另外，对于其中出现的1 - 2 - 3这种case，这种动态规划的做法会将其视为1 - (2 - 3)，但是1 - 2 - 3的结果会在1 - (2 + 3)这种情况下被计算出来，因此是没有问题的。

不过考虑到path生成非常复杂，且path可能需要将绝大部分状态都储存下来，无论实现的复杂程度还是时空复杂度都是比较高的，那么索性就用暴力搜索来解决好了。

具体做法就是每次枚举切分点，然后对切分点之前这一段形成的数，与当前已经生成的结果now分别进行加法、减法或者乘法操作即可。当整个字符串被搜索完之后，判断now是否等于target即可。

需要注意的是，在这里乘法同样需要特殊处理，于是需要采取经典的做法，将减法看做负数的加法，那么整个过程就变成了加上某数，或者加上某个乘积。当需要进行乘法运算时，只需要将当前的结果减去上一轮的变化量，然后加上这个变化量乘以当前数字的结果即可。

还是样例中的'123'，假设前两轮是now \= 1 + 2 \= 3，那么如果最后需要乘上3，now需要减去第二轮的变化量2，再加上2 \* 3 \= 6，即now \= 3 - 2 + 2 \* 3 \= 7。

又例如'1234'，假设前三轮是now \= 1 - 2 \* 3 \= -5，那么如果最后需要乘上4，now需要减去第三轮的变化量-6，再加上-6 \* 4 \= -24，即now \= -5 - (-6) + (-24) \= -23。

另外，当切分出来的数如果以0开头，但是又不为0，那么就不是合法的数，不应该将其加入到搜索树中。

最后附上python代码：

```python
class Solution(object):
    def addOperators(self, num, target):
        """
        :type num: str
        :type target: int
        :rtype: List[str]
        """

        res = []
        now = 0
        for index, char in enumerate(num):
            if now == 0 and index != 0:
                break
            now = now * 10 + int(char)
            self.dfs(num, index, now, now, str(now), target, res)

        return res

    def dfs(self, num, last_pos, now, last_delta, expr, target, res):
        if last_pos == len(num) - 1:
            if now == target:
                res.append(expr)
            return

        tmp = 0
        for index in range(last_pos + 1, len(num)):
            if tmp == 0 and index != last_pos + 1:
                break
            tmp = tmp * 10 + int(num[index])
            self.dfs(num, index, now + tmp, tmp, expr + '+' + str(tmp), target, res)
            self.dfs(num, index, now - tmp, -tmp, expr + '-' + str(tmp), target, res)
            self.dfs(num, index, now - last_delta + last_delta * tmp, last_delta * tmp, expr + '*' + str(tmp), target, res)
```
