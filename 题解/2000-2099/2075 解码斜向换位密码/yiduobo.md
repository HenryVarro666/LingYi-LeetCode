---
title: "2075. 解码斜向换位密码"
aliases: ["yiduobo的每日leetcode 2075.解码斜向换位密码"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/517093918"
zhihu_id: "517093918"
zhihu_title: "yiduobo的每日leetcode 2075.解码斜向换位密码"
question_id: "2075"
question: "解码斜向换位密码"
problem_url: "https://leetcode.cn/problems/decode-the-slanted-ciphertext/"
difficulty: "Medium"
created: "2022-05-19T22:09:52+08:00"
updated: "2022-05-19T22:09:52+08:00"
upvotes: 0
comments: 0
---

# 2075. 解码斜向换位密码

> **[yiduobo的每日leetcode 2075.解码斜向换位密码](https://zhuanlan.zhihu.com/p/517093918) · 知乎 · 2022-05-19 · 赞同 0**
> 力扣：[2075. 解码斜向换位密码](https://leetcode.cn/problems/decode-the-slanted-ciphertext/) · Medium · 灵茶山艾府：[模拟：将 encodedText 视作二维矩阵](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2075.解码斜向换位密码

[力扣](https://leetcode.cn/problems/decode-the-slanted-ciphertext/)

题目已经给出了详细的解码方式，直接照着模拟解码就好了。

每一条斜线的首字符恰好也是每一列的首字符，那么可以遍历每一列，然后从首字符开始顺着右斜线向下遍历每个字符，直到来到矩阵的下边界或者有边界。

由于需要遍历每一列，那么就需要先知道列的数量cols，在这里可以通过encodedText的长度除以rows计算得到。接下来对于以第j列首字符开头的斜线而言，其再往右移动cols - 1 - j步就会到达矩阵的右边界，因此对于当前的列j，行的最大值就是min(rows - 1, cols - 1 - j)。

接下来开始执行遍历。对于当前遍历到的列j和行i，其对应的各自是矩阵中的第i行第i + j列这个格子，因此其在encodedText中对应的字符就是encodedText[i \* cols + i + j]，将其加入到答案末尾即可。

另外，由于题目不允许后缀空格出现，还需从答案末尾向前删除掉所有的后缀空格。

最后附上python代码：

```python
class Solution(object):
    def decodeCiphertext(self, encodedText, rows):
        """
        :type encodedText: str
        :type rows: int
        :rtype: str
        """

        n = len(encodedText)
        cols = n / rows
        res = []
        for j in range(cols):
            for i in range(min(rows, cols - j)):
                res.append(encodedText[i * cols + i + j])
        
        while res and res[-1] == ' ':
            res.pop()
        return ''.join(res)
```
