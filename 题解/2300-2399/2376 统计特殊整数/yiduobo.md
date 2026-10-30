---
title: "2376. 统计特殊整数"
aliases: ["yiduobo的每日leetcode 2376.统计特殊整数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/564126997"
zhihu_id: "564126997"
zhihu_title: "yiduobo的每日leetcode 2376.统计特殊整数"
question_id: "2376"
question: "统计特殊整数"
problem_url: "https://leetcode.cn/problems/count-special-integers/"
difficulty: "Hard"
rating: 2120
created: "2022-09-14T02:27:50+08:00"
updated: "2022-09-14T02:27:50+08:00"
upvotes: 1
comments: 0
---

# 2376. 统计特殊整数

> **[yiduobo的每日leetcode 2376.统计特殊整数](https://zhuanlan.zhihu.com/p/564126997) · 知乎 · 2022-09-14 · 赞同 1**
> 力扣：[2376. 统计特殊整数](https://leetcode.cn/problems/count-special-integers/) · Hard · 灵茶山艾府：[数位 DP 通用模板（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2376.统计特殊整数

[力扣](https://leetcode.cn/problems/count-special-integers/)

对于这类问题，王道做法通常是数位动态规划。简单来说，就是令f[i][j][k][state]表示前i位能构造出的合法整数数目。状态表示中的j和k分别表示第i为数字的上下限，而state则表示上下限触碰情况以及其他数字的规则情况。

对于本题，则可以基于简单的组合数学，用简单点的做法来做。

首先可以参考本题的青春版357题：

[yiduobo：yiduobo的每日leetcode 357.计算各个位数不同的数字个数](https://zhuanlan.zhihu.com/p/164636818)

在这里不妨设f[i]表示i位整数中有多少特殊整数，那么就可以先使用357题中的做法一趟遍历计算出所有的f。

令l表示n的位数，那么所有的位数不足l位的特殊整数一共就有f[1] + f[2] + ... + f[l - 1]个，可以先用这个和来初始化答案。

接下来考虑l位的特殊整数，从n的最高位开始逐位向后考虑。

首先是最高位，不妨设为num[0]：

1、先考虑最高位为1、2、...、num[0] - 1的l位整数

这些数都是小于n的，而以1、2、...、num[0] - 1开头的l为的特殊整数的数量都是f[l] / 9，理由是基于特殊整数的定义来看，最高位无论是1到9中的哪个数都是等价的。

因此在这里应该将(num[0] - 1) \* (f[l] / 9)累加到答案中

2、接下来是以num[0]开头的l位整数

对于这个问题，就可以转化成所有l - 1位，且小于等于n去除最高位后的整数中，有多少个特殊整数。不过需要注意的是，这里的特殊整数的最高位可以为0，因此这里是基于f[l] / 9来进行计算，而不是f[l - 1]来进行计算。

可以发现这跟原问题其实差不了多少，因此可以直接套用上面的步骤来继续求解。不过需要特别注意的是，对于后面的数位可以将0考虑进去，同时在前面位上用过的数字就不能再用了。另一方面，所有特殊整数的数目不是对应的f，而是从f[l]不断执行除法细分下来的。

另外，若当前的数位上限在前面出现过，那么就无需再向后考虑了。反之，如果考虑到最后一位都没有出现重复，则需要将答案再加上1。

以两个例子来说明。

首先是n \= 111，在考虑最高的两位后，已经计算过了所有以10开头的三位数中特殊整数的数目，此时没有必要再考虑以11开头的三位数了，因为11开头本身就不合法。

另一个例子是123，在考虑最高的两位后，计算过了以10、11开头的三位数。而考虑完三位之后，则只考虑了120，但是123自身并没有考虑进去，因此需要将最终答案再加上1。

最后附上python代码：

```python
class Solution(object):
    def countSpecialNumbers(self, n):
        """
        :type n: int
        :rtype: int
        """

        l = 0
        tmp = n
        num_list = []
        while tmp:
            num_list.append(tmp % 10)
            tmp /= 10
            l += 1
        
        num_list.reverse()

        f = [0, 9]
        for index in range(2, l + 1):
            f.append(f[-1] * (11 - index))
        
        res = 0
        for index in range(l):
            res += f[index]
        
        used = set()
        possible = f[l] / 9
        for index, now in enumerate(num_list):
            if index == 0:
                res += (now - 1) * possible
            else:
                for num in range(now):
                    if num not in used:
                        res += possible
            
            if now in used:
                break
            
            used.add(now)
            possible /= (10 - index - 1)
            if index == l - 1:
                res += 1
        
        return res
```
