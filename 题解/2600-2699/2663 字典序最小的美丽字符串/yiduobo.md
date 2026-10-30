---
title: "2663. 字典序最小的美丽字符串"
aliases: ["yiduobo的每日leetcode 2663.字典序最小的美丽字符串"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/648599293"
zhihu_id: "648599293"
zhihu_title: "yiduobo的每日leetcode 2663.字典序最小的美丽字符串"
question_id: "2663"
question: "字典序最小的美丽字符串"
problem_url: "https://leetcode.cn/problems/lexicographically-smallest-beautiful-string/"
difficulty: "Hard"
rating: 2416
created: "2023-08-07T23:09:45+08:00"
updated: "2023-08-07T23:09:45+08:00"
upvotes: 0
comments: 0
---

# 2663. 字典序最小的美丽字符串

> **[yiduobo的每日leetcode 2663.字典序最小的美丽字符串](https://zhuanlan.zhihu.com/p/648599293) · 知乎 · 2023-08-07 · 赞同 0**
> 力扣：[2663. 字典序最小的美丽字符串](https://leetcode.cn/problems/lexicographically-smallest-beautiful-string/) · Hard · 灵茶山艾府：[贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2663.字典序最小的美丽字符串

[力扣](https://leetcode.cn/problems/lexicographically-smallest-beautiful-string/)

首先，题目给出的s是一个美丽字符串，那么就意味着s中不存在任何长度大于等于2的回文串。更进一步的，由于每个长度为偶数的回文串中心的两个字符是一个回文串，同时长度为奇数的回文串中心的三个字符也是一个回文串，因此在构造时只需要保证修改的部分不会产生新的长度为2以及长度为3的回文串就行了。

为了使得最终答案的字典序最小，那么就应该尽可能只修改字符串的末尾部分，于是可以从字符串尾部开始向前遍历，枚举必须进行修改的最高位。对于这个最高位上修改后的字符，需要满足以下三个条件：

1、修改后的字符必须比原字符要大，但是也不能超过字母表中的第k个字符

2、若当前位置左侧还有字符，那么修改后的字符不能与当前位置左侧的字符相同，因为这样会形成长度为2的回文串

3、若当前位置左侧两个位置还有字符，那么修改后的字符也不能与这个位置的字符相同，因为这样会形成长度为3的回文串

按照上面的规则找出需要修改的最高位，若找不到合法的位置，那么直接返回空字符串，否则就对该位进行修改。修改完毕后，该位右侧的字符应该选择一种字典序最小的构造方法。由于题目保证了k大于等于4，因此在这里必然存在一种可行的构造方式，于是只需一趟遍历，根据上面修改字符时的条件2和条件3，逐位选择字典序最小的字符进行填充就行了。

最后附上python代码：

```python
class Solution(object):
    def smallestBeautifulString(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: str
        """

        asc_list = []
        for char in s:
            asc_list.append(ord(char))
        
        max_asc = 97 + k - 1

        n = len(asc_list)
        flag = False
        p = n
        while p > 0 and not flag:
            p -= 1
            for asc in range(asc_list[p] + 1, max_asc + 1):
                if p > 0 and asc_list[p - 1] == asc:
                    continue
                if p > 1 and asc_list[p - 2] == asc:
                    continue
                
                flag = True
                asc_list[p] = asc
                break

        if p == 0 and not flag:
            return ""

        for index in range(p + 1, n):
            for asc in range(97, max_asc + 1):
                if index > 0 and asc_list[index - 1] == asc:
                    continue
                if index > 1 and asc_list[index - 2] == asc:
                    continue
                
                asc_list[index] = asc
                break
        
        return ''.join([chr(x) for x in asc_list])
```
