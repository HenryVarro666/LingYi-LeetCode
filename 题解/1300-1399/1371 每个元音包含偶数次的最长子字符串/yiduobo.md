---
title: "1371. 每个元音包含偶数次的最长子字符串"
aliases: ["yiduobo的每日leetcode 1371.每个元音包含偶数次的最长子字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/400845649"
zhihu_id: "400845649"
zhihu_title: "yiduobo的每日leetcode 1371.每个元音包含偶数次的最长子字符串"
question_id: "1371"
question: "每个元音包含偶数次的最长子字符串"
problem_url: "https://leetcode.cn/problems/find-the-longest-substring-containing-vowels-in-even-counts/"
created: "2021-08-17T23:18:01+08:00"
updated: "2021-08-17T23:18:01+08:00"
upvotes: 0
comments: 0
---

# 1371. 每个元音包含偶数次的最长子字符串

> **[yiduobo的每日leetcode 1371.每个元音包含偶数次的最长子字符串](https://zhuanlan.zhihu.com/p/400845649) · 知乎 · 2021-08-17 · 赞同 0**
> 力扣：[1371. 每个元音包含偶数次的最长子字符串](https://leetcode.cn/problems/find-the-longest-substring-containing-vowels-in-even-counts/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1371.每个元音包含偶数次的最长子字符串

[力扣](https://leetcode-cn.com/problems/find-the-longest-substring-containing-vowels-in-even-counts/)

对于子字符串相关的问题，一般都会朝两个方向考虑，即双指针法和前缀数组法。在这里显然是前缀数组法更加使用。

最简单的思路就是一趟遍历，对每个位置index记录下s[:index]这个前缀字符串中各个元音字符出现的次数，那么对于当前的index，我们遍历0到index - 1，若中途出现某个位置p满足s[:index]中各个元音字符出现的次数减去s[:p]中各个元音出现的次数之后都为偶数，那么说明s[p + 1:index]就是以index为结尾的一个合法答案。我们对每个index都找出对应的p，其中最长的就是最终的答案。

上面的做法的时间复杂度比较高，还有优化的余地。

首先，题目只需要判断奇偶，具体出现的次数实际上并不重要，那么我们可以用二进制来表示某个元音字符出现的次数是奇数还是偶数。又由于一共只有5个元音字符，那么实际上对于每个index而言，我们都可以用一个5位的二进制来表示当前s\[:index\]中元音字符的奇偶性。具体来说，就是对元音字符a、e、i、o、u进行编码，分别表示1、2、4、8、16。那么对于当前的index，设f\[index\]表示s\[:index\]中元音字符的奇偶性。若s\[index\]不是元音字符，那么此时有f\[index\] \= f\[index - 1\]，否则f\[index\] \= f\[index - 1\] ^ val\[s\[index\]\]，其中val表示元音字符对应的编码。

这样一来，我们就可以使用哈希表来储存每种状态第一次出现的位置。对于当前的f[index]，设其上一次出现的位置为p，那么s[p + 1 : index]就是一个合法的答案，同样是从中选出最长的作为最终答案即可，此时时间复杂度就优化到了O(n)。

最后附上python代码：

```python
class Solution(object):
    def findTheLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """

        val = {'a': 1, 'e': 2, 'i': 4, 'o': 8, 'u': 16}
        pos_dict = {0: -1}

        now = 0
        res = 0
        for index, char in enumerate(s):
            if char in val:
                now ^= val[char]
                if now not in pos_dict:
                    pos_dict[now] = index
                
            res = max(res, index - pos_dict[now])

        return res
```
