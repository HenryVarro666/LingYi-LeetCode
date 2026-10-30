---
title: "2801. 统计范围内的步进数字数目"
aliases: ["yiduobo的每日leetcode 2801.统计范围内的步进数字数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/memoization", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/657494978"
zhihu_id: "657494978"
zhihu_title: "yiduobo的每日leetcode 2801.统计范围内的步进数字数目"
question_id: "2801"
question: "统计范围内的步进数字数目"
problem_url: "https://leetcode.cn/problems/count-stepping-numbers-in-range/"
difficulty: "Hard"
rating: 2367
created: "2023-09-21T03:48:10+08:00"
updated: "2023-09-21T03:48:10+08:00"
upvotes: 0
comments: 0
---

# 2801. 统计范围内的步进数字数目

> **[yiduobo的每日leetcode 2801.统计范围内的步进数字数目](https://zhuanlan.zhihu.com/p/657494978) · 知乎 · 2023-09-21 · 赞同 0**
> 力扣：[2801. 统计范围内的步进数字数目](https://leetcode.cn/problems/count-stepping-numbers-in-range/) · Hard · 灵茶山艾府：[数位 DP 通用模板](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2801.统计范围内的步进数字数目

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/count-stepping-numbers-in-range/)

非常标准的数位动态规划问题，令f[level][last][flag]表示填充了某个步进数的前level位数字，其中level这一位的值为last，且当前数字与low和high的上下界关系以及当前数字是否还处于前导0的状态为flag时的可行方案数。

这里先说明一下前导0的问题。

由于题目给出的low和high位数可能不同，为了方便起见，我在这里选择统一填充一个长度为len(high)的数，但是当low的位数比high的位数要少时，则可能存在位数较少但是也符合条件的数，因此在这里就需要使用前导0来进行填充这些数字，使得这些数字的位数达到len(high)。但是需要注意的是，在使用前导0时是无需考虑步进数字相邻位之间差1这条规则的，因此需要一个标记来表示当前填充的位置是否紧挨着前导0，如果是，那么当前位就可以无视相邻位差1。而对于前导0标记的设置，则需要满足当前位上一位也是前导0，且当前位填充的是0，同时low的位数没达到当前位。在这里可以先将low的位数也填充到len(high)，那么最后这个判断就可以直接通过0是否小于low当前位来达成了。

除了上面的前导0标记外，还需要常规的上下界表示，因此flag在这里是一个3位的二进制数，其中最高位用来储存前导0的标记，而中间和最低位则分别表示当前构造的数是否与上界high以及下界low的前缀相同。

接下来是状态转移。

对于f[level][last][flag]，在这里先要确定level这一位可以填充的数的取值范围。

对于flag最高位为1，也就是当前还是前导0状态时，可以无视相邻数字间差值为1的规定，那么候选集就是0到9的所有数字，反之，可用的数字就只能是last - 1或者last + 1。在这里需要特别判断last为0或者9的情况，这两种情况下只有一种可行的取值。

另一方面，对于flag中的其他两位，若中间这一位为1，那么说明之前填充的数字与high的前缀相同，那么当前填充的数值上界top就不能超过high[level]，反之则可以将top设置为9。同理，若flag的最低位为1，那么当前填充的数值下界bottom就不能小于low[level]，反之则可以将bottom设置为0。

得到候选集以及上下界之后，只需逐个枚举接下来要填充的数digit，然后判断digit是否处于bottom和top之间，若满足条件，那么说明level这一位可以填充digit，此时则需要通过digit的取值以及当前flag的情况，计算出下一位对应的flag。具体来说，若digit与bottom相同，且flag最低位为1，那么下一位的new_flag对应的最低位也为1，表示填充了digit后当前数字与low的前缀相同。同样的道理，若digit与top相同，且flag中间这一位为1，那么new_flag的中间这一位也为1，表示填充了digit后当前数字与high的前缀相同。最后，若flag最高位为1，且digit为0，那么当前依然在延续之前的前导0状态，此时则需要将new_flag的最高位也设置为1。

得到new_flag后，只需通过记忆化搜索递归求解f[level + 1][digit][new_flag]，然后将这个值累加到f[level][last][flag]中就行了。

另外，即使在没有前导0的情况下数字的最高位也是不受差1条件约束的，因此可以从low[0]到high[0]枚举这个最高位first，并通过first与low[0]、high[0]以及0的关系来计算最初始的flag，然后通过记忆化搜索求解f[1][first][flag]，并将其累加到答案中。

最后附上python代码：

```python
class Solution(object):
    def countSteppingNumbers(self, low, high):
        """
        :type low: str
        :type high: str
        :rtype: int
        """

        mod = 10 ** 9 + 7

        max_level = len(high)
        low = '0' * (max_level - len(low)) + low

        f = [[[None] * 8 for j in range(10)] for i in range(max_level)]
        res = 0

        def dfs(level, last, flag):
            if level == max_level:
                return 1
            
            if f[level][last][flag] is None:
                f[level][last][flag] = 0
                if flag & 4 == 4:
                    candidate = range(10)
                else:
                    candidate = []
                    if last > 0:
                        candidate.append(last - 1)
                    if last < 9:
                        candidate.append(last + 1)

                if flag & 1 == 1:
                    bottom = int(low[level])
                else:
                    bottom = 0
                    
                if flag & 2 == 2:
                    top = int(high[level])
                else:
                    top = 9

                for digit in candidate:
                    if digit < bottom or digit > top:
                        continue
                    new_flag = 0
                    if digit == bottom and (flag & 1 == 1):
                        new_flag |= 1
                    if digit == top and (flag & 2 == 2):
                        new_flag |= 2
                    if digit == 0 and (flag & 4 == 4):
                        new_flag |= 4
                    
                    f[level][last][flag] += dfs(level + 1, digit, new_flag)
                    if f[level][last][flag] >= mod:
                        f[level][last][flag] -= mod
            
            return f[level][last][flag]

        for first in range(int(low[0]), int(high[0]) + 1):
            flag = 0
            if first == int(low[0]):
                flag |= 1
            if first == int(high[0]):
                flag |= 2
            if first == 0:
                flag |= 4

            res += dfs(1, first, flag)
            if res >= mod:
                res -= mod
        
        return res
```
