---
title: "736. Lisp语法解析"
aliases: ["yiduobo的每日leetcode 736.Lisp语法解析"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/336468594"
zhihu_id: "336468594"
zhihu_title: "yiduobo的每日leetcode 736.Lisp语法解析"
question_id: "736"
question: "Lisp语法解析"
problem_url: "https://leetcode.cn/problems/parse-lisp-expression/"
created: "2020-12-12T19:23:54+08:00"
updated: "2020-12-12T19:23:54+08:00"
upvotes: 1
comments: 0
---

# 736. Lisp语法解析

> **[yiduobo的每日leetcode 736.Lisp语法解析](https://zhuanlan.zhihu.com/p/336468594) · 知乎 · 2020-12-12 · 赞同 1**
> 力扣：[736. Lisp语法解析](https://leetcode.cn/problems/parse-lisp-expression/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

736.Lisp语法解析

[力扣](https://leetcode-cn.com/problems/parse-lisp-expression/)

题目描述看上去比较复杂，不过总的来说还是遵循从左往右的计算方式，且可以根据表达式中的括号匹配以及空格，将整个表达式分为若干个块。

有了上面这几点，那么大体思路就是先根据括号和空格将表达式分块，根据第一块的内容判断当前应该执行哪种操作，然后对于后续的块进行操作。

具体做法为：

1、若当前字符串的第一个字符为左括号，那么需要去除头尾的括号

2、若当前字符串的第一个字符为数字或者负号，说明整个字符串表示的是一个数字，直接转换为int返回即可。

3、否则就从头开始往后进行扫描，使用一个cnt表示当前未匹配左括号的数量。那么对于一个字符：

3-1、若其为左括号，则cnt加一

3-2、若其为右括号，则cnt减一

3-3、若其为空格，且此时的cnt为0，说明从上一个块的结束位置，到当前位置可以形成一个新的块，于是将其从字符串中分离并储存起来。

扫描完毕后，得到分好的块parts。

4、对于parts：

4-1、若当前parts的长度为1，说明只有一串英文字符串，表示某个变量的名称，于是从变量表中查找该变量的值然后返回

4-2、若当前parts[0]为add，那么分别递归求解parts[1]以及parts[2]，然后返回二者的和

4-3、若当前parts[0]为mul，那么分别递归求解parts[1]以及parts[2]，然后返回二者的积

4-4、否则此时的parts[0]必然为let，那么从parts[1]开始两个一组往后遍历。对于parts[index]以及parts[index + 1]，前者必然是字符串，表示遍历名，那么只需递归求解后者的值，然后修改变量表中对应的值即可。

另外需要注意的是，每个子块都会继承父块的变量值，但是在子块内部如果变量值产生的变化并不会反馈回父块，于是每次递归求解时，都需要先copy一遍变量表，然后让这个copy的版本去进行递归求解，原版保持不动。

最后附上python代码：

```python
class Solution(object):
    def evaluate(self, expression):
        """
        :type expression: str
        :rtype: int
        """

        return self.parse(expression, {})

    def parse(self, exp, value_dict):
        if exp[0] == '(':
            exp = exp[1:-1]
        
        if (exp[0] >= '0' and exp[0] <= '9') or exp[0] =='-':
            return int(exp)
        
        parts = []
        last_pos = 0
        cnt = 0
        for index, char in enumerate(exp):
            if exp[index] == '(':
                cnt += 1
            elif exp[index] == ')':
                cnt -= 1
            elif exp[index] == ' ' and cnt == 0:
                parts.append(exp[last_pos:index])
                last_pos = index + 1
        
        parts.append(exp[last_pos:index + 1])

        tmp_value_dict = value_dict.copy()
        if len(parts) == 1:
            return tmp_value_dict[parts[0]]
        elif parts[0] == 'add':
            v1 = self.parse(parts[1], tmp_value_dict)
            v2 = self.parse(parts[2], tmp_value_dict)
            return v1 + v2
        elif parts[0] == 'mult':
            v1 = self.parse(parts[1], tmp_value_dict)
            v2 = self.parse(parts[2], tmp_value_dict)
            return v1 * v2
        else:
            for index in range(1, len(parts) - 1, 2):
                tmp_value_dict[parts[index]] = self.parse(parts[index + 1], tmp_value_dict)
            return self.parse(parts[-1], tmp_value_dict)
```
