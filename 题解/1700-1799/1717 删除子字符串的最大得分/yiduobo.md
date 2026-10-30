---
title: "1717. 删除子字符串的最大得分"
aliases: ["yiduobo的每日leetcode 1717.删除子字符串的最大得分"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/450514771"
zhihu_id: "450514771"
zhihu_title: "yiduobo的每日leetcode 1717.删除子字符串的最大得分"
question_id: "1717"
question: "删除子字符串的最大得分"
problem_url: "https://leetcode.cn/problems/maximum-score-from-removing-substrings/"
created: "2021-12-27T22:14:50+08:00"
updated: "2021-12-27T22:14:50+08:00"
upvotes: 0
comments: 0
---

# 1717. 删除子字符串的最大得分

> **[yiduobo的每日leetcode 1717.删除子字符串的最大得分](https://zhuanlan.zhihu.com/p/450514771) · 知乎 · 2021-12-27 · 赞同 0**
> 力扣：[1717. 删除子字符串的最大得分](https://leetcode.cn/problems/maximum-score-from-removing-substrings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1717.删除子字符串的最大得分

[力扣](https://leetcode-cn.com/problems/maximum-score-from-removing-substrings/)

由于题目只能消除'ab'或者'ba'，一旦在某个位置p出现了'a'或'b'以外的字符，那么p之前与p之后的字符串就不可能出现连续的'ab'或者'ba'来进行消除，也就是说p之前和p之后的字符串可以独立计算。更进一步的，实际每个仅包含的'a'和'b'的字符串都是独立计算的，于是可以一趟扫描，每次只计算仅包含'a'和'b'的字符串的得分。

对于一个仅包含'a'或者'b'的字符串，只要里面还有'a'或者'b'，那么至少会出现一组'ab'或者'ba'。换言之，在'a'或者'b'被完全消除之前，总是存在消除的办法的。

对于具体的消除而言，若x大于y，那么肯定是希望多消除'ab'，反过来则是希望多消除'ba'。那么在这里可以用类似括号匹配的方法，若x大于y，那么记'a'为左括号，'b'为右括号，反过来若x小于等于y，则记'a'为右括号，'b'为左括号。然后一趟扫描，记录当前可用左括号的数目l_cnt，并根据当前括号的种类来更新l_cnt以及答案。另外，在这里落单右括号的数目r_cnt也是需要记录的。

扫描完毕后，最后剩下的必然是))...))((...((这种形式的括号组合，那么这里可以通过另一种消除方式得到min(l_cnt, r_cnt)组消除，也需要将这个更新到答案上去。

将上面的结论组合起来就得到了最终的做法：

1、首先根据x和y的大小确定哪个字符表示左括号left，哪个字符表示右括号right

2、初始化l_cnt以及r_cnt为0，然后从头开始向后一趟扫描，对于当前字符：

2-1)若当前字符不为'a'或者'b'，说明当前这一段仅有'a'和'b'的字符串已经完结了，此时需要更新))...))((...((这种形式括号组合带来的影响min(x, y) \* min(l_cnt, r_cnt)，并将l_cnt和r_cnt都重置为0

2-2)若当前字符为对应左括号的字符left，那么将l_cnt加上1

2-3)若当前字符为对应右括号的字符right，那么需要考察当前l_cnt的状况。若l_cnt大于0，说明之前存在一个可用的左括号与当前的右括号匹配，那么将答案加上max(x, y)，并将l_cnt减去1。若l_cnt等于1，说明当前右括号落单了，成为了最终))...))里面的一员，此时应该将r_cnt加上1

需要特别注意的是，上面的做法对于以'a'或'b'结尾的字符串会漏掉最后的))...))((...((，因此可以在一开始就在s的最后加上一个字符'c'来规避这个问题。

最后附上python代码：

```python
class Solution(object):
    def maximumGain(self, s, x, y):
        """
        :type s: str
        :type x: int
        :type y: int
        :rtype: int
        """

        if x > y:
            left = 'a'
            right = 'b'
        else:
            left = 'b'
            right = 'a'

        l_cnt = r_cnt = 0
        res = 0
        s += 'c'
        for index, char in enumerate(s):
            if char == left:
                l_cnt += 1
            elif char == right:
                if l_cnt > 0:
                    res += max(x, y)
                    l_cnt -= 1
                else:
                    r_cnt += 1
            else:
                res += min(x, y) * min(l_cnt, r_cnt)
                l_cnt = r_cnt = 0

        return res
```
