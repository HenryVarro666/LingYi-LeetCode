---
title: "12. 整数转罗马数字"
aliases: ["yiduobo的每日leetcode 12.整数转罗马数字"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/array", "leetcode/math", "leetcode/string", "题单/常用数据结构", "题单/面试经典-150-题", "题单/常用数据结构/编程能力强化训练", "题单/面试经典-150-题/数组-/-字符串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/114273942"
zhihu_id: "114273942"
zhihu_title: "yiduobo的每日leetcode 12.整数转罗马数字"
question_id: "12"
question: "整数转罗马数字"
problem_url: "https://leetcode.cn/problems/integer-to-roman/"
difficulty: "Medium"
created: "2020-03-18T21:46:51+08:00"
updated: "2020-03-18T21:46:51+08:00"
upvotes: 0
comments: 0
---

# 12. 整数转罗马数字

> **[yiduobo的每日leetcode 12.整数转罗马数字](https://zhuanlan.zhihu.com/p/114273942) · 知乎 · 2020-03-18 · 赞同 0**
> 力扣：[12. 整数转罗马数字](https://leetcode.cn/problems/integer-to-roman/) · Medium · 灵茶山艾府：[简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

12.整数转罗马数字<https://leetcode-cn.com/problems/integer-to-roman/>

由于每一位上的数字表示方法实际上和其他位上没什么关系，所以最快的应该是按位打表。

正经按位来做的话：

若x \<\= 3，那么是x个单位一。

若x \= 4，那么是单位一拼上单位五。

若x \= 9，那么是单位一拼上单位十。

其他情况，即5 \<\= x \<\= 8，那么是单位五拼上x - 5个单位一。

另外还需要注意高低位的顺序不要弄反了。

最后附上python代码，上面注释掉的部分是正常按位来做，下面的部分是打表：

```
class Solution(object):
    def intToRoman(self, num):
        """
        :type num: int
        :rtype: str
        """

        '''
        one = ['I', 'X', 'C', 'M']
        five = ['V', 'L', 'D', '']
        ten = ['X', 'C', 'M', '']
        res = ''
        pos = 0
        while num > 0:
            k = num % 10
            num /= 10
            if k <= 3:
                res = one[pos] * k + res
            elif k == 4:
                res = one[pos] + five[pos] + res
            elif k == 9:
                res = one[pos] + ten[pos] + res
            else:
                res = five[pos] + one[pos] * (k - 5) + res
            pos += 1

        return res
        '''

        f = [['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX'],
             ['', 'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC'],
             ['', 'C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM'],
             ['', 'M', 'MM', 'MMM']]
        
        res = ''
        pos = 0
        while num > 0:
            res = f[pos][num % 10] + res
            num /= 10
            pos += 1

        return res
```
