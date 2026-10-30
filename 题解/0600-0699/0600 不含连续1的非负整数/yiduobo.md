---
title: "600. 不含连续1的非负整数"
aliases: ["yiduobo的每日leetcode 600.不含连续1的非负整数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/268628958"
zhihu_id: "268628958"
zhihu_title: "yiduobo的每日leetcode 600.不含连续1的非负整数"
question_id: "600"
question: "不含连续1的非负整数"
problem_url: "https://leetcode.cn/problems/non-negative-integers-without-consecutive-ones/"
difficulty: "Hard"
created: "2020-10-25T22:31:00+08:00"
updated: "2020-10-25T22:31:00+08:00"
upvotes: 1
comments: 0
---

# 600. 不含连续1的非负整数

> **[yiduobo的每日leetcode 600.不含连续1的非负整数](https://zhuanlan.zhihu.com/p/268628958) · 知乎 · 2020-10-25 · 赞同 1**
> 力扣：[600. 不含连续1的非负整数](https://leetcode.cn/problems/non-negative-integers-without-consecutive-ones/) · Hard · 灵茶山艾府：[数位 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

600.不含连续1的非负整数<https://leetcode-cn.com/problems/non-negative-integers-without-consecutive-ones/submissions/>

乍一看感觉应该可以用组合数学来解决，但是最终没有想出可行的做法，只能老老实实用动态规划来做了。

定义f[i]为二进制下长度为i的合法整数个数，注意这里的长度为i可以存在前导0。

首先，边界条件有f[1] \= 2，即0和1都合法。

接下来，对于f[i]，若其最高位为0，那么此时就相当于长度为i - 1的合法整数个数。若其最高位为1，那么其次高位必须是0，那么此时就相当于长度为i - 2的合法整数个数。因此就有

f[i] \= f[i - 1] + f[i - 2]

为了适配上面的递推式，我们额外定义f[0] \= 1。

计算出f数组之后，接下来我们考察n的二进制表示，设其长度为l：

首先，其最高位显然是1，因此所有最高位为0的长度为l的合法整数均可以加入到答案中，即f[l - 1]

接下来，从次高位开始逐个往后考虑：

1、若当前位为0，那么直接往后考虑下一位。

2、若当前位为1，设当前处理到第index位，此时必然是如1xx...x1yy...y的形式，我们可以将以1xx...x0开头的合法的整数加入到答案中。因为当前是第index位，后面还有第0到index - 1共index个数，所以此时应该将f[index]加入到答案中。

另外，还需要考虑一种情况，即上一位也为1，即此时是1xx...x11yy...y的形式。

我们在处理上一位的时候已经将1xx...x00yy...y到1xx...x01yy...y中的所有合法整数加入到了答案中，而我们在处理当前位的时候，考虑到的是1xx...x10yy...y这种形式的所有合法整数。由于1xx...x11yy...y这种形式的整数必然是不合法的，因此在处理完当前位之后就没有其他合法的情况了，因此可以直接返回res。

若整个遍历完成，说明不存在上面这种有两个连续1的情况出现，即n这个数本身也是合法的。我们在上面的遍历，都是遇1考虑后面的0，而遇0直接跳过，因此n这个数本身我们不会将其加入到答案中，所以在这里应该加1后再返回，表示n本身也是一个合法的整数。

最后附上python代码：

```python
class Solution(object):
    def findIntegers(self, num):
        """
        :type num: int
        :rtype: int
        """

        bits = []
        while num:
            bits.append(num % 2)
            num /= 2
        
        l = len(bits)
        f = [1, 2]
        for index in range(2, l):
            f.append(f[-1] + f[-2])
        
        res = f[l - 1]
        for index in range(l - 2, -1, -1):
            if bits[index] == 1:
                res += f[index]
                if bits[index + 1] == 1:
                    return res
            
        return res + 1
```
