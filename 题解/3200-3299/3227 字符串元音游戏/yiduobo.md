---
title: "3227. 字符串元音游戏"
aliases: ["yiduobo的每日leetcode 3227.字符串元音游戏"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/game-theory", "题单/数学算法", "题单/贪心算法", "题单/数学算法/四-博弈论", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/720053432"
zhihu_id: "720053432"
zhihu_title: "yiduobo的每日leetcode 3227.字符串元音游戏"
question_id: "3227"
question: "字符串元音游戏"
problem_url: "https://leetcode.cn/problems/vowels-game-in-a-string/"
difficulty: "Medium"
rating: 1452
created: "2024-09-13T23:03:43+08:00"
updated: "2024-09-13T23:03:43+08:00"
upvotes: 1
comments: 0
---

# 3227. 字符串元音游戏

> **[yiduobo的每日leetcode 3227.字符串元音游戏](https://zhuanlan.zhihu.com/p/720053432) · 知乎 · 2024-09-13 · 赞同 1**
> 力扣：[3227. 字符串元音游戏](https://leetcode.cn/problems/vowels-game-in-a-string/) · Medium · 灵茶山艾府：[脑筋急转弯（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3227.字符串元音游戏

[. - 力扣（LeetCode）](https://leetcode.cn/problems/vowels-game-in-a-string/description/)

题目给出一个字符串，小红和小明轮流从中间执行删除操作。小红每一轮需要删除一个包含奇数个元音字符的非空子串，而小明每一轮则需要删除一个包含偶数个元音字符的非空子串，若某一方无法删除，则另一方获胜。从小红开始执行删除操作，问最终谁可以获胜。

不妨设字符串中存在cnt个元音字符，那么可以针对cnt的奇偶性来进行分析：

1、若cnt为奇数：

小红一轮就可以直接全部删完，此时小红必胜。

2、若cnt为偶数：

若cnt为0，那么小红一开始就无法删除，此时小明必胜。

若cnt大于0，那么小红第一轮可以删掉任意一个包含cnt - 1个元音字符的子串，那么剩下的字符串中还存在唯一一个元音字符。接下来无论小明如何操作，都不可能删掉这唯一一个元音字符，接下来再次轮到小红时，只需将剩下字符串全部删除即可，此时小红必胜。

综合上面两种情况可以发现，若字符串中存在元音字符，则小红必胜，否则小明必胜。

最后附上python代码：

```python
class Solution(object):
    def doesAliceWin(self, s):
        """
        :type s: str
        :rtype: bool
        """

        vowel_set = set(['a', 'e', 'i', 'o', 'u'])
        for char in s:
            if char in vowel_set:
                return True
        
        return False
```
