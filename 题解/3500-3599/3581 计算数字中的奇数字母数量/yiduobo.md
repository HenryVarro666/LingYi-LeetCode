---
title: "3581. 计算数字中的奇数字母数量"
aliases: ["yiduobo的每日leetcode 3581.计算数字中的奇数字母数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1937924221197063859"
zhihu_id: "1937924221197063859"
zhihu_title: "yiduobo的每日leetcode 3581.计算数字中的奇数字母数量"
question_id: "3581"
question: "计算数字中的奇数字母数量"
problem_url: "https://leetcode.cn/problems/count-odd-letters-from-number/"
created: "2025-08-10T17:16:07+08:00"
updated: "2025-08-10T17:16:07+08:00"
upvotes: 1
comments: 0
---

# 3581. 计算数字中的奇数字母数量

> **[yiduobo的每日leetcode 3581.计算数字中的奇数字母数量](https://zhuanlan.zhihu.com/p/1937924221197063859) · 知乎 · 2025-08-10 · 赞同 1**
> 力扣：[3581. 计算数字中的奇数字母数量](https://leetcode.cn/problems/count-odd-letters-from-number/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3581.计算数字中的奇数字母数量

[3581. 计算数字中的奇数字母数量 - 力扣（LeetCode）](https://leetcode.cn/problems/count-odd-letters-from-number/description/)

题目给出一个整数n，要求先将n的每个数位转换为它的小写英文单词，然后将这些单词按顺序连接起来形成字符串s，最后计算s中出现奇数次的字符数量。

先建立0到9这些数字到英文单词的哈希表，接下来通过模10除以10的方法分离出n的每个数位，使用另一个哈希表cnt统计这些数位对应的单词中每种字符出现的次数。分离并统计完成后，只需遍历cnt，统计其中出现次数为奇数的字符数量即可。

最后附上python代码：

```python
class Solution(object):
    def countOddLetters(self, n):
        """
        :type n: int
        :rtype: int
        """

        words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        cnt = {}
        while n:
            d = n % 10
            n //= 10
            for char in words[d]:
                cnt[char] = cnt.get(char, 0) + 1
        
        res = 0
        for char in cnt:
            if cnt[char] % 2 == 1:
                res += 1
        
        return res
```
