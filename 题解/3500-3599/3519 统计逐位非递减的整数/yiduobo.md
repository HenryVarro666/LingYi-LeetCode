---
title: "3519. 统计逐位非递减的整数"
aliases: ["yiduobo的每日leetcode 3519.统计逐位非递减的整数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "leetcode/combinatorics", "题单/动态规划", "题单/数学算法", "题单/动态规划/十-数位-DP", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1902550722165347134"
zhihu_id: "1902550722165347134"
zhihu_title: "yiduobo的每日leetcode 3519.统计逐位非递减的整数"
question_id: "3519"
question: "统计逐位非递减的整数"
problem_url: "https://leetcode.cn/problems/count-numbers-with-non-decreasing-digits/"
difficulty: "Hard"
rating: 2246
created: "2025-05-08T21:47:58+08:00"
updated: "2025-05-08T21:47:58+08:00"
upvotes: 1
comments: 0
---

# 3519. 统计逐位非递减的整数

> **[yiduobo的每日leetcode 3519.统计逐位非递减的整数](https://zhuanlan.zhihu.com/p/1902550722165347134) · 知乎 · 2025-05-08 · 赞同 1**
> 力扣：[3519. 统计逐位非递减的整数](https://leetcode.cn/problems/count-numbers-with-non-decreasing-digits/) · Hard · 灵茶山艾府：[两种方法：上下界数位 DP / 组合数学（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3519.统计逐位非递减的整数

[3519. 统计逐位非递减的整数 - 力扣（LeetCode）](https://leetcode.cn/problems/count-numbers-with-non-decreasing-digits/description/)

题目给出两个以字符串形式表示的整数l和r，以及一个整数b，其中l和r的长度不超过100，b的取值范围则在2到10之间。现在要求返回大小在[l, r]之间，且b进制表示时每一位数字都是非递减的整数个数。

标准的数位动态规划问题，不过在计算之前，需要先将l和r都转化为b进制，然后再执行数位动态规划。

对于进制转换的问题，在这里可以直接沿用经典的模b除b的做法，倒序记录每一轮的余数得到转换后的结果。

虽然看上去好像涉及到了高精度除法，不过本题中b的取值范围在2到10之间，因此在具体实现时只需从高位开始向前逐位遍历转换数组s_list，对于当前遍历到的位index，先将s_list[index]对base取模的结果乘以10累加到s_list[index - 1]中，然后将s_list[index]除以base就行了。遍历结束后，将最低位s_list[0]对base取模的结果添加到转换结果的数组res中，然后再将s_list[0]除以base。

执行完一轮后，注意清理掉s_list中高位的前导0。

重复此过程直到s_list为空为止，此时将结果数组res翻转即为进制转换的结果。

完成进制转换后，需要先给l填充足够的前导0，让l的数位与r相同，接下来就可以执行数位动态规划了。

令f[level][last][flag]表示填充到第level位，最后一次填充的数位值为last，且已经填充的前缀与l和r的前缀大小关系为flag时合法的填充方案数。其中flag时一个两位的二进制数，低位表示已经填充的前缀与l的前缀是否相同，高位则表示已经填充的前缀与r的前缀是否相同。那么对于f[level][last][flag]：

1、若level等于n，那么说明当前填充方案合法，此时f[level][last][flag] \= 1

2、若level \< n，则尝试填充当前的数位。

对于当前数位，其可以填充元素的下界start初始情况下应该等于last。另一方面，若flag的低位为1，那么start还必须大于等于l[level]。同样的，对于可填充元素的上界end，初始情况下应该等于b - 1。若flag的高位为1，那么end还必须小于等于r[level]。

接下来从start到end遍历填充的数值digit。

若digit等于l[level]，那么nxt_flag的低位为1，否则为0；若digit等于r[level]，那么nxt_flag的高位为1，否则为0。得到nxt_flag后，就可以递归求解f[level + 1][digit][nxt_flag]，然后将其累积到f[level][last][flag]中。

全部计算完成后，f[0][0][3]即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def countNumbers(self, l, r, b):
        """
        :type l: str
        :type r: str
        :type b: int
        :rtype: int
        """
        
        def trans_base(s, base):
            s_list = []
            for char in s:
                s_list.append(int(char))
            
            s_list.reverse()
            res = []
            while s_list:
                for index in range(len(s_list) - 1, 0, -1):
                    s_list[index - 1] += s_list[index] % base * 10
                    s_list[index] //= base
                
                res.append(s_list[0] % base)
                s_list[0] //= base

                while s_list and s_list[-1] == 0:
                    s_list.pop()

            return res[::-1]

        l_base_b = trans_base(l, b)
        r_base_b = trans_base(r, b)

        n = len(r_base_b)
        l_base_b = [0] * (n - len(l_base_b)) + l_base_b

        f = [[[None] * 4 for _ in range(b)] for _ in range(n)]
        mod = 10 ** 9 + 7
        def dfs(level, last, flag, f):
            if level == n:
                return 1
            
            if f[level][last][flag] is None:
                f[level][last][flag] = 0

                start = last
                if flag & 1:
                    start = max(last, l_base_b[level])
                
                end = b - 1
                if flag & 2:
                    end = min(end, r_base_b[level])
                
                for digit in range(start, end + 1):
                    nxt_flag = 0
                    if (flag & 1) and digit == l_base_b[level]:
                        nxt_flag |= 1
                    if (flag & 2) and digit == r_base_b[level]:
                        nxt_flag |= 2
                    f[level][last][flag] += dfs(level + 1, digit, nxt_flag, f)
                    if f[level][last][flag] >= mod:
                        f[level][last][flag] -= mod
            
            return f[level][last][flag]
        
        return dfs(0, 0, 3, f)
```
