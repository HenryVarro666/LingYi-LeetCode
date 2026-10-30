---
title: "1639. 通过给定词典构造目标字符串的方案数"
aliases: ["yiduobo的每日leetcode 1639.通过给定词典构造目标字符串的方案数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/438659245"
zhihu_id: "438659245"
zhihu_title: "yiduobo的每日leetcode 1639.通过给定词典构造目标字符串的方案数"
question_id: "1639"
question: "通过给定词典构造目标字符串的方案数"
problem_url: "https://leetcode.cn/problems/number-of-ways-to-form-a-target-string-given-a-dictionary/"
created: "2021-11-28T12:39:23+08:00"
updated: "2021-11-28T12:39:23+08:00"
upvotes: 0
comments: 0
---

# 1639. 通过给定词典构造目标字符串的方案数

> **[yiduobo的每日leetcode 1639.通过给定词典构造目标字符串的方案数](https://zhuanlan.zhihu.com/p/438659245) · 知乎 · 2021-11-28 · 赞同 0**
> 力扣：[1639. 通过给定词典构造目标字符串的方案数](https://leetcode.cn/problems/number-of-ways-to-form-a-target-string-given-a-dictionary/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1639.通过给定词典构造目标字符串的方案数

[力扣](https://leetcode-cn.com/problems/number-of-ways-to-form-a-target-string-given-a-dictionary/)

题目非常贴心地设定了一旦用过第k列上的字符，前k列的字符就不能再用了这样一个规则，那么摆明了就是前i前j这种形式的动态规划。令f[i][j]表示target中的前i个字符，通过words中的前j列去构造有多少种方案数。

方便起见，可以先对words进行预处理，统计出每一列上各个字符出现的次数，记为cnt。那么对于f[i][j]：

1、当i和j都为0时：

此时需要寻找words的第0列上有多少个target[0]，那么就有

f\[i\]\[j\] \= cnt_list\[0\]\[target\[0\]\]

2、当i等于0，j大于0时：

此时有两种可能。

第一种是target\[0\]出现在第j列，此时的可能性就是cnt_list\[j\]\[target\[0\]\]。

第二种可能则是target[0]由第0到第j - 1列处理掉了，那么就是f[i][j - 1]。

于是就有

f\[i\]\[j\] \= f\[i\]\[j - 1\] + cnt_list\[j\]\[target\[0\]\]

3、当i大于0，且i > j时：

此时一共需要i + 1个字符，但是最多只能从这0到j列中选出j + 1个字符，必然是无法满足条件的，因此这些情况下的f[i][j] \= 0

4、当i大于0，且i \<\= j时：

此时同样是两种情况。

第一种是target\[i\]出现在第j列，而第0到第i - 1个字符由第0到第j - 1列处理掉了，也就是f\[i - 1\]\[j - 1\]。而对于target\[i\]，第j列一共有cnt_list\[j\]\[target\[i\]\]种选择，因此此时总的可能性就是f\[i - 1\]\[j - 1\] \* cnt_list\[j\]\[target\[i\]\]。

第二种可能则是target[i]也是由0到第j - 1列处理掉的，那么就是f[i][j - 1]。

于是就有

f\[i\]\[j\] \= f\[i\]\[j - 1\] + f\[i - 1\]\[j - 1\] \* cnt_list\[j\]\[target\[i\]\]

最后附上python代码：

```python
class Solution(object):
    def numWays(self, words, target):
        """
        :type words: List[str]
        :type target: str
        :rtype: int
        """

        m = len(words[0])
        n = len(target)
        cnt_list = [{} for _ in range(m)]
        for word in words:
            for index, char in enumerate(word):
                cnt_list[index][char] = cnt_list[index].get(char, 0) + 1
        
        mod = 10 ** 9 + 7
        f = [[0] * m for _ in range(n)]
        for i, char in enumerate(target):
            for j in range(m):
                if i == 0:
                    if j == 0:
                        f[i][j] = cnt_list[0].get(char, 0)
                    else:
                        f[i][j] = f[i][j - 1] + cnt_list[j].get(char, 0)
                elif i <= j:
                    f[i][j] = (f[i][j - 1] + f[i - 1][j - 1] * cnt_list[j].get(char, 0)) % mod

        return f[-1][-1]
```
