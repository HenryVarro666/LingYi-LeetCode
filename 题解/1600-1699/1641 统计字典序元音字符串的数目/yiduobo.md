---
title: "1641. 统计字典序元音字符串的数目"
aliases: ["yiduobo的每日leetcode 1641.统计字典序元音字符串的数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/439282992"
zhihu_id: "439282992"
zhihu_title: "yiduobo的每日leetcode 1641.统计字典序元音字符串的数目"
question_id: "1641"
question: "统计字典序元音字符串的数目"
problem_url: "https://leetcode.cn/problems/count-sorted-vowel-strings/"
created: "2021-11-30T00:03:55+08:00"
updated: "2021-11-30T00:03:55+08:00"
upvotes: 0
comments: 0
---

# 1641. 统计字典序元音字符串的数目

> **[yiduobo的每日leetcode 1641.统计字典序元音字符串的数目](https://zhuanlan.zhihu.com/p/439282992) · 知乎 · 2021-11-30 · 赞同 0**
> 力扣：[1641. 统计字典序元音字符串的数目](https://leetcode.cn/problems/count-sorted-vowel-strings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1641.统计字典序元音字符串的数目

[力扣](https://leetcode-cn.com/problems/count-sorted-vowel-strings/)

拿到题目最直观的想法自然是动态规划。令f[i][0]到f[i][4]分别表示长度为i，且最后一个字符为a、e、i、o、u的字符串总数，那么：

1、a的只能跟在a的后面，因此

f[i][0] \= f[i - 1][0]

2、e可以跟在a和e的后面，因此

f[i][1] \= f[i - 1][0] + f[i - 1][1] \= f[i][0] + f[i - 1][1]

3、i可以跟在a、e、i的后面，因此

f[i][2] \= f[i - 1][0] + f[i - 1][1] + f[i - 1][2] \= f[i][1] + f[i - 1][2]

4、o可以跟在a、e、i、o的后面，因此

f[i][3] \= f[i - 1][0] + f[i - 1][1] + f[i - 1][2] + f[i - 1][3] \= f[i][2] + f[i - 1][3]

5、u可以跟在所有字符后面，因此

f[i][4] \= f[i - 1][0] + f[i - 1][1] + f[i - 1][2] + f[i - 1][3] + f[i - 1][4] \= f[i][3] + f[i - 1][4]

处理完长度为n的情况，然后f[n][0]到f[n][4]的和就是最终答案了。

当然，这一题也可以通过组合数学来做。

首先有一个前提是对于合法的答案，相同的元音字符都是连续出现的。证明也很简单，若存在某个合法答案的第i位和第j位都是某个字符，且i到j之间还有其他字符，那么这个其他字符的字典序必然要大于该字符，此时这个其他字符与第j为的这个字符就不符合字典序了，也就证明了相同元音字符是连续出现的。

根据这个前提，一个很直观的思路就是n个字符串被分割成为a、e、i、o、u这五个元音字符连续出现的部分，问有多少种分割方式，那么换成小球，就是n个球之间插入4块隔板，隔板的位置可以重叠，问有多少种情况。再转化一下，就是n + 4个球中选4个不重复球，这些被选出来的球将被视为4块隔板，问有多少种情况。很明显答案就是C(n + 4, 4)了。

最后附上python代码：

```python
class Solution(object):
    def countVowelStrings(self, n):
        """
        :type n: int
        :rtype: int
        """

        return (n + 4) * (n + 3) * (n + 2) * (n + 1) / 24
```
