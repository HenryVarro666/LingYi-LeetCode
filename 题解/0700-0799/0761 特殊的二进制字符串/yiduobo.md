---
title: "761. 特殊的二进制序列"
aliases: ["yiduobo的每日leetcode 761.特殊的二进制序列"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/338583599"
zhihu_id: "338583599"
zhihu_title: "yiduobo的每日leetcode 761.特殊的二进制序列"
question_id: "761"
question: "特殊的二进制字符串"
problem_url: "https://leetcode.cn/problems/special-binary-string/"
difficulty: "Hard"
created: "2020-12-21T23:33:37+08:00"
updated: "2020-12-21T23:33:37+08:00"
upvotes: 0
comments: 0
---

# 761. 特殊的二进制序列

> **[yiduobo的每日leetcode 761.特殊的二进制序列](https://zhuanlan.zhihu.com/p/338583599) · 知乎 · 2020-12-21 · 赞同 0**
> 力扣：[761. 特殊的二进制字符串](https://leetcode.cn/problems/special-binary-string/) · Hard · 灵茶山艾府：[本质是合法括号字符串，递归排序（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

761.特殊的二进制序列

[力扣](https://leetcode-cn.com/problems/special-binary-string/)

首先，题目保证1和0的个数一样多，且所有前缀的1个数都不少于0的个数。仔细回想一下这两个性质，可以发现这实际上是合法的括号字符串，其中1代表左括号，而0代表右括号。那么对于一个括号串，有两种可能的情况，分别为：

1、不存在以首字母开头的合法子串：

此时意味着其中最左侧的括号与最右侧的括号是一对，合法的非空子串只有这个串本身，因此无法再这个层级上进行优化。

但是对于这种情况，若串的长度大于2，那么必然是11......00的形式。证明也很容易，首位和末尾很明显必然是1和0，由于不存在合法子串，因此这个串也不能是10......0或者1......10的形式，因此只能是11......00的形式。

有了这个结论，我们就可以掐头去尾，递归求解中间这个字符串。

2、存在以首字母开头的合法子串：

此时就可以使用括号匹配的方法，将原始串分解为多个part。由于题目可以交换相邻的两个part，实际上就是可以执行冒泡排序，因此可以优先递归求解各个part。注意到这里的part必然都是合法的最短字符串，换言之各个part都是满足条件1的，因此在递归求解时可以先掐头去尾然后再进行递归求解。求解完毕后拼上头的1和尾的0，然后将各个part按拼接后的字典序进行排序。

在具体实现上，由于递归求解时都要掐头去尾，因此可以将情况1看做只有1个part的情况，按照情况2的做法来实现。

最后附上python代码：

```python
def compare(self, other):
    if self + other > other + self:
        return -1
    else:
        return 1

class Solution(object):
    def makeLargestSpecial(self, S):
        """
        :type S: str
        :rtype: str
        """

        return self.dfs(S)

    def dfs(self, s):
        if len(s) == 0:
            return ''
        if len(s) == 2:
            return s

        parts = []
        cnt = 0
        last_pos = 0
        for index, char in enumerate(s):
            if char == '1':
                cnt += 1
            else:
                cnt -= 1
                if cnt == 0:
                    parts.append('1' + self.dfs(s[last_pos + 1 : index]) + '0')
                    last_pos = index + 1

        return ''.join(sorted(parts, cmp = compare))
```
