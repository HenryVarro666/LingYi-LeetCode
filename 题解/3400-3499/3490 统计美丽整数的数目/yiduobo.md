---
title: "3490. 统计美丽整数的数目"
aliases: ["yiduobo的每日leetcode 3490.统计美丽整数的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1899222448995567219"
zhihu_id: "1899222448995567219"
zhihu_title: "yiduobo的每日leetcode 3490.统计美丽整数的数目"
question_id: "3490"
question: "统计美丽整数的数目"
problem_url: "https://leetcode.cn/problems/count-beautiful-numbers/"
difficulty: "Hard"
rating: 2502
created: "2025-04-25T22:50:14+08:00"
updated: "2025-04-25T22:50:14+08:00"
upvotes: 0
comments: 0
---

# 3490. 统计美丽整数的数目

> **[yiduobo的每日leetcode 3490.统计美丽整数的数目](https://zhuanlan.zhihu.com/p/1899222448995567219) · 知乎 · 2025-04-25 · 赞同 0**
> 力扣：[3490. 统计美丽整数的数目](https://leetcode.cn/problems/count-beautiful-numbers/) · Hard · 灵茶山艾府：[【模板】数位 DP v2.1（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3490.统计美丽整数的数目

[3490. 统计美丽整数的数目 - 力扣（LeetCode）](https://leetcode.cn/problems/count-beautiful-numbers/description/)

题目定义美丽整数为每一位上数字的乘积可以被这些数字之和整除的正整除，接下来给出两个正整数l和r，要求找出l和r之间美丽整数的数目，其中l和r的大小都小于10^9。

非常标准的数位动态规划问题，不过本题中涉及到数位之和取模，但是数位之和可能随着数位的填充不断变化，在这个过程中无法通过上一轮的余数计算出新的余数。注意到本题中l和r都小于10^9，也就是说最多只有8为，那么这些数位之和就只能在1到72之间，因此在这里可以枚举最后的数位和mod，接下来对于当前的mod，就可以使用f[level][s][rest][flag]表示填充了前level位，这些位上之和为s，乘积对mod取模的结果为rest，且这些位上与l和r前level位的大小关系表示为flag时，最终可以填充得到的美丽整数数目。

关于状态表示中的level、s、rest，都是比较好理解的，flag则是一个3为的2进制数，其中最高位表示当前填充的数位是否还是前导0，中间这一位表示当前填充的数位是否与left的前缀相同，最低位则表示当前填充的数位是否与right的前缀相同。

在这里记录前导0的作用是计算rest时不应该将前导0中的0乘进来，而记录是否与left或者right前缀相同的作用则是限制下一位填充数值的区间。简单来说，若前level位填充的值与left前level位相同，那么在填充第level + 1位时，其数值就必须大于等于left的第level + 1位；反之，若不相同，那么可填充数值的下界就不受left的影响。同样的，前level位填充的值是否与right的前level位相同则决定了可填充数值的上界是否受right的影响。

不妨设可填充数值的下界和上界分别为start和end，那么就可以从中枚举当前位填充的数值v，接下来就可以通过s + v计算nxt_s，同时若flag最高位不为1，就可以通过rest \* v % mod计算nxt_rest。除此之外：

若flag最高位为1，且v等于0，那么nxt_flag的最高位也为1，否则为0。

若flag中间这一位为1，且v等于left[level]，那么nxt_flag中间这一位也为1，否则为0。

若flag最低位为1，且v等于right[level]，那么nxt_flag最低位也为1，否则为0。

接下来，将f[level + 1][nxt_s][nxt_rest][nxt_flag]累加到f[level][s][rest][flag]中即可。

---

在具体实现上，使用记忆化搜索比较方便。另外按上面的处理方法实现出来之后，发现在时间复杂度方面比较吃紧。在加入了可行性剪枝后，发现依然不行，所以在这里我还采用了另一个优化。

由于题目中定义的美丽整数需要数位之积可以被数位之和整除，那么当数位中存在非前导的0时，无论其他数位如何填充都可以形成美丽整数；反之若数位中不存在非前导的0时，其数位之积的质因子只可能是2、3、5、7，因为数位之积是通过1到9的整数相乘得到的。因此在枚举mod时，可以先对mod分解质因数，若其中包含除2、3、5、7之外的质因子，就不需要计算不存在非前导的0这种情况了。

当然，这样分情况处理的话就需要针对存在0和不存在0的情况分别进行计算。其中存在0的部分不需要额外记录rest，但是需要在flag中再添加一位，表示当前是否已经有了非前导的0，而对于不存在0的部分则还是按照最开始的做法进行处理。

最后附上python代码：

```python
class Solution(object):
    def beautifulNumbers(self, l, r):
        """
        :type l: int
        :type r: int
        :rtype: int
        """
        
        left = [int(x) for x in str(l)]
        right = [int(x) for x in str(r)]
        left = [0] * (len(right) - len(left)) + left

        n = len(right)

        def calc_with_zero(level, s, flag, f):
            if f[level][s][flag] is None:
                f[level][s][flag] = 0
                if level == n:
                    if flag & 8:
                        f[level][s][flag] = 1
                    return f[level][s][flag]
                
                start, end = 0, 9
                if flag & 2:
                    start = left[level]
                
                if flag & 1:
                    end = right[level]

                for v in range(start, end + 1):
                    nxt_s = s + v

                    if nxt_s + (n - level - 1) * 9 < mod:
                        continue

                    if nxt_s > mod:
                        break
                    
                    nxt_flag = (flag & 8)
                    if v == 0:
                        if flag & 4:
                            nxt_flag |= 4
                        else:
                            nxt_flag |= 8
                    
                    if v == left[level]:
                        nxt_flag |= (flag & 2)
                    
                    if v == right[level]:
                        nxt_flag |= (flag & 1)

                    f[level][s][flag] += calc_with_zero(level + 1, nxt_s, nxt_flag, f)
            
            return f[level][s][flag]

        def calc_without_zero(level, s, rest, flag, f):
            if f[level][s][rest][flag] is None:
                f[level][s][rest][flag] = 0
                if level == n:
                    if rest == 0 and s == mod:
                        f[level][s][rest][flag] = 1
                    return f[level][s][rest][flag]
                
                start, end = 1, 9
                if flag & 4:
                    start = 0

                if flag & 2:
                    start = max(start, left[level])
                
                if flag & 1:
                    end = right[level]

                for v in range(start, end + 1):
                    nxt_s = s + v

                    if nxt_s + (n - level - 1) * 9 < mod:
                        continue

                    if nxt_s > mod:
                        break

                    nxt_flag = 0
                    if flag & 4:
                        if v == 0:
                            nxt_flag |= 4
                            nxt_rest = 0
                        else:
                            nxt_rest = v % mod
                    else:
                        nxt_rest = rest * v % mod
                    
                    if v == left[level]:
                        nxt_flag |= (flag & 2)
                    
                    if v == right[level]:
                        nxt_flag |= (flag & 1)

                    f[level][s][rest][flag] += calc_without_zero(level + 1, nxt_s, nxt_rest, nxt_flag, f)
            
            return f[level][s][rest][flag]

        res = 0
        for mod in range(1, 9 * n + 1):
            tmp = mod
            for v in [2, 3, 5, 7]:
                while tmp % v == 0:
                    tmp //= v
            
            if tmp == 1:
                f = [[[[None] * 8 for _ in range(mod)] for _ in range(mod + 1)] for _ in range(n + 1)]
                res += calc_without_zero(0, 0, 0, 7, f)

            f = [[[None] * 16 for _ in range(mod + 1)] for _ in range(n + 1)]
            res += calc_with_zero(0, 0, 7, f)
        
        return res
```
