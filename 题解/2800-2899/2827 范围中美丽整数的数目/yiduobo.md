---
title: "2827. 范围中美丽整数的数目"
aliases: ["yiduobo的每日leetcode 2827.范围中美丽整数的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/659086434"
zhihu_id: "659086434"
zhihu_title: "yiduobo的每日leetcode 2827.范围中美丽整数的数目"
question_id: "2827"
question: "范围中美丽整数的数目"
problem_url: "https://leetcode.cn/problems/number-of-beautiful-integers-in-the-range/"
difficulty: "Hard"
rating: 2324
created: "2023-09-30T00:03:44+08:00"
updated: "2023-09-30T00:03:44+08:00"
upvotes: 0
comments: 0
---

# 2827. 范围中美丽整数的数目

> **[yiduobo的每日leetcode 2827.范围中美丽整数的数目](https://zhuanlan.zhihu.com/p/659086434) · 知乎 · 2023-09-30 · 赞同 0**
> 力扣：[2827. 范围中美丽整数的数目](https://leetcode.cn/problems/number-of-beautiful-integers-in-the-range/) · Hard · 灵茶山艾府：[数位 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2827.范围中美丽整数的数目

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/number-of-beautiful-integers-in-the-range/description/)

又是标准的数位动态规划问题。对于本题需要使用状态f[level][diff][r][flag]来表示填充前level位数字，偶数位的数量与奇数位的数量之差为diff，当前已填充的数字对k取模的结果为r，且与上下界的关系以及当前数位是否还处于前导0的状态为flag时的可行方案数。

在这里还是先说明一下flag表达的含义。

flag是一个三位的二进制数，其中：

1、最低位取值为1时表示之前已填充的数字与low的前缀相同，这也就意味着当前位的取值不能再比low对应的位取值要小，否则无论之后怎么填充，得到的数字都一定比low要小，不符合题目要求

2、对于这个二进制数的中间这一位，取值为1时则表示之前已填充的数字与high的前缀相同，这也就意味着当前位的取值不能再比high对应的位取值要大

3、最高位为1时则表示当前还处于前导0的状态。在这里需要这个前导0状态的理由是low和high的长度不一定相同，为了方便起见，我在这里将low通过填充前导0的方式使其与high的长度相同，但是这样的话就可能得到某些具有前导0的答案。但是前导0在本题中既不应该参与奇偶位数的计算，也不应该参与对k取模的计算，因此在这里需要一个标记来区分当前是否依然处于前导0的情况

除此之外，还有两点需要注意。

首先是diff的取值范围应该在-max_level到max_level之间，这里的max_level表示的是high的长度，因此在状态表示中，需要一个大小为max_level的偏移值以防止数组下标为负，也就是说，当diff等于max_level时表示的是奇偶数位相等，而当diff等于0时表示的则是奇数位比偶数位多出max_level个。

另一点就是对k取模这里，由于实际上在第level位上填充的数值digit表示的是digit \* 10^(max_level - level)，因此取模运算需要带上后面10的幂次，因此在这里可以提前预处理出所有10的幂次对k取模的结果，在这里记为r_list，那么第level位上填充digit后将是的对k取模的结果加上r_list[level] \* digit % k。

---

明确了上面这几点之后，接下来是动态规划的转移过程。对于f[level][diff][r][flag]：

1、若当前的level等于max_level，说明此时已经完成了填充，若diff等于max_level，也就是奇偶数位的数量相同，且r等于0，也就是整个数对k取模的结果为0，那么f[level][diff][r][flag]就等于1，否则等于0。

2、若当前的level小于max_level，则还需要对level以及后续的数位进行填充。首先初始化f[level][diff][r][flag]为0，接下来从0到9枚举填充的数值digit：

2-1）检测digit与上下界的合法性

若flag的最低位为1，那么digit就不能小于low[level]；若flag的中间位为1，那么digit就不能大于high[level]。若这两个条件中有一个不满足，那么就跳过digit

2-2）判断是否依然处于前导0的状态

若flag的最高位为1，且digit等于0，那么接下来将依然处于前导0状态。这种情况下不会影响diff和r的取值，同时flag必然是恒定为5，也就是最高位和最低位为1，于是就有f[level][diff][r][flag] +\= f[level + 1][diff][r][5]

2-3）对于不处于前导0且通过2-1中检测的digit，此时就需要计算下一轮的new_diff、new_r以及new_flag

首先是new_diff。若digit为偶数，那么new_diff就等于diff加1，否则new_diff就等于diff减1。

接下来是new_r。当前位digit对余数的贡献为digit \* r_list[level] % k，那么只需将这个值累加到r中就行，也就是new_r \= (r + digit \* r_list[level]) % k。

最后是new_flag。new_flag的最高位必然为0，因为前导0的情况在2-2中处理过了。而对于中间这一位，只有当flag的中间这一位为1，且digit等于high[level]时才为1，否则为0。同样的，对于最低位，也需要flag的最低位为1，且digit等于low[level]时才为1，否则为0。

得到这三个值之后，就有f[level][diff][r][flag] +\= f[level + 1][new_diff][new_r][new_flag]

在具体实现上，倒推不是很好实现，因此我在这里采用的是记忆化搜索的做法，使用dfs(level, diff, r, flag)递归地计算f[level][diff][r][flag]的值，那么dfs(0, max_level, 0, 7)就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def numberOfBeautifulIntegers(self, low, high, k):
        """
        :type low: int
        :type high: int
        :type k: int
        :rtype: int
        """

        str_high = str(high)
        max_level = len(str_high)
        str_low = str(low)
        str_low = '0' * (max_level - len(str_low)) + str_low

        now = 1
        r_list = []
        for index in range(max_level):
            r_list.append(now)
            now = now * 10 % k
        r_list.reverse()

        f = [[[[None] * 8 for _ in range(k)] for _ in range(max_level * 2 + 1)] for _ in range(max_level)]

        def dfs(level, diff, r, flag):
            if level == max_level:
                if diff == max_level and r == 0:
                    return 1
                else:
                    return 0

            if f[level][diff][r][flag] is None:
                f[level][diff][r][flag] = 0
                
                for digit in range(10):
                    if (flag & 2 == 2) and digit > int(str_high[level]):
                        continue
                    if (flag & 1 == 1) and digit < int(str_low[level]):
                        continue
                    
                    if digit == 0 and (flag & 4 == 4):
                        f[level][diff][r][flag] += dfs(level + 1, diff, r, 5)
                    else:
                        new_flag = 0
                        if (flag & 2 == 2) and digit == int(str_high[level]):
                            new_flag |= 2
                        if (flag & 1 == 1) and digit == int(str_low[level]):
                            new_flag |= 1
                        
                        new_diff = diff
                        if digit % 2 == 0:
                            new_diff += 1
                        else:
                            new_diff -= 1
                        
                        new_r = (r + r_list[level] * digit) % k

                        f[level][diff][r][flag] += dfs(level + 1, new_diff, new_r, new_flag)
                    
            
            return f[level][diff][r][flag]
        

        return dfs(0, max_level, 0, 7)
```
