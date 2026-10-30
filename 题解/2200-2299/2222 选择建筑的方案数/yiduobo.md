---
title: "2222. 选择建筑的方案数"
aliases: ["yiduobo的每日leetcode 2222.选择建筑的方案数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "题单/动态规划", "题单/动态规划/六-状态机-DP", "题单/动态规划/七-其他线性-DP", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/542503804"
zhihu_id: "542503804"
zhihu_title: "yiduobo的每日leetcode 2222.选择建筑的方案数"
question_id: "2222"
question: "选择建筑的方案数"
problem_url: "https://leetcode.cn/problems/number-of-ways-to-select-buildings/"
difficulty: "Medium"
rating: 1657
created: "2022-07-16T23:33:13+08:00"
updated: "2022-07-16T23:33:13+08:00"
upvotes: 0
comments: 0
---

# 2222. 选择建筑的方案数

> **[yiduobo的每日leetcode 2222.选择建筑的方案数](https://zhuanlan.zhihu.com/p/542503804) · 知乎 · 2022-07-16 · 赞同 0**
> 力扣：[2222. 选择建筑的方案数](https://leetcode.cn/problems/number-of-ways-to-select-buildings/) · Medium · 灵茶山艾府：[计算 010 和 101 的出现次数](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2222.选择建筑的方案数

[力扣](https://leetcode.cn/problems/number-of-ways-to-select-buildings/)

题目要求找出所有的长度为3，且0和1交替出现的子序列，也就是010或者101这种类型的。

对于010，可以认为是在01这种子序列的基础上添加一个0，同样的，对于101则可以认为是在10的基础上添加一个1。那么问题就变成了对于字符串中的每个0，要求找出这个0左侧有多少个01这样的子序列，以及对于字符串中的每个1，在这个1左侧有多少个10这样的子序列。

同样的分析方法，对于01，就是当前这个1左侧0的数目，而对于10，则是当前这个0左侧1的数目。

根据上面的分析就得到了一种动态规划的做法。

令one[i]表示第0到第i个字符中1的数目，类似的，zero[i]表示0的数目，one_zero表示10的数目，zero_one表示01的数目。接下来从左向右一趟遍历，对于当前字符s[i]：

1、当s[i]为0时：

1-1）首先单个字符的状态是很直观的，one[i] \= one[i - 1]，zero[i] \= zero[i - 1] + 1

1-2）以s[i]为结尾的10的数目取决于0到i - 1之间1的数目，而如果不使用s[i]，那么原先在0到i - 1之间就有one_zero[i - 1]个合法的子序列10，因此就有one_zero[i] \= one_zero[i - 1] + one[i - 1]

1-3）没有以s[i]为结尾的01，因此zero_one[i] \= zero_one[i - 1]

1-4）此时可以得到010这样的合法序列，数量取决于0到i - 1之间01的数目，因此需要将答案加上zero_one[i - 1]

2、当s[i]为1时，与上面完全对称：

1-1）one[i] \= one[i - 1] + 1，zero[i] \= zero[i - 1]

1-2）zero_one[i] \= zero_one[i - 1] + zero[i - 1]

1-3）one_zero[i] \= one_zero[i - 1]

1-4）将one_zero[i - 1]累加到答案中

注意到这里所有的状态都只与上一轮有关，因此完全不需要数组，使用四个变量进行迭代就行了。

最后附上python代码：

```python
class Solution(object):
    def numberOfWays(self, s):
        """
        :type s: str
        :rtype: int
        """

        res = 0
        zero = one = 0
        zero_one = one_zero = 0
        for char in s:
            if char == '0':
                zero += 1
                one_zero += one
                res += zero_one
            else:
                one += 1
                zero_one += zero
                res += one_zero
        
        return res
```
