---
title: "65. 有效数字"
aliases: ["yiduobo的每日leetcode 65.有效数字"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/常用数据结构", "题单/常用数据结构/三-栈", "题单/常用数据结构/编程能力强化训练"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/129881442"
zhihu_id: "129881442"
zhihu_title: "yiduobo的每日leetcode 65.有效数字"
question_id: "65"
question: "有效数字"
problem_url: "https://leetcode.cn/problems/valid-number/"
difficulty: "Hard"
created: "2020-04-13T22:31:37+08:00"
updated: "2020-04-13T22:31:37+08:00"
upvotes: 0
comments: 0
---

# 65. 有效数字

> **[yiduobo的每日leetcode 65.有效数字](https://zhuanlan.zhihu.com/p/129881442) · 知乎 · 2020-04-13 · 赞同 0**
> 力扣：[65. 有效数字](https://leetcode.cn/problems/valid-number/) · Hard · 灵茶山艾府：[精确总结题目规则，简单实现（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

65.有效数字<https://leetcode-cn.com/problems/valid-number/>

比较复杂的题目，用自动机来做应该是最清晰的，不过我在这里使用的利用各种flag拼凑起来的低配自动机。

对于s中的字符：

1、e字符。最多只能出现一次，且e前面可以是整数或者实数，e后面必须是整数。

2、+号或-号。在e前面和e后面最多分别只能出现一次，且必须出现在最前方。

3、小数点符号。只能出现在e前面，且最多只能出现一次。

4、空格。只能出现在s的头部与尾部连续出现。

5、0-9这些数字。没有出现的限制。

6、其他符号。一旦出现就直接返回False。

那么对于各类字符设置对应的flag，分别为：

1、正负号标记symbol_flag，表示是否已经出现过正负号或者其他冲突的符号。

2、小数点标记point_flag，表示是否已经出现过小数点或者其他冲突的符号。

3、指数标记e_flag，表示是否已经出现过字符e或者其他冲突的符号。

4、数字标记number_flag，表示当前部分是否已经出现过数字。

于是我们首先去掉s头部与尾部的空格，接下来从左到右检测每个字符：

1、如果是正负号:

检测正负号标记symbol_flag。若symbol_flag为True，说明产生了冲突，返回False，否则将symbol_flag置为True。

2、如果是字符e：

首先检测e_flag。若e_flag为True，说明产生了冲突，返回False，否则将e_flag置为True。

接下来检测number_flag，即在字符e之前是否存在数字的部分，如果number_flag为False，说明e之前没有数字存在，返回False。

若上面的检测都通过，那么将e_flag置为True，表示后续不能再出现字符e。将point_flag置为True，表示e后面的指数部分必须是整数，不能是实数。将symbol_flag置为False，表示指数部分还可以出现一次符号。将number_flag也置为False，表示后续还需要出现指数部分的数字。

3、如果是小数点：

检测小数点标记point_flag。若point_flag为True，说明产生了冲突，返回False，否则将point_flag置为True，同时还需要将symbol_flag置为True，因为正负号必须出现在当前部分数字的最前面。

4、如果是0到9这些数字：

将symbol_flag置为True，因为正负号必须出现在当前部分数字的最前面。同时将number_flag置为True，说明已经出现过数字。

5、其他字符：

直接返回False。

当所有字符检测完毕后，如果number_flag为False，说明s中缺少了部分数字，那么返回False，否则返回True。

题目本身不难，但是细节比较多，并且也存在一些感觉很奇怪的case。例如我之前也判断过当小数点直接出现在e之前则返回False，但是存在1.e-5这种case。

最后附上python代码：

```python
class Solution(object):
    def isNumber(self, s):
        """
        :type s: str
        :rtype: bool
        """

        if not s:
            return False

        symbol_flag= False
        point_flag = False
        number_flag = False
        e_flag = False
        left = 0
        right = len(s) - 1
        
        while left < len(s) and s[left] == ' ':
            left += 1

        if left == len(s):
            return False

        while right > -1 and s[right] == ' ':
            right -= 1

        for index in range(left, right + 1):
            char = s[index]
            if char in ['+', '-']:
                if symbol_flag:
                    return False
                symbol_flag = True
            elif char == 'e':
                if e_flag:
                    return False
                if not number_flag:
                    return False
                e_flag = True
                number_flag = False
                point_flag = True
                symbol_flag = False
            elif char == '.':
                if point_flag:
                    return False
                point_flag = True
                symbol_flag = True
            elif ord(char) >= 48 and ord(char) <= 57:
                symbol_flag = True
                number_flag = True
            else:
                return False

        return number_flag
```
