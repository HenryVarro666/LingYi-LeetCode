---
title: "1866. 恰有K根木棍可以看到的排列数目"
aliases: ["yiduobo的每日leetcode 1866.恰有K根木棍可以看到的排列数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/combinatorics", "题单/动态规划", "题单/数学算法", "题单/动态规划/七-其他线性-DP", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/474428171"
zhihu_id: "474428171"
zhihu_title: "yiduobo的每日leetcode 1866.恰有K根木棍可以看到的排列数目"
question_id: "1866"
question: "恰有 K 根木棍可以看到的排列数目"
problem_url: "https://leetcode.cn/problems/number-of-ways-to-rearrange-sticks-with-k-sticks-visible/"
difficulty: "Hard"
rating: 2333
created: "2022-03-02T01:05:01+08:00"
updated: "2022-03-02T01:05:01+08:00"
upvotes: 0
comments: 0
---

# 1866. 恰有K根木棍可以看到的排列数目

> **[yiduobo的每日leetcode 1866.恰有K根木棍可以看到的排列数目](https://zhuanlan.zhihu.com/p/474428171) · 知乎 · 2022-03-02 · 赞同 0**
> 力扣：[1866. 恰有 K 根木棍可以看到的排列数目](https://leetcode.cn/problems/number-of-ways-to-rearrange-sticks-with-k-sticks-visible/) · Hard · 灵茶山艾府：[可以转换成第一类斯特林数的理由](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1866.恰有K个木棍可以看到的排列数目

[力扣](https://leetcode-cn.com/problems/number-of-ways-to-rearrange-sticks-with-k-sticks-visible/)

找规律的题目。对于这类问题，一般是从边界入手。在这里就是从最短或者最长的那根木棍入手，想办法从n根木棍的情况推出n + 1根木棍的情况。

我在这里考虑是最短的木棍，相比考虑最长的木棍要简单明了得多。

先从n较小的情况入手。不妨设当前木棍长度为2、3、4，此时3根木棍6种排列，一共可以形成

2 3 1

这种形式的答案分布，即只能看到一根木棍的情况有2种，可以看到两根木棍的情况有3种，可以看到全部三根木棍的情况有1种。

接下来考虑新加入一根长度为1的木棍。加入之后答案应该扩展到长度为4的数组，分别表示可以看到一根到四根木棍的情况种数。

对于之前由2、3、4构成的的任意排列，则一共有4个位置可以插入这个新来的木棍。

当这个木棍插入到排列的最前方时，就相当于在之前三根木棍排列的基础上可以额外多看到一根木棍，因此在这里相当于将之前答案的2、3、1向右移动了一位，即当1放在最前面时，有2种情况可以看到两根木棍，有3种情况可以看到三根木棍，有4中情况可以看到四根木棍，即

0 2 3 1

接下来，如果这里新来的1插入到排列除开头之外的其他任何位置，这个1都不可能被看到，因此在这里可以认为保持之前2、3、4排列可以看到的木棍数量不变。由于这里新来的1除了排列开头之外还有3处可以插入的地方，因此需要将之前的2、3、1原地复制3份，即

6 9 3

最后，将上面这些累加起来，即

0 2 3 1

6 9 3

得到

6 11 6 1

就是1、2、3、4这四根木棍的排列可以看到木棍数的分布。

推广到一般的情况，令f[i]表示i根木棍的所有排列可以看到木棍数的分布，那么在计算f[i + 1]时，先将f[i]复制后向前移动一位，接下来将f[i]原地复制i份，最后将这二者相加即为f[i + 1]。

具体实现时，由于移动整个数组是不太方便的，因此可以反过来思考，令数组的第0位表示答案的最高位，例如对于上面的例子，使用[1, 3, 2]来保存答案。接下来在计算时，在数组尾部添加一个0，就可以认为前面的[1, 3, 2]已经向前移动了。此时的数组为[1, 3, 2, 0]，然后在这个基础上加上之前[1, 3, 2]的三份复制[3, 9, 6]，最终就可以得到[1, 6, 11, 6]了。

另外，需要特别注意的是，由于是倒过来计算，因此在最终输出时答案对应的位置应该是f[n - k]。

最后附上python代码：

```python
class Solution(object):
    def rearrangeSticks(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """

        f = [1]
        mod = 10 ** 9 + 7
        for l in range(1, n):
            f.append(0)
            for index in range(l, 0, -1):
                f[index] += f[index - 1] * l
                f[index] %= mod
            
        return f[n - k]
```
