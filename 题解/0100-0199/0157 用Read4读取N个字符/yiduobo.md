---
title: "157. 用Read4读取N个字符"
aliases: ["yiduobo的每日leetcode 157.用Read4读取N个字符"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/590705854"
zhihu_id: "590705854"
zhihu_title: "yiduobo的每日leetcode 157.用Read4读取N个字符"
question_id: "157"
question: "用Read4读取N个字符"
problem_url: "https://leetcode.cn/problems/read-n-characters-given-read4/"
created: "2022-12-10T03:34:16+08:00"
updated: "2022-12-10T03:34:16+08:00"
upvotes: 0
comments: 0
---

# 157. 用Read4读取N个字符

> **[yiduobo的每日leetcode 157.用Read4读取N个字符](https://zhuanlan.zhihu.com/p/590705854) · 知乎 · 2022-12-10 · 赞同 0**
> 力扣：[157. 用Read4读取N个字符](https://leetcode.cn/problems/read-n-characters-given-read4/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

157.用Read4读取N个字符

[力扣](https://leetcode.cn/problems/read-n-characters-given-read4/)

题目给出了某种每次读取最多4个字符的方法Read4，要求调用Read4来实现读取n个字符。

由于每次调用最多新增4个字符，那么按照4的步长执行一次for循环，每轮都将读入的字符添加到最终需要返回的buf中就行了。需要注意n可能并不是4的倍数，因此在添加到buf中的字符达到n个时应该直接返回结果。

最后附上python代码：

```python
"""
The read4 API is already defined for you.

    @param buf4, a list of characters
    @return an integer
    def read4(buf4):

# Below is an example of how the read4 API can be called.
file = File("abcdefghijk") # File is "abcdefghijk", initially file pointer (fp) points to 'a'
buf4 = [' '] * 4 # Create buffer with enough space to store characters
read4(buf4) # read4 returns 4. Now buf = ['a','b','c','d'], fp points to 'e'
read4(buf4) # read4 returns 4. Now buf = ['e','f','g','h'], fp points to 'i'
read4(buf4) # read4 returns 3. Now buf = ['i','j','k',...], fp points to end of file
"""

class Solution(object):
    def read(self, buf, n):
        """
        :type buf: Destination buffer (List[str])
        :type n: Number of characters to read (int)
        :rtype: The number of actual characters read (int)
        """

        res = 0
        for offset in range(0, n, 4):
            buf4 = [' '] * 4
            for index in range(read4(buf4)):
                buf[offset + index] = buf4[index]
                res += 1
                if res == n:
                    return res
        
        return res
```
