---
title: "201. 数字范围按位与"
aliases: ["yiduobo的每日leetcode 201.数字范围按位与"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "题单/位运算", "题单/面试经典-150-题", "题单/位运算/九-其他", "题单/面试经典-150-题/位运算"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/146350341"
zhihu_id: "146350341"
zhihu_title: "yiduobo的每日leetcode 201.数字范围按位与"
question_id: "201"
question: "数字范围按位与"
problem_url: "https://leetcode.cn/problems/bitwise-and-of-numbers-range/"
difficulty: "Medium"
created: "2020-06-06T19:02:02+08:00"
updated: "2020-06-06T19:02:02+08:00"
upvotes: 1
comments: 0
---

# 201. 数字范围按位与

> **[yiduobo的每日leetcode 201.数字范围按位与](https://zhuanlan.zhihu.com/p/146350341) · 知乎 · 2020-06-06 · 赞同 1**
> 力扣：[201. 数字范围按位与](https://leetcode.cn/problems/bitwise-and-of-numbers-range/) · Medium · 灵茶山艾府：[O(1) 写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

201.数字范围按位与<https://leetcode-cn.com/problems/bitwise-and-of-numbers-range/>

题目要求m到n的按位与，实际上就是求m到n在二进制表示下的最长公共前缀。由于m到n这些数是连续的，那么实际上m到n在二进制表示下的公共前缀就是m和n在二进制表示下的最长公共前缀，因为如果存在满足m与k最长公共前缀长度小于m与n最长公共前缀的长度，那么k一定小于m或者大于n，即在m到n之间是不会出现这种情况的。

现在的问题就变成了如何求解m与n的最长公共前缀，即找到m与n从高位开始往下的第一个不一样的位，于是可以不断右移m与n直到m与n相等，同时记录下左移的位数p，然后将相等时刻的m左移p位即可。

我在这里的做法是不断去除n的最低位1，直到n小于等于m，那么此时得到的n最终形式为XX...XXX000..00，而m则是XX...XXXYYY..YY，其中XX部分是一样的。于是此时最后执行一次与操作取出XX的部分即为最终结果。

最后附上python代码：

```python
class Solution(object):
    def rangeBitwiseAnd(self, m, n):
        """
        :type m: int
        :type n: int
        :rtype: int
        """

        while m < n:
            n &= n - 1
        
        return m & n
```
