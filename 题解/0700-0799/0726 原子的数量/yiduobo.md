---
title: "726. 原子的数量"
aliases: ["yiduobo的每日leetcode 726.原子的数量"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/334798971"
zhihu_id: "334798971"
zhihu_title: "yiduobo的每日leetcode 726.原子的数量"
question_id: "726"
question: "原子的数量"
problem_url: "https://leetcode.cn/problems/number-of-atoms/"
difficulty: "Hard"
created: "2020-12-08T22:59:08+08:00"
updated: "2020-12-08T22:59:08+08:00"
upvotes: 1
comments: 0
---

# 726. 原子的数量

> **[yiduobo的每日leetcode 726.原子的数量](https://zhuanlan.zhihu.com/p/334798971) · 知乎 · 2020-12-08 · 赞同 1**
> 力扣：[726. 原子的数量](https://leetcode.cn/problems/number-of-atoms/) · Hard · 灵茶山艾府：[Golang 栈+map 双百](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

726.原子的数量

[力扣](https://leetcode-cn.com/problems/number-of-atoms/)

题目描述看上去很复杂，但是仔细分析，抛开化学知识来看，可以看做给出一个表达式，里面有若干代数符号以及加法、乘法、括号这三种操作，求表达式中各个代数符号最终出现的次数。那么对于这类问题，经典的做法就是从左往右一趟扫描，碰到括号时将当前统计值压栈，处理完括号里面的内容之后再弹栈合并结果。

注意到这里的乘法操作，系数是在元素符号后面的，因此我们可以适当转换思路，从后往前进行扫描，遇到右括号时进行压栈操作，左括号则弹栈合并，于是现在的做法为使用now_multi表示当前元素的系数，now_element表示当前元素符号，now_dict则储存当前各个元素出现的次数，然后从右往左一趟扫描，对于当前字符char：

1、若该字符为数字，那么有now_multi \= char + now_multi，表示将其并入系数字符串。这里使用字符串的原因每次需要将char加到now_multi的最高位，使用字符串比使用整数会方便一些。

2、若该字符为右括号，那么就将now_multi以及now_dict压入栈中，同时清空now_multi以及now_dict。

3、若该字符为左括号，说明括号中的内容已经结束。此时括号中的所有元素都应该乘以栈顶的multi，于是我们弹出栈顶，得到pre_multi以及pre_dict。接下来将now_dict中所有元素出现的次数都乘以pre_multi，然后与pre_dict合并得到当前的now_dict。

4、若该字符为小写字符，说明这个字符只是某个元素的一个部分，因此有now_element \= char + now_element。

5、若该字符为大写字符，说明这个字符是某个元素的起始字符，那么先执行now_element \= char + now_element，此时的now_element就是该元素的完整名称，然后需要将其加入到now_dict当中。需要注意的是，若此时的now_multi为空，说明应该累加1次，否则就是累加now_multi次。加入now_dict后，还需要情况now_multi以及now_dict。

一趟扫描完毕后，按字典序统计now_dict中各个元素出现的次数，拼接后输出即可。需要注意这里出现1次的元素同样不要带上系数。

最后附上python代码：

```python
class Solution(object):
    def countOfAtoms(self, formula):
        """
        :type formula: str
        :rtype: str
        """

        stack = []
        now_multi = ''
        now_element = ''
        now_dict = {}

        for index in range(len(formula) - 1, -1, -1):
            if formula[index] >= '0' and formula[index] <= '9':
                now_multi = formula[index] + now_multi
            elif formula[index] == ')':
                if now_multi == '':
                    stack.append([1, now_dict])
                else:
                    stack.append([int(now_multi), now_dict])
                    now_multi = ''
                now_dict = {}
            elif formula[index] == '(':
                pre_multi, pre_dict = stack.pop()
                for key in now_dict:
                    now_dict[key] *= pre_multi
                for key in pre_dict:
                    now_dict[key] = now_dict.get(key, 0) + pre_dict[key]
            elif formula[index] >= 'a' and formula[index] <= 'z':
                now_element = formula[index] + now_element
            else:
                now_element = formula[index] + now_element
                if now_multi == '':
                    now_dict[now_element] = now_dict.get(now_element, 0) + 1
                else:
                    now_dict[now_element] = now_dict.get(now_element, 0) + int(now_multi)
                now_multi = ''
                now_element = ''

        res = ''
        for element, cnt in sorted(now_dict.items(), key=lambda d:d[0]):
            res += element
            if cnt > 1:
                res += str(cnt)

        return res
```
