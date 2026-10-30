---
title: "984. 不含AAA或BBB的字符串"
aliases: ["yiduobo的每日leetcode 984.不含AAA或BBB的字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/363803471"
zhihu_id: "363803471"
zhihu_title: "yiduobo的每日leetcode 984.不含AAA或BBB的字符串"
question_id: "984"
question: "不含AAA或BBB的字符串"
problem_url: "https://leetcode.cn/problems/string-without-aaa-or-bbb/"
created: "2021-04-10T18:44:27+08:00"
updated: "2021-04-10T18:44:27+08:00"
upvotes: 0
comments: 0
---

# 984. 不含AAA或BBB的字符串

> **[yiduobo的每日leetcode 984.不含AAA或BBB的字符串](https://zhuanlan.zhihu.com/p/363803471) · 知乎 · 2021-04-10 · 赞同 0**
> 力扣：[984. 不含AAA或BBB的字符串](https://leetcode.cn/problems/string-without-aaa-or-bbb/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

984.不含AAA或BBB的字符串

[力扣](https://leetcode-cn.com/problems/string-without-aaa-or-bbb/)

当a和b的数量一样时，直接让二者交替出现即可，因此现在就只需要想办法抹平二者数量上的差距。当a比较多时，由于不能出现连续的三个a，那么我们需要使用两个a一个b的组合，通过b来分割这两个a与其他的a，同时也达到了来减少a的数量的目的。同理，当b比较多时则使用两个b一个a减少b的数量。

受到样例2的启发，两个a一个b的组织形式应该是aab，这样后续要有机会使用掉多出的a。同样的，两个b一个a则应该写成bba。

接下来，当a的数量和b的数量不为零，且二者数量不相等时，就不同通过生成aab或bba来抹平二者数量的差值，直到其中一方数量为0或者二者数量相等。

此时会产生3种情况：

1、a用完了，b还剩下，那么说明执行过程中b的数量也必然大于a的数量，也就是说已经生成的字符串应该是bbabba...bba这种形式，那么此时将剩下的b添加到答案末尾即可。

2、b用完了，a还剩下，与情况1类似，将剩下的a添加到答案末尾即可。

3、a和b还剩下，且此时数量相同。由于不清楚之前是按aab还是bba生成的字符串，那么需要判断当前已生成字符串的最后一个字符是a还是b。若为a，那么就可以将剩下的a和b写成若干组ba的形式接在答案后面。同样地，若为b，则写成若干组ab的形式接在答案后面。

最后附上python代码：

```python
class Solution(object):
    def strWithout3a3b(self, a, b):
        """
        :type a: int
        :type b: int
        :rtype: str
        """

        res = ''
        while a > 0 and b > 0 and a != b:
            if a > b:
                res += 'aab'
                a -= 2
                b -= 1
            else:
                res += 'bba'
                a -= 1
                b -= 2
        
        if a == b:
            if len(res) > 0 and res[-1] == 'a':
                tmp = 'ba'
            else:
                tmp = 'ab'
            res += tmp * a
        elif a > 0:
            res += 'a' * a
        else:
            res += 'b' * b

        return res
```
