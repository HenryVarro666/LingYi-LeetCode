---
title: "158. 用Read4读取n个字符II"
aliases: ["yiduobo的每日leetcode 158.用Read4读取n个字符II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/590825435"
zhihu_id: "590825435"
zhihu_title: "yiduobo的每日leetcode 158.用Read4读取n个字符II"
question_id: "158"
question: "用Read4读取n个字符II"
problem_url: "https://leetcode.cn/problems/read-n-characters-given-read4-ii-call-multiple-times/"
created: "2022-12-10T17:37:37+08:00"
updated: "2022-12-10T17:37:37+08:00"
upvotes: 0
comments: 0
---

# 158. 用Read4读取n个字符II

> **[yiduobo的每日leetcode 158.用Read4读取n个字符II](https://zhuanlan.zhihu.com/p/590825435) · 知乎 · 2022-12-10 · 赞同 0**
> 力扣：[158. 用Read4读取n个字符II](https://leetcode.cn/problems/read-n-characters-given-read4-ii-call-multiple-times/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

158.用Read4读取n个字符II

[力扣](https://leetcode.cn/problems/read-n-characters-given-read4-ii-call-multiple-times/)

本题依然是给出读取4个字符的方法read4，不过这里每次调用read之后，read4读出来的buf4可能没有被消耗完，而下一次调用read时需要从没消耗完的位置开始读，因此在这里需要设置一个全局的buf4，同时设置配套的read_len和p，表示这个全局buf4的长度以及已经消耗掉的字符数。

接下来对于每次read操作，都从p开始将buf4中的内容写入到buf中。若某一时刻p等于read_len，那么就调用read4重新装载buf4，同时更新其对应的read_len，重置p为0。重复此过程直到往buf中写入n个字符，或者read4读不到任何东西为止。

最后附上python代码：

```python
# The read4 API is already defined for you.
# @param buf4, List[str]
# @return an integer
# def read4(buf4):

class Solution(object):

    def __init__(self):
        self.p = 0
        self.read_len = 0
        self.buf4 = [' '] * 4

    def read(self, buf, n):
        """
        :type buf: List[str]
        :type n: int
        :rtype: int
        """

        cnt = 0
        while cnt < n:
            if self.p == self.read_len:
                self.buf4 = [' '] * 4
                self.read_len = read4(self.buf4)
                self.p = 0
                if self.read_len == 0:
                    break
            
            buf[cnt] = self.buf4[self.p]
            self.p += 1
            cnt += 1
        
        return cnt
```
