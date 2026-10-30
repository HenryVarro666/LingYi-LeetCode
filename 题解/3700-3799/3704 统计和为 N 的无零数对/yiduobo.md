---
title: "3704. 统计和为N的无零数对"
aliases: ["yiduobo的每日leetcode 3704.统计和为N的无零数对"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/combinatorics", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1958263810595984653"
zhihu_id: "1958263810595984653"
zhihu_title: "yiduobo的每日leetcode 3704.统计和为N的无零数对"
question_id: "3704"
question: "统计和为 N 的无零数对"
problem_url: "https://leetcode.cn/problems/count-no-zero-pairs-that-sum-to-n/"
difficulty: "Hard"
rating: 2419
created: "2025-10-07T14:46:11+08:00"
updated: "2025-10-07T14:46:15+08:00"
upvotes: 0
comments: 0
---

# 3704. 统计和为N的无零数对

> **[yiduobo的每日leetcode 3704.统计和为N的无零数对](https://zhuanlan.zhihu.com/p/1958263810595984653) · 知乎 · 2025-10-07 · 赞同 0**
> 力扣：[3704. 统计和为 N 的无零数对](https://leetcode.cn/problems/count-no-zero-pairs-that-sum-to-n/) · Hard · 灵茶山艾府：[从低到高的数位 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3704.统计和为N的无零数对

[3704. 统计和为 N 的无零数对 - 力扣（LeetCode）](https://leetcode.cn/problems/count-no-zero-pairs-that-sum-to-n/description/)

一个无零整数指的是一个十进制表示中不包含数字0的正整数。

给出一个n，其中n的取值范围在2到10^15，要求将n拆分为两个无零整数之和，问有多少种可行的拆分方式。

题目的数据规模很大，直接暴力计算显然是不行的，也没有想到什么好的数学方法，不过本题中需要处理的是加法，而加法的进位最多只会进一，因此在这里只需保留进位的信息，就可以采取逐位填充的数位动态规划来进行处理。

与常规的实现不同，因为有进位的存在，因此本题应该从低位开始向高位进行填充，那么大致的过程就是从低到高填充a的数位，然后通过已经填充的数位，计算b对应的数位，同时检测其中是否存在0。因为变成了做减法，因此在语义上这里记录的应该是借位的信息而不是进位的信息，不过本质上是一样的。

由于a和b的数位可能比n要短，也就是说在填充时可能会出现前导0，因此也需要将前导0的状态也编码进来，那么最终得到的状态表示就是f[index][state]表示接下来填充第index位，而已经填充的数位中的状态为state时的合法填充方案。其中state是一个3为二进制，从低到高位分别表示当前位是否被低位借位过、a是否进入了前导0的模式、b是否进入了前导0的模式。需要注意，一旦a或者b进入了前导0的模式，接下来的位就只能继续填充0，否则就与无零整数的矛盾了。

另外由于本题是枚举a然后检测对应的b是否合法，因此相比通过f[index - 1]来更新f[index]，在这里使用f[index]来更新f[index + 1]是更合适的。

接下来考虑具体的动态规划应该怎么做。

初始状态下有f[0][0]为1，其他的f[0][1]到f[0][7]为0，其中f[0][0]表示一开始既没有借位，也没有前导0。

接下来将n的数位分离出来，得到数位数组digits，然后从低到高遍历每一位以及每种对应的状态，对于当前遍历到的f[index][state]，可以将state分离出来，得到对应的borrow、a_zero以及b_zero，分别表示是否出现了借位、a是否进入了前导0模式、b是否进入了前导0模式。记r为digits[index]，若borrow为true，则将r减去1。接下来考虑当前位上a应该如何填充：

1、首先是填充0的情况：

只要index大于0，a总是可以填充0，相对应的需要先将nxt_state置为2。另外，由于a填充的为0，因此b在对应位置就应该为r。

需要注意的是，若此时b已经进入了前导0的模式，且r不为0，此时的填充方案就不合法。反之，则需要根据r的具体情况调整nxt_state：若r小于0，则需要借位，此时需要将1按位或到nxt_state中；若r等于0，则说明b接下来进入了前导0模式，需要将4按位或到nxt_state中。

最后，将f[index][state]累加到f[index + 1][nxt_state]中。

2、接下来考虑填充非0的情况：

此时的a_zero必须false，否则a就不是无零整数了。相对应的，可以先将nxt_state置为0。

接下来需要根据r的具体值来判断状态转移应该如何进行。

2-1）当r \<\= 0时：

由于a填充的数在1到9之间，因此必然会产生借位，需要将1按位或到nxt_state中。

若此时b已经进入了前导0的模式，那么只有当r等于-1，且a填充的数为9时，才能使得b在对应的位置上为0，此时就应该将f[index][state]累加到f[index + 1][nxt_state | 4]中。

若此时b还没有进入前导0的模式，那么当a填充的在1到8之间时，b对应的位置上都不为0，因此可以现将f[index][state] \* 8累加到f[index + 1][nxt_state]中。而对于a填充9的情况，与上面相同，若r等于-1，那么b对应位上为0，也就是说进入了前导0的模式，此时应该将f[index][state]累加到f[index + 1][nxt_state | 4]中，反之则应该将f[index][state]累加到f[index + 1][nxt_state]中。

2-2）当r > 0时：

若此时b已经进入了前导0的模式，那么a只能填充r才能使得b在对应的位置上为0，因此同样是将f[index][state]累加到f[index + 1][nxt_state | 4]中。

若此时b还没有进入前导0的模式，那么a的取值可以分为三段，分别为1到r - 1、r、r + 1到9：

当填充1到r - 1这一段时，b在对应位置上大于0，一共是r - 1种情况，因此需要将f[index][state] \* (r - 1)累加到f[index][state]中。

当填充r时，b进入了前导0模式，因此需要将f[index][state]累加到f[index + 1][state | 4]中。

当填充r + 1到9这一段时，会产生借位，同时b在对应位置上大于0，一共是9 - r种情况，因此需要将f[index][state] \* (9 - r)累加到f[index][state | 1]中。

全部计算完成后，最终f中没有出现借位的状态，也就是f[-1][0]、f[-1][2]、f[-1][4]以及f[-1][6]之和即为最终的合法方案数。

另外，由于f每一轮状态只与上一轮有关，因此可以使用滚动数组优化掉index这一维。

最后附上python代码：

```python
class Solution(object):
    def countNoZeroPairs(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        digits = []
        tmp = n
        while tmp:
            digits.append(tmp % 10)
            tmp //= 10

        length = len(digits)
        f = [0] * 8
        f[0] = 1

        for index in range(length):
            g = f[:]
            f = [0] * 8
            for state in range(8):
                if state & 1:
                    borrow = True
                else:
                    borrow = False

                if state & 2:
                    a_zero = True
                else:
                    a_zero = False
                
                if state & 4:
                    b_zero = True
                else:
                    b_zero = False

                r = digits[index]
                if borrow:
                    r -= 1

                if index > 0:
                    nxt_state = 2
                    
                    if not b_zero or r == 0:
                        if r < 0:
                            nxt_state |= 1
                        elif r == 0:
                            nxt_state |= 4
                    
                        f[nxt_state] += g[state]

                if not a_zero:
                    nxt_state = 0
                    if r <= 0:
                        nxt_state |= 1
                        if b_zero:
                            if r == -1:
                                f[nxt_state | 4] += g[state]
                        else:
                            f[nxt_state] += g[state] * 8
                            if r == 0:
                                f[nxt_state] += g[state]
                            else:
                                f[nxt_state | 4] += g[state]
                
                    else:
                        if b_zero:
                            f[nxt_state | 4] += g[state]
                        else:
                            f[nxt_state] += g[state] * (r - 1)
                            if index > 0:
                                f[nxt_state | 4] += g[state]
                            f[nxt_state | 1] += g[state] * (9 - r)
        
        return f[0] + f[2] + f[4] + f[6]
```
