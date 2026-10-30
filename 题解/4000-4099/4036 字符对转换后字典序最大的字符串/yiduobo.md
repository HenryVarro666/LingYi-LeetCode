---
title: "4036. 字符对转换后字典序最大的字符串"
aliases: ["yiduobo的每日leetcode 4036.字符对转换后字典序最大的字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/bit-manipulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2078636844900677366"
zhihu_id: "2078636844900677366"
zhihu_title: "yiduobo的每日leetcode 4036.字符对转换后字典序最大的字符串"
question_id: "4036"
question: "字符对转换后字典序最大的字符串"
problem_url: "https://leetcode.cn/problems/lexicographically-largest-string-after-pair-transformations/"
difficulty: "Medium"
created: "2026-09-03T00:25:06+08:00"
updated: "2026-09-03T00:25:06+08:00"
upvotes: 1
comments: 0
---

# 4036. 字符对转换后字典序最大的字符串

> **[yiduobo的每日leetcode 4036.字符对转换后字典序最大的字符串](https://zhuanlan.zhihu.com/p/2078636844900677366) · 知乎 · 2026-09-03 · 赞同 1**
> 力扣：[4036. 字符对转换后字典序最大的字符串](https://leetcode.cn/problems/lexicographically-largest-string-after-pair-transformations/) · Medium · 灵茶山艾府：[位运算，简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4036.字符对转换后字典序最大的字符串

<https://leetcode.cn/problems/lexicographically-largest-string-after-pair-transformations/>

题目给出一个整数数组nums。

对于nums中的每个整数x，先生成一个由x个小写字符'a'组成的字符串。

接下来可以执行任意次操作(包括零次)，每次操作中，可以选择两个相邻且相同的字符，将二者合并为字母表中的下一个字符。例如'aa'可以替换为'b'，而'bb'则可以替换为'c'，不过'zz'无法进一步替换。

现在要求对于nums中的每个x，找出其可以得到的字典序最大的字符串。

对于给定的x，为了使得字典序最大，就应该尽量先合并出z，当无法合并出z时，再从'y'开始依次向下类推。更具体的说，就是先尽量使用2^25个'a'合并出'z'，直到'a'的数量不足2^25，此时再考虑用2^24、2^23这样一路下来合并字母表中靠后的字符。

在具体实现上，可以将x视为一个超长的2进制数，那么其可以写成

a[0] \* 2^0 + a[1] \* 2^1 + ... + a[25] \* 2^25

其中a[0]到a[24]只能是0或者1，而a[25]则可以大于1。这里的a数组就恰好表示每种字符在答案中出现的次数，将较大的字符放到前面即可构成答案。

于是只需从0到24进行一趟遍历，提取出a[0]到a[24]，若不为0，就将对应的字符加入答案数组。然后将x右移25位，位移之后的x就是上面的a[25]，将对应数量的z加入答案数组，然后再将答案数组翻转即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def largestString(self, nums):
        """
        :type nums: List[int]
        :rtype: List[str]
        """
        
        
        res = []
        for v in nums:
            s = []
            for index in range(25):
                if v & 1:
                    s.append(chr(index + 97))
                v >>= 1
            
            s.extend(['z'] * v)
            res.append(''.join(s[::-1]))
        
        return res
```
