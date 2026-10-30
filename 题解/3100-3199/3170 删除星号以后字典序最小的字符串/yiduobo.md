---
title: "3170. 删除星号以后字典序最小的字符串"
aliases: ["yiduobo的每日leetcode 3170.删除星号以后字典序最小的字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/greedy", "leetcode/bit-manipulation", "leetcode/sorting", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/三-栈", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/705221718"
zhihu_id: "705221718"
zhihu_title: "yiduobo的每日leetcode 3170.删除星号以后字典序最小的字符串"
question_id: "3170"
question: "删除星号以后字典序最小的字符串"
problem_url: "https://leetcode.cn/problems/lexicographically-minimum-string-after-removing-stars/"
difficulty: "Medium"
rating: 1772
created: "2024-06-25T00:35:38+08:00"
updated: "2024-06-25T00:35:38+08:00"
upvotes: 1
comments: 0
---

# 3170. 删除星号以后字典序最小的字符串

> **[yiduobo的每日leetcode 3170.删除星号以后字典序最小的字符串](https://zhuanlan.zhihu.com/p/705221718) · 知乎 · 2024-06-25 · 赞同 1**
> 力扣：[3170. 删除星号以后字典序最小的字符串](https://leetcode.cn/problems/lexicographically-minimum-string-after-removing-stars/) · Medium · 灵茶山艾府：[三种写法：26 个栈+位运算优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3170.删除星号以后字典序最小的字符串

[. - 力扣（LeetCode）](https://leetcode.cn/problems/lexicographically-minimum-string-after-removing-stars/description/)

题目给出一个字符串s，其中可能包含若干小写字符以及星号。接下来按从左到右的顺序删去所有星号，每删除一个星号时，需要将当前星号左侧的字典序最小的字符删去一个。问删掉所有星号后字典序最小的字符串是什么。

题目规定了必须从左到右删除星号，而删除星号时又必须删除其左侧的字典序最小的字符，那么需要考虑的问题就是对于当前星号左侧的剩余字符中字典序最小的字符，应该删掉其中哪一个。

为了使得最终答案的字典序最小，就应该让字典序小的字符尽量靠前，那么在这里就应该删掉字典序最小的字符中下标最靠后的那个。于是可以使用一个二维数组pos记录每种字符在s中出现的位置，接下来一趟遍历，若当前遍历到的char是一个字符，那么就将当前下标加入到pos[char]的末尾；若char是星号，那么就从'a'遍历到'z'，若当前字符c在剩余字符串中出现过，那么只需将pos[c][-1]标记为需要删除，然后将pos[c]的末尾元素弹出。

遍历完成后，再遍历一次字符串，将没有被标记过需要删除的字符收集起来即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def clearStars(self, s):
        """
        :type s: str
        :rtype: str
        """

        pos = {}
        remove = set()
        for index, char in enumerate(s):
            if 'a' <= char <= 'z':
                if char not in pos:
                    pos[char] = []
                pos[char].append(index)
            else:
                for asc in range(97, 123):
                    c = chr(asc)
                    if c in pos and len(pos[c]) > 0:
                        remove.add(pos[c][-1])
                        pos[c].pop()
                        break
            
                remove.add(index)
        
        return ''.join([s[index] if index not in remove else '' for index in range(len(s))])
```
