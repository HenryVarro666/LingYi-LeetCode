---
title: "3211. 生成不含相邻零的二进制字符串"
aliases: ["yiduobo的每日leetcode 3211.生成不含相邻零的二进制字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/recursion", "leetcode/backtracking", "题单/链表-二叉树与回溯", "题单/位运算", "题单/链表-二叉树与回溯/四-回溯", "题单/位运算/一-基础题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/708146154"
zhihu_id: "708146154"
zhihu_title: "yiduobo的每日leetcode 3211.生成不含相邻零的二进制字符串"
question_id: "3211"
question: "生成不含相邻零的二进制字符串"
problem_url: "https://leetcode.cn/problems/generate-binary-strings-without-adjacent-zeros/"
difficulty: "Medium"
rating: 1353
created: "2024-07-10T22:06:42+08:00"
updated: "2024-07-10T22:06:42+08:00"
upvotes: 0
comments: 0
---

# 3211. 生成不含相邻零的二进制字符串

> **[yiduobo的每日leetcode 3211.生成不含相邻零的二进制字符串](https://zhuanlan.zhihu.com/p/708146154) · 知乎 · 2024-07-10 · 赞同 0**
> 力扣：[3211. 生成不含相邻零的二进制字符串](https://leetcode.cn/problems/generate-binary-strings-without-adjacent-zeros/) · Medium · 灵茶山艾府：[两种方法：回溯/位运算（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3211.生成不含相邻零的二进制字符串

<https://leetcode.cn/problems/generate-binary-strings-without-adjacent-zeros/description/>

题目给出一个正整数n，要求找出所有长度为n，且不包含相邻的0的字符串。

一般这类问题问的都是合法字符串的数量，处理方法就是动态规划，令f[i]和g[i]分别表示长度为i且最后一个字符分别为1和0时的合法字符串数量。

对于本题，也可以如法炮制，令f[i]和g[i]分别表示长度为i且最后一个字符分别为1和0时的所有合法字符串。那么对于f[i]，可以在f[i - 1]和g[i - 1]的基础上填充一个1，那么就有

f\[i\] \= \[s + '1' for s in f\[i - 1\]\] + \[s + '1' for s in g\[i - 1\]\]

而对于g[i]，则只能在f[i - 1]的基础上填充一个0，因为g[i - 1]已经是以0结尾了，再添加0就会出现相邻的0。此时就有

g\[i\] \= \[s + '0' for s in f\[i - 1\]\]

初始状态下，f[1] \= '1'，g[1] \= '0'，接下来只需从2到n一趟遍历，计算出对应的f和g即可。

另外由于f和g每一轮都只和上一轮的状态有关，因此也可以用滚动数组省去i这一维。

最后附上python代码：

```python
class Solution(object):
    def validStrings(self, n):
        """
        :type n: int
        :rtype: List[str]
        """

        f = ["1"]
        g = ["0"]

        for index in range(1, n):
            new_f = [s + "1" for s in f] + [s + "1" for s in g]
            new_g = [s + "0" for s in f]
            f, g = new_f, new_g
        
        return f + g
```
