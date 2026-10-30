---
title: "2484. 统计回文子序列数目"
aliases: ["yiduobo的每日leetcode 2484.统计回文子序列数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/动态规划", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/589499849"
zhihu_id: "589499849"
zhihu_title: "yiduobo的每日leetcode 2484.统计回文子序列数目"
question_id: "2484"
question: "统计回文子序列数目"
problem_url: "https://leetcode.cn/problems/count-palindromic-subsequences/"
difficulty: "Hard"
rating: 2223
created: "2022-12-06T01:30:19+08:00"
updated: "2022-12-06T01:30:19+08:00"
upvotes: 0
comments: 0
---

# 2484. 统计回文子序列数目

> **[yiduobo的每日leetcode 2484.统计回文子序列数目](https://zhuanlan.zhihu.com/p/589499849) · 知乎 · 2022-12-06 · 赞同 0**
> 力扣：[2484. 统计回文子序列数目](https://leetcode.cn/problems/count-palindromic-subsequences/) · Hard · 灵茶山艾府：[前后缀分解 + O(100) 常数空间（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2484.统计回文子序列数目

[力扣](https://leetcode.cn/problems/count-palindromic-subsequences/)

题目要求找出字符串中所有长度为5的回文子序列，对于这种寻找定长的有规律的子串或者子序列的问题，还是按照老办法，枚举中心位置，然后计算前缀和后缀中满足某种条件的子串或者子序列的数目。

对于本题，则是枚举回文子序列的中心位置p，那么问题就被拆解成了前缀中能形成每种两位数的子序列数目，以及后缀中反向能形成每种两位数的子序列数目。对于这个问题，则可以通过动态规划求解。

由于左侧和右侧子序列的求解仅有方向不同，其他的处理方式都是一样的，因此在这里只需要考虑一侧的做法，然后另一侧反过来遍历并照搬已有的做法就行了。

令left_two[i][j]表示前i个字符能形成数值为j的长度为2的子序列的数目。为了求解left_two，需要一个辅助数组left_one，其中left_one[i][j]表示前i个字符能形成数值为j的长度为1的子序列的数目。对于left_one[i][j]和left_two[i][j]：

1、可以考虑不使用第i个字符，因此就可以枚举所有合法的j，初始化

left_one[i][j] \= left_one[i - 1][j]

left_two[i][j] \= left_two[i - 1][j]

需要注意的是，对于left_one而言，合法的j取值范围是0到9，而对于left_two而言，则是0到99

2、如果考虑使用第i个字符，那么就有

left_one\[i\]\[s\[i - 1\]\] +\= 1

同时需要从0到9枚举left_two的高位high_digit，那么就有

left_two\[i\]\[high_digit \* 10 + s\[i - 1\]\] +\= left_one\[i - 1\]\[high_digit\]

表示由high_digit于s[i - 1]组成了长度为2的子序列

在这里可以简单的滚动掉left_one的i这一维，但是由于left_two的i这一维在后续枚举p的时候需要用到，因此不能省去。

计算得到left_two以及反过来计算得到与left_two定义相似的right_two之后，只需枚举中心位置p，然后从0到99枚举j，使用left_two[p - 1][j] \* right_two[p + 1][j]来更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def countPalindromes(self, s):
        """
        :type s: str
        :rtype: int
        """

        n = len(s)
        mod = 10 ** 9 + 7

        left_one = [0] * 10
        left_two = [[0] * 100 for _ in range(n)]

        right_one = [0] * 10
        right_two = [[0] * 100 for _ in range(n)]

        
        for index in range(n):
            digit = int(s[index])
            if index > 0:
                left_two[index] = left_two[index - 1][:]
            for high_digit in range(10):
                num = high_digit * 10 + digit
                left_two[index][num] += left_one[high_digit]

            left_one[digit] += 1
        
        for index in range(n - 1, -1, -1):
            digit = int(s[index])
            if index < n - 1:
                right_two[index] = right_two[index + 1][:]
            for high_digit in range(10):
                num = high_digit * 10 + digit
                right_two[index][num] += right_one[high_digit]
            right_one[digit] += 1

        res = 0
        for mid_pos in range(2, n - 2):
            for num in range(100):
                res += left_two[mid_pos - 1][num] * right_two[mid_pos + 1][num]
                res %= mod
        
        return res
```
