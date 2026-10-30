---
title: "1541. 平衡括号字符串的最少插入次数"
aliases: ["yiduobo的每日leetcode 1541.平衡括号字符串的最少插入次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/simulation", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/424244097"
zhihu_id: "424244097"
zhihu_title: "yiduobo的每日leetcode 1541.平衡括号字符串的最少插入次数"
question_id: "1541"
question: "平衡括号字符串的最少插入次数"
problem_url: "https://leetcode.cn/problems/minimum-insertions-to-balance-a-parentheses-string/"
difficulty: "Medium"
rating: 1759
created: "2021-10-22T18:58:58+08:00"
updated: "2021-10-22T18:58:58+08:00"
upvotes: 0
comments: 0
---

# 1541. 平衡括号字符串的最少插入次数

> **[yiduobo的每日leetcode 1541.平衡括号字符串的最少插入次数](https://zhuanlan.zhihu.com/p/424244097) · 知乎 · 2021-10-22 · 赞同 0**
> 力扣：[1541. 平衡括号字符串的最少插入次数](https://leetcode.cn/problems/minimum-insertions-to-balance-a-parentheses-string/) · Medium · 灵茶山艾府：[【套路】合法括号字符串，附相似题目（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1541.平衡括号字符串的最少插入次数

[力扣](https://leetcode-cn.com/problems/minimum-insertions-to-balance-a-parentheses-string/)

题目要求使用两个连续的右括号来匹配左括号，那么任意时刻可能出现，且合法的情况必然是形如 ((((..( 或者 ((((..()

其中，左括号可以由任意多个，而右括号的数量只能是0或者1。当右括号有2个时，则可以根据目前是否有左括号来判断如何插入，具体来说：

1、若当前括号为左括号，且目前已有合法括号形如 ((((..()：

1-1）若此时左括号数量大于0，那么此时只需要添加一个右括号，将最后的右括号以及与之前的左括号去掉，然后再将当前的左括号添加到末尾，也就是说已有合法括号去掉了最后的右括号变成了((((..(。此时需要将答案加上1

1-2）若当前括号为左括号数量为0，那么此时需要添加一个左括号和一个右括号，然后再将当前的左括号添加到末尾，也就是说已有合法括号变成了一个单独的左括号。此时需要将答案加上2

2、若当前括号为左括号，且目前已有合法括号形如((((..(：

此时只需要将当前的左括号添加到合法括号末尾即可

3、若当前括号为右括号，且目前已有合法括号形如 ((((..()：

3-1）若此时左括号数量大于0，那么此时在合法括号末尾添加右括号之后，恰好就形成了一组匹配的括号，于是此时将合法括号末尾的一个左括号以及一个右括号移除后即可

3-2）若此时左括号数量为0，那么此时需要添加一个左括号，然后去除掉最后的右括号。此时需要将答案加上1

4、若当前括号为右括号，且目前已有合法括号形如((((..(：

此时只需要将当前的右括号添加到合法括号末尾即可

扫描完成后，若当前合法括号串的末尾为右括号，则需要根据之前是否有左括号决定需要添加几个括号。除此之外，对于最后剩下的左括号，还需要逐个添加两个右括号来适配。

具体实现时，无需维护整个括号串，只需要统计目前已有左括号以及右括号数目即可。

最后附上python代码：

```python
class Solution(object):
    def minInsertions(self, s):
        """
        :type s: str
        :rtype: int
        """

        left = right = 0
        res = 0
        for char in s:
            if char == '(':
                if right == 1:
                    if left > 0:
                        left -= 1
                        res += 1
                    else:
                        res += 2
                
                left += 1
                right = 0
            else:
                if right == 1:
                    if left > 0:
                        left -= 1
                    else:
                        res += 1
                    right = 0
                else:
                    right += 1
        
        if right == 1:
            res += 1
            if left > 0:
                left -= 1
            else:
                res += 1
        
        res += left * 2
        return res
```
