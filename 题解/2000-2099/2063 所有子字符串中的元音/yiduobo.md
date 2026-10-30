---
title: "2063. 所有子字符串中的元音"
aliases: ["yiduobo的每日leetcode 2063.所有子字符串中的元音"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser", "leetcode/math", "leetcode/string", "leetcode/combinatorics", "leetcode/counting", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/514549119"
zhihu_id: "514549119"
zhihu_title: "yiduobo的每日leetcode 2063.所有子字符串中的元音"
question_id: "2063"
question: "所有子字符串中的元音"
problem_url: "https://leetcode.cn/problems/vowels-of-all-substrings/"
difficulty: "Medium"
rating: 1663
created: "2022-05-14T23:53:53+08:00"
updated: "2022-05-14T23:53:53+08:00"
upvotes: 0
comments: 0
---

# 2063. 所有子字符串中的元音

> **[yiduobo的每日leetcode 2063.所有子字符串中的元音](https://zhuanlan.zhihu.com/p/514549119) · 知乎 · 2022-05-14 · 赞同 0**
> 力扣：[2063. 所有子字符串中的元音](https://leetcode.cn/problems/vowels-of-all-substrings/) · Medium · 灵茶山艾府：[单独计算每个元音的出现次数](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2063.所有子字符串中的元音

[力扣](https://leetcode.cn/problems/vowels-of-all-substrings/)

从单个字符串的角度出发考虑是比较麻烦的，不妨转换一下思路，从单个元音字符串的角度出发来考虑。

对于单个元音字符而言，有多少个子字符串包含了该字符，该字符就会对最终答案做出多少贡献，那么对于字符串中下标为index的字符s[index]而言，其左侧有0到index - 1这一共index个字符，右侧有index + 1到n - 1这n - index - 1个字符，那么其左侧有(index + 1)种可行的选择方法，右侧有(n - index)种可行的选择方法，因此包含s[index]的子字符串数目就是(index + 1) \* (n - index)。

根据上面的结论，只需从左向右一趟遍历，对于当前的s[index]，若其为一个元音字符，那么就将答案加上(index + 1) \* (n - index)。

最后附上python代码：

```python
class Solution(object):
    def countVowels(self, word):
        """
        :type word: str
        :rtype: int
        """

        n = len(word)
        res = 0
        char_set = set(['a', 'e', 'i', 'o', 'u'])
        for index in range(n):
            if word[index] in char_set:
                res += (index + 1) * (n - index)
        return res
```
