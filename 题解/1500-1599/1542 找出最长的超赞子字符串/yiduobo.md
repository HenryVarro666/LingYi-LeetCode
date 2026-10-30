---
title: "1542. 找出最长的超赞子字符串"
aliases: ["yiduobo的每日leetcode 1542.找出最长的超赞子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/array", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/424974130"
zhihu_id: "424974130"
zhihu_title: "yiduobo的每日leetcode 1542.找出最长的超赞子字符串"
question_id: "1542"
question: "找出最长的超赞子字符串"
problem_url: "https://leetcode.cn/problems/find-longest-awesome-substring/"
difficulty: "Hard"
rating: 2222
created: "2021-10-23T22:10:25+08:00"
updated: "2021-10-23T22:10:25+08:00"
upvotes: 0
comments: 0
---

# 1542. 找出最长的超赞子字符串

> **[yiduobo的每日leetcode 1542.找出最长的超赞子字符串](https://zhuanlan.zhihu.com/p/424974130) · 知乎 · 2021-10-23 · 赞同 0**
> 力扣：[1542. 找出最长的超赞子字符串](https://leetcode.cn/problems/find-longest-awesome-substring/) · Hard · 灵茶山艾府：[前缀异或和，附类似题目（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1542.找出最长的超赞子字符串

[力扣](https://leetcode-cn.com/problems/find-longest-awesome-substring/)

首先分析超赞子字符串的定义：

1、必须是一个子串。字串就意味着可能需要用到双指针或前缀来解决的可能性，但是具体怎么做还需要再看别的条件

2、必须能凑出一个回文串。回文串可以分成有奇数长度，存在一个单独的中心字符，以及偶数长度，所有字符都是成对出现的。换言之，这个子字符串中每个字符出现的次数至多只能又一个奇数。

注意到这里字符串是由0到9这些数字组成的，因此可以使用一个10位二进制来表示当前子串中各个数字出现次数的奇偶性。那么对于一个超赞子字符串来说，若其每个数字出现次数都是偶数次，那么其编码就是0；若其各个数字出现次数中有一个奇数，那么其编码必然是2^p，其中p的取值范围为0到9，表示这个出现奇数次的数字。

有了上面的结论，可以使用前缀来解决这个问题。对于某个位置index，设s[0]到s[index]的编码为now，那么：

1、若now这个状态在之前已经出现过，设其最早出现的位置为pos，那么从pos + 1到index这一段的状态编码就是0，也就是说pos + 1到index这一段是一个超赞字符串

2、若now与2^p进行异或的结果在之前已经出现过，设其最早出现的位置为pos，那么从pos + 1到index这一段的状态编码就是2^p，也就是说pos + 1到index这一段是一个超赞字符串

于是我们可以一趟遍历，并使用一个哈希表来统计当前已有状态最早出现的位置。对于当前的状态码now，先与哈希表中出现过的状态码进行匹配来更新答案，然后将now加入到哈希表中并向后继续遍历。

最后附上python代码：

```python
class Solution(object):
    def longestAwesome(self, s):
        """
        :type s: str
        :rtype: int
        """

        pow2 = [1]
        for index in range(10):
            pow2.append(pow2[-1] + pow2[-1])
        status_dict = {0 : -1}
        now = 0
        res = 0
        for index, char in enumerate(s):
            now ^= (1 << int(char))
            for p in pow2:
                tmp = now ^ p
                if tmp in status_dict:
                    res = max(res, index - status_dict[tmp])
            
            if now in status_dict:
                res = max(res, index - status_dict[now])
            else:
                status_dict[now] = index

        return res
```
