---
title: "770. 基本计算器IV"
aliases: ["yiduobo的每日leetcode 770.基本计算器IV"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/339636227"
zhihu_id: "339636227"
zhihu_title: "yiduobo的每日leetcode 770.基本计算器IV"
question_id: "770"
question: "基本计算器IV"
problem_url: "https://leetcode.cn/problems/basic-calculator-iv/"
created: "2020-12-26T01:30:12+08:00"
updated: "2020-12-26T01:30:12+08:00"
upvotes: 0
comments: 1
---

# 770. 基本计算器IV

> **[yiduobo的每日leetcode 770.基本计算器IV](https://zhuanlan.zhihu.com/p/339636227) · 知乎 · 2020-12-26 · 赞同 0**
> 力扣：[770. 基本计算器IV](https://leetcode.cn/problems/basic-calculator-iv/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

770.基本计算器IV

[力扣](https://leetcode-cn.com/problems/basic-calculator-iv/)

这题算是在leetcode做题以来，做过最难写的一题。这里的难写并不是指的算法难写，而是构造题目要求的数据结构有点复杂，而且没有什么优化的想法。

题目要求计算一个代数表达式的值，其中可能包含加减乘、括号以及字符串代表的变量。

首先，若expression中不包含空格，那么说明expression是一个独立的整体，可以直接判断其属于常量、变量还是操作符。

接下里，若expression中包含空格，那么需要将expression中的每个部分都解析出来。考虑到其中可能存在括号，我在这里采取的做法为记录当前区间的起点start_pos\=0，然后从头开始向后遍历expression：

1、若当前字符为左括号，则cnt加一

2、若当前字符为右括号，则cnt减一

3、若当前字符为空格，且cnt为0：

此时的空格为分隔符，且括号时正确匹配的，那么从start_pos到当前位置这一段就是一个合法的子表达式，可以对其进行递归求解。若上一个字符为右括号，说明这一段是必然是(XXXX)的形式，因此递归求解时应该剥离掉两侧的括号。

对于每个一段的结果，其都是一个单独的list，而这个list是由一个或多个二元组以及操作符组成的。这里二元组的定义为 [系数, {变量 : 幂次}]，例如2\*a\*a\*b，就表示为[2, {a : 2, b : 1}]。

完成这个分离的过程之后，得到的是一个有操作符间隔的list，具体形式为

[part_0, opt_1, part_1, ... , opt_k, part\_(k+1)]

例如样例中的(e + 8) \* (e - 8)，我们假设已经递归求解了两个括号中的内容，那么此时得到的list为\[\[\[1, {e:1}\], \[8, {}\]\], '\*', \[\[1, {e:1}\], \[-8, {}\]\]\]

那么我们接下里的目标就是将这个list中的各个part通过opt合并起来，得到最终结果

\[\[1, {e:2}\], \[-64, {}\]\]

由于这里面的opt可能存在乘号，因此我在这里采用的是从头到尾一趟遍历，使用栈来储存当前的结果，首先栈中压入part_0，然后从opt_1和part_1开始成对往后遍历：

1、若当前opt为加号，那么直接将part压入栈中

2、若当前opt为减号，那么将part中所有所有系数全部取负，然后将part压入栈中

3、若当前opt为乘号，那么将栈顶的last_part弹出，然后逐个遍历part和last_part中的所有元素，两两相乘之后得到新的{变量 ：幂次}，而此时的系数则为两个part的系数相乘。然后将这个新的系数和幂次dict再重新压入栈中。

例如对于上面样例(e + 8) \* (e - 8)这一段，list为

\[\[\[1, {e:1}\], \[8, {}\]\], '\*', \[\[1, {e:1}\], \[-8, {}\]\]\]

1、首先将\[\[1, {e:1}\], \[8, {}\]\]压入栈中

2、接下来遇到'\*'与\[\[1, {e:1}\], \[-8, {}\]\]，此时将栈顶的\[\[1, {e:1}\], \[8, {}\]从栈中弹出，然后逐个遍历两个part中的所有元素，然后两两进行乘法，分别为

last_part的[1, {e:1}]与part的[1, {e:1}]，得到[1, {e:2}]

last_part的[1, {e:1}]与part的[-8, {}]，得到[-8, {e:1}]

last_part的[8, {}]与part的[1, {e:1}]，得到[8, {e:1}]

last_part的[8, {}]与part的[-8, {}]，得到[-64, {}]

此时得到的新part为\[\[1, {e:2}\], \[-8, {e:1}\], \[8, {e:1}\], \[-64, {}\]\]，将其压入栈中

3、此时遍历完成，栈中最后剩下的就是执行完乘法与减法的结果，我们还需要将其各个相同的部分进行合并

对于合并操作，我在这里采用的是先将幂次dict转化为字符串的形式，然后使用一个dict来进行合并。对于上面的样例，此时有\[\[1, {e:2}\], \[-8, {e:1}\], \[8, {e:1}\], \[-64, {}\]\]，依次遍历，分别得到的是

[1, {e:2}]：字符串e^2，权重1

[-8, {e:1}]：字符串e^1，权重-8

[8, {e:1}]：字符串e^1，权重8

[-64, {}]：空字符串，权重64

那么通过dict合并之后，结果dict就是{"e^2" : 1, "e^1" : 0, '' : 64}，然后再将其中权重非0的key转化回二元组的形式，最终就得到了答案\[\[1, {e:2}\], \[-64, {}\]\]

得到最后结果之后，还需要将其中各个表达式通过乘号拼接，并按照次数第一、字典序第二的顺序进行排序后才能输出。

总结下来，这道题目首先是对于括号在表达式中的处理，然后是栈在加减以及乘法运算中的运用，最后则是幂次的储存以及合并。算法并不难，但是实现起来还是比较复杂的。

题解的每一步顺序都是跟代码对应的，对照着看应该比较清晰。最后附上python代码：

```python
class Solution(object):
    def basicCalculatorIV(self, expression, evalvars, evalints):
        """
        :type expression: str
        :type evalvars: List[str]
        :type evalints: List[int]
        :rtype: List[str]
        """
        var_dict = {}
        for var, value in zip(evalvars, evalints):
            var_dict[var] = value

        parse_list = self.parse(expression, var_dict)
        res_list = []
        for index in range(len(parse_list)):
            c, power_dict = parse_list[index]
            if c != 0:
                exp = '*'.join(['*'.join([char] * power_dict[char]) for char in sorted(power_dict.keys())])
                d = sum(power_dict.values())
                if d > 0:
                    res_exp = str(c) + '*' + exp
                else:
                    res_exp = str(c)
                res_list.append([-d, c, exp, res_exp])

        return [x[-1] for x in sorted(res_list, key=lambda d:(d[0], d[2]))]

    def parse(self, expression, var_dict):
        if expression.find(' ') == -1:
            if expression[0] in ('+', '-', '*'):
                return expression[0]
            if expression[0] == '(':
                expression = expression[1 : len(expression) - 1]
            if expression in var_dict:
                return [[var_dict[expression], {}]]
            elif expression[0] >= '0' and expression[0] <= '9':
                return [[int(expression), {}]]
            else:
                return [[1, {expression : 1}]]

        part_list = []
        cnt = 0
        start_pos = 0
        now = 0
        while now < len(expression):
            char = expression[now]
            if char == '(':
                cnt += 1
            elif char == ')':
                cnt -= 1
            elif char == ' ' and cnt == 0:
                if expression[now - 1] == ')':
                    part_list.append(self.parse(expression[start_pos + 1 : now - 1], var_dict))
                else:
                    part_list.append(self.parse(expression[start_pos : now], var_dict))
                start_pos = now + 1

            now += 1

        if expression[-1] == ')':
            part_list.append(self.parse(expression[start_pos + 1 : len(expression) - 1], var_dict))
        else:
            part_list.append(self.parse(expression[start_pos : len(expression)], var_dict))
        stack = [part_list[0]]
        for index in range(1, len(part_list), 2):
            operator = part_list[index]
            now = part_list[index + 1]
            if operator == '+':
                stack.append(now)
            elif operator == '-':
                stack.append([[c * -1, power_dict] for c, power_dict in now])
            else:
                last = stack.pop()
                tmp = []
                for c1, power_dict1 in last:
                    for c2, power_dict2 in now:
                        tmp_dict = {}
                        for char, power in power_dict1.items():
                            tmp_dict[char] = power
                        for char, power in power_dict2.items():
                            tmp_dict[char] = tmp_dict.get(char, 0) + power
                        tmp.append([c1 * c2, tmp_dict.copy()])

                stack.append(tmp)
                
        key_dict = {}
        for parts in stack:
            for c, var_dict in parts:
                var_key = '*'.join([key + '^' + str(var_dict.get(key)) for key in sorted(var_dict.keys())])
                key_dict[var_key] = key_dict.get(var_key, 0) + c

        res_list = []
        for key, c in key_dict.items():
            if c == 0:
                continue
            res_list.append([c, {}])
            if key != '':
                for char_power in key.split('*'):
                    char, power = char_power.split('^')
                    res_list[-1][1][char] = int(power)
        
        return res_list
```
