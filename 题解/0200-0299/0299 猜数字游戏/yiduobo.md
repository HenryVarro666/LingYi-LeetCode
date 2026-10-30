---
title: "299. 猜数字游戏"
aliases: ["yiduobo的每日leetcode 299.猜数字游戏"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/array", "leetcode/hash-table", "leetcode/counting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/157612369"
zhihu_id: "157612369"
zhihu_title: "yiduobo的每日leetcode 299.猜数字游戏"
question_id: "299"
question: "猜数字游戏"
problem_url: "https://leetcode.cn/problems/bulls-and-cows/"
difficulty: "Medium"
created: "2020-07-07T20:32:06+08:00"
updated: "2020-07-07T20:32:06+08:00"
upvotes: 0
comments: 0
---

# 299. 猜数字游戏

> **[yiduobo的每日leetcode 299.猜数字游戏](https://zhuanlan.zhihu.com/p/157612369) · 知乎 · 2020-07-07 · 赞同 0**
> 力扣：[299. 猜数字游戏](https://leetcode.cn/problems/bulls-and-cows/) · Medium · 灵茶山艾府：[阅读理解（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

299.猜数字游戏<https://leetcode-cn.com/problems/bulls-and-cows/>

比较基础的题目。对于secret中的每个字母，统计出其出现的次数以及其出现在guess中的次数，二者取min就是这个字母的cows + bulls。同时，统计出位置正确的次数，即这个字母的bulls，然后相减得出cows即可。

最后附上python代码：

```python
class Solution(object):
    def getHint(self, secret, guess):
        """
        :type secret: str
        :type guess: str
        :rtype: str
        """

        A = B = 0

        secret_dict = {}
        guess_dict = {}
        for index in range(len(secret)):
            if secret[index] == guess[index]:
                A += 1
            secret_dict[secret[index]] = secret_dict.get(secret[index], 0) + 1
            guess_dict[guess[index]] = guess_dict.get(guess[index], 0) + 1

        for char in guess_dict:
            B += min(guess_dict[char], secret_dict.get(char, 0))
        
        B -= A

        return str(A) + 'A' + str(B) + 'B'
```
