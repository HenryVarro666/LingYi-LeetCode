---
title: "1896. 反转表达式值的最少操作次数"
aliases: ["yiduobo的每日leetcode 1896.反转表达式值的最少操作次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/479614084"
zhihu_id: "479614084"
zhihu_title: "yiduobo的每日leetcode 1896.反转表达式值的最少操作次数"
question_id: "1896"
question: "反转表达式值的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-change-the-final-value-of-expression/"
created: "2022-03-12T01:06:53+08:00"
updated: "2022-03-12T01:06:53+08:00"
upvotes: 1
comments: 0
---

# 1896. 反转表达式值的最少操作次数

> **[yiduobo的每日leetcode 1896.反转表达式值的最少操作次数](https://zhuanlan.zhihu.com/p/479614084) · 知乎 · 2022-03-12 · 赞同 1**
> 力扣：[1896. 反转表达式值的最少操作次数](https://leetcode.cn/problems/minimum-cost-to-change-the-final-value-of-expression/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1896.反转表达式值的最少操作次数

[力扣](https://leetcode-cn.com/problems/minimum-cost-to-change-the-final-value-of-expression/)

非常有水平的题目，对于这个数据规模，只能是O(n)的算法来求解。

O(n^2)的算法相对来说比较容易想到。首先一趟遍历求解表达式的值，并将最上层的表达式拆解开，并根据最后一个运算符以及运算结果来递归求解这个运算符两侧的子表达式。这个做法的缺点是确定最上层表达式需要一趟完整的遍历，但是拆解后可能出现本次操作只是去除了一组括号这种尴尬的情况，因此最终的时间复杂度为O(n^2)。

为了改进这个做法，就必须在遍历的同时计算出最终的结果，而不是表达式的值然后回头再去进行拆解。

由于这里的中间结果只可能是0或者1，那么就可以使用二元组(zero, one)来表示将当前子表达式的值变为0和1所需的最少操作数。注意到题目中的与和或是没有优先级之分的，因此可以一趟扫描求解，过程中利用栈来处理括号。具体来说需要维护一个符号栈和一个结果栈，对于每种字符：

1、对于数字0，变为0不需要操作，变为1需要操作1次，因此其对应了二元组(0, 1)。将其加入到结果栈中。接下来，若此时符号栈不为空，且符号栈顶不是左括号，那么说明此时是一个需要计算的子表达式，那么利用当前符号栈顶的运算符以及结果栈顶的两个二元组来计算出新的二元组。

具体计算规则可以需要分情况讨论。不妨设此时的两个二元组分别为(f_zero, f_one)以及(s_zero, s_one)，那么：

1-1）如果二者之间是或运算，且需要结果为0，就必须要满足二者都为0，因此总的操作次数为or_zero \= f_zero + s_zero

1-2）如果二者之间是或运算，且需要结果为1，那么二者只需要有一个1最终结果就是1，此时就有前0后1，前1后0以及前后都是1三种情况，对应的操作次数分别为f_zero + s_one，f_one + s_zero以及f_one + s_one，那么最终的or_one \= min(f_zero + s_one，f_one + s_zero，f_one + s_one)

1-3）如果二者之间是与运算，且需要结果为0，那么二者只需要有一个0最终结果就是0，此时就有前0后1，前1后0以及前后都是0三种情况，对应的操作次数分别为f_zero + s_one, f_one + s_zero以及f_zero + s_zero，那么最终的and_zero \= min(f_zero + s_one, f_one + s_zero，f_zero + s_zero)

1-4）如果二者之间是与运算，且需要结果为1，就必须要满足二者都为1，因此总的操作次数为and_one \= f_one + s_one

接下来考虑当前的运算符。

若为或，那么如果不变更运算符，此时让运算结果为0和1的操作次数分别就是or_zero和or_one，如果变更操作符，则为and_zero + 1和and_one + 1，因此最终的二元组就是

(min(or_zero, and_zero + 1)，min(or_one, and_one + 1))

同样的，若为与，最终的二元组就是

(min(and_zero, or_zero + 1), min(and_one, or_one + 1))

2、对于数字1，变为0需要1次操作，变为1则不需要操作，因此其对应了二元组(1, 0)，将其加入到结果栈中。接下来，若符号栈不为空且栈顶不是左括号，那么就需要进行计算，计算的过程与情况1完全一样

3、对于左括号、与以及或这三种符号，都只需要直接加入到符号栈中即可

4、对于右括号，此时括号左侧的表达式必然已经计算出结果并存在于结果栈的栈顶，而此时符号栈的栈顶对应的必然是左括号，那么此时就需要左括号弹出。接下来，若符号栈不为空，且符号栈顶不再是左括号，那么说明之前括号内的结果，即对应到结果栈栈顶的二元组需要与之前的表达式进行运算了，此时同样是按情况1中的计算方式进行计算即可

全部遍历完成后，栈中只会剩下一个二元组，分别表示将最终结果变为0需要的操作数以及将最终结果变为1需要的操作数。如果保持原表达式值的话，其需要的操作数必然为0，那么就说明最后这个二元组中较大的那一个就是将表达式值翻转所需的操作数，于是此时只需返回最后这个二元组中的较大值即可。

值得一提的是，上面这种做法的一个前提是运算符除括号为无优先级，那么在同一优先级中就应该按从左到右进行计算。在这里则体现在只要当前有能够计算的表达式就立刻计算结果，相当于表达式中的第二个变量出现时，立马就让第一个变量与其进行运算，从而满足了从左向右计算的要求。而对于括号中的表达式，则通过左括号阻断了向前运算的过程，保证了运算优先级是正确的。

最后附上python代码：

```python
class Solution(object):
    def minOperationsToFlip(self, expression):
        """
        :type expression: str
        :rtype: int
        """

        stack_op = []
        stack_res = []
        for char in expression:
            if char == '0' or char == '1' or char == ')':
                if char == '0':
                    stack_res.append([0, 1])
                elif char == '1':
                    stack_res.append([1, 0])
                else:
                    stack_op.pop()
                
                while stack_op and stack_op[-1] != '(':
                    f_zero, f_one = stack_res.pop()
                    s_zero, s_one = stack_res.pop()
                    or_zero = f_zero + s_zero
                    or_one = min(f_zero + s_one, f_one + s_zero, f_one + s_one)
                    and_zero = min(f_zero + s_one, f_one + s_zero, f_zero + s_zero)
                    and_one = f_one + s_one

                    if stack_op[-1] == '|':
                        and_zero += 1
                        and_one += 1
                    else:
                        or_zero += 1
                        or_one += 1

                    stack_res.append([min(or_zero, and_zero), min(or_one, and_one)])
                    stack_op.pop()
            
            else:
                stack_op.append(char)

        return max(stack_res[0][0], stack_res[0][1])
```
