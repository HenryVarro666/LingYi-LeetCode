---
title: "3677. 统计二进制回文数字的数目"
aliases: ["yiduobo的每日leetcode 3677.统计二进制回文数字的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/math", "题单/动态规划", "题单/数学算法", "题单/动态规划/十-数位-DP", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1952818906717721673"
zhihu_id: "1952818906717721673"
zhihu_title: "yiduobo的每日leetcode 3677.统计二进制回文数字的数目"
question_id: "3677"
question: "统计二进制回文数字的数目"
problem_url: "https://leetcode.cn/problems/count-binary-palindromic-numbers/"
difficulty: "Hard"
rating: 2223
created: "2025-09-22T21:49:53+08:00"
updated: "2025-09-22T21:49:55+08:00"
upvotes: 1
comments: 0
---

# 3677. 统计二进制回文数字的数目

> **[yiduobo的每日leetcode 3677.统计二进制回文数字的数目](https://zhuanlan.zhihu.com/p/1952818906717721673) · 知乎 · 2025-09-22 · 赞同 1**
> 力扣：[3677. 统计二进制回文数字的数目](https://leetcode.cn/problems/count-binary-palindromic-numbers/) · Hard · 灵茶山艾府：[从 O(log n) 到 O(1)（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3677.统计二进制回文数字的数目

<https://leetcode.cn/problems/count-binary-palindromic-numbers/>

若一个非负整数的二进制表示(不含前导零)是回文串，那么就称这个数为二进制回文数。题目给出一个非负整数n，问0到n之间二进制回文数的数目。n的取值范围在0到10^15之间。

题目需要判断的是二进制回文串，在这里就应该先将n转化为二进制表示，不妨记为digits。由于题目需要计算的是0到n之间的二进制回文数，那么所有二进制表示下长度小于digits的二进制回文数就都是符合题目要求的。令digits的长度为m，在这里就可以先计算出所有长度为0、1、2、...、m - 1的二进制回文数总量，然后再想办法计算长度为m且大小不超过n的二进制回文数数量。

首先对于长度为len的二进制回文数总量：

1、若len为1，一共有0或者1这两种

2、若len为2，则只有11这一种

3、若len为3，一共有101或者111这两种

4、若len为4，一共有1001或者1111这两种

5、当len >\= 5时，就可利直接利用之前的结论了。若len为奇数，那么其中心位置只能填0或者1；若len为偶数，那么其中心位置只能填00或者11。填充了中心位置之后，问题就转化为了计算长度为len - 1或者len - 2时二进制回文数的数量，在这里可以直接利用之前计算出来的结果，乘以2之后就得到了长度为len的二进制回文数的数量。

基于以上的结论，只需从5开始遍历到m - 1，计算出所有长度小于m的二进制回文数数量，并累加到答案中。

接下来，还需要计算小于等于n且长度恰好为m的二进制回文数数量。

对于这个问题，则需要使用数位动态规划。

令g[level][state]表示接下来需要填充第level位，且已经填充好的数位与digits的关系为state时的填充方案数。由于最终必须填充得到一个回文串，因此实际上前后同时往中间填充。由于本题不需要处理下界，也不需要处理前导零的情况，因此这里的state只需要表示填充的前缀是否达到了前缀大小的上限，也就是与digits的前level位完全相同，以及填充的后缀是否小于等于digits的后缀，可以用一个两位的二进制数来表示。

在所有的位都填充完毕后，只有前缀小于digits的前缀，或者前缀等于digits的前缀同时后缀小于等于digits的后缀的填充方案才是合法的。

那么对于g[level][state]，先从state中拆解出前缀状态left_bound以及后缀状态right_invalid，接下来考虑下一位填充什么。填充的下界自然为0，而上界则取决于left_bound，若left_bound为true，也就是之前填充的数位与digits相同，那么下一位的上界就是digits[level]，否则为1。

得到填充值的上下界之后，则只需要枚举具体填充的数值d，并根据d更新接下来的状态nxt_state就行了。

具体来说，若d与digits[level]相同，且left_bound为true，那么就将nxt_state中left_bound的位设置为1。

另一方面，level这一位在回文中对应的是m - 1 - level这一位，若d大于digits[m - 1 - level]，或者d与digits[m - 1 - level]相同，且right_invalid为true，那么就将nxt_state中right_invalid的位设置为1。需要特别注意的是，有一种特殊情况是level这一位就是回文中心，此时对于left_bound的处理不变，而right_invalid则只需要照搬之前的结果就行了，不需要重新计算。

得到nxt_state之后，递归计算g[level + 1][nxt_state]，然后将其累加到g[level][state]中即可。

除此之外，还需要特别注意一点。由于回文串的首位和末位必然都填充1，而首位必然是顶着digits[0]的，因此在这里还需要特别判断digits的最后一位是0还是1，才能决定初始状态下的state。

最后附上python代码：

```python
class Solution(object):
    def countBinaryPalindromes(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        if n == 0:
            return 1
        elif n == 1:
            return 2

        digits = []
        while n:
            digits.append(n % 2)
            n //= 2
        digits.reverse()
        m = len(digits)

        f = [0, 2, 1, 2, 2]   
        for length in range(5, m):
            if length % 2 == 1:
                f.append(f[length - 1] + f[length - 1])
            else:
                f.append(f[length - 1])
        
        def calc(level, state, g):
            if state & 2:
                left_bound = True
            else:
                left_bound = False
                
            if state & 1:
                right_invalid = True
            else:
                right_invalid = False
                
            if level * 2 >= m:
                if not left_bound or not right_invalid:
                    return 1
                return 0
            
            if g[level][state] is None:
                g[level][state] = 0

                start = 0
                if left_bound:
                    end = digits[level]
                else:
                    end = 1
                
                nxt_state = 0
                for d in range(start, end + 1):
                    if left_bound and d == digits[level]:
                        nxt_state |= 2
                    if m - 1 - level != level:
                        if digits[m - 1 - level] < d or (digits[m - 1 - level] == d and right_invalid):
                            nxt_state |= 1
                    elif right_invalid:
                        nxt_state |= 1

                    g[level][state] += calc(level + 1, nxt_state, g)
            
            return g[level][state]

        res = sum(f[:m])
        g = [[None] * 4 for _ in range((m + 1) // 2)]
        if digits[-1] == 0:
            res += calc(1, 3, g)
        else:
            res += calc(1, 2, g)
        
        return res
```
