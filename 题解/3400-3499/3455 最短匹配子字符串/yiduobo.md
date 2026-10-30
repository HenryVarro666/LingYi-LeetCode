---
title: "3455. 最短匹配子字符串"
aliases: ["yiduobo的每日leetcode 3455.最短匹配子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/two-pointers", "leetcode/string-matching", "题单/常用数据结构", "题单/字符串", "题单/常用数据结构/零-常用枚举技巧", "题单/字符串/一-KMP-前缀的后缀"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1894139832227312457"
zhihu_id: "1894139832227312457"
zhihu_title: "yiduobo的每日leetcode 3455.最短匹配子字符串"
question_id: "3455"
question: "最短匹配子字符串"
problem_url: "https://leetcode.cn/problems/shortest-matching-substring/"
difficulty: "Hard"
rating: 2303
created: "2025-04-11T21:54:01+08:00"
updated: "2025-04-11T21:55:50+08:00"
upvotes: 2
comments: 0
---

# 3455. 最短匹配子字符串

> **[yiduobo的每日leetcode 3455.最短匹配子字符串](https://zhuanlan.zhihu.com/p/1894139832227312457) · 知乎 · 2025-04-11 · 赞同 2**
> 力扣：[3455. 最短匹配子字符串](https://leetcode.cn/problems/shortest-matching-substring/) · Hard · 灵茶山艾府：[线性做法：KMP+枚举中间+三指针（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3455.最短匹配子字符串

[3455. 最短匹配子字符串 - 力扣（LeetCode）](https://leetcode.cn/problems/shortest-matching-substring/description/)

题目给出一个字符串s以及一个模式字符串p，其中p恰好包含了两个星号，星号可以匹配零个或者多个字符形成的任何子串。

现在要求从s中找出与p匹配的最短子串的长度，如果不存在这样的子串，则返回-1。

一般情况下，两个星号会将p切分成三个部分(当然也会有星号出现在开头或者末尾，以及两个星号相邻的情况，这些特殊情况放在最后再讨论)，对于这三个部分，分别记为first、second、third，那么就可以通过kmp算法，分别计算出这三个部分在s中出现的所有位置，在这里记为first_hit，second_hit，third_hit。接下来，只需从中找出一组first_index、second_index、third_index，满足：

1、first_hit[first_index] + len(first) \<\= second_hit[second_index]：

这个不等式的含义是first的首字母位于first_hit[index]，那么first的最后一个字母就位于first_hit[first_index] + len(first) - 1，而second的首字母必须大于first最后一个字母的下标，因此second_hit[second_index]必须大于等于first_hit[first_index] + len(first)

2、second_hit[second_index] + len(second) \<\= third_hit[third_index]：

理由同上

3、third_hit[third_index] + len(third) - 1 - first_hit[first_index] + 1最小：

前面third_hit[third_index] + len(third) - 1是third最后一个字母的下标，也就是s中对应子串的下标，而first_hit[first_index]则是first的首字母下标，也就是对应子串首字母的下标，二者相减后加1即为对应字符的长度。按题目要求应该找出其中最短的。

接下来的问题就变成了如何找出最优的first_index、second_index、third_index。由于first_hit、second_hit、third_hit都是通过kmp一趟遍历计算得到的，因此里面的元素是天然有序的，那么随着first_index的向后移动，first_hit[first_index] + len(first)也会跟着向后移动，因此second_index也必然会在之前的基础上向后移动；同理，third_index也会随着second_index的移动而移动。另一方面，为了使得最终的长度最短，那么second_index以及third_index应该在移动到刚好满足条件1以及条件2时就停止。这样一来，就可以对first_index进行一趟遍历，每一轮都在之前的基础上找到最小的可行的second_index以及third_index并更新答案即可。

最后，对于特殊情况，无非就是星号将p分割出来的first、second、third中存在空串的情况。当存在一个空串时，依然是对非空的两个部分通过kmp计算匹配的位置，然后枚举左侧非空子串匹配的所有下标，找出右侧子串在不与左侧子串重叠的前提下最靠前的匹配下标，然后更新答案；当存在两个空串时，只要剩下的子串是s的子串，也就是存在至少一个匹配的下标，那么答案就是这个子串的长度。

最后附上python代码：

```python
class Solution(object):
    def shortestMatchingSubstring(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: int
        """
        
        first_next = []
        second_next = []
        third_next = []
        
        def get_next(start, f):
            if start == len(p) or p[start] == '*':
                return start
            f.append(0)
            pos = 0
            now = start + 1
            while now < len(p) and p[now] != '*':
                while pos > 0 and p[pos + start] != p[now]:
                    pos = f[pos - 1]
                
                if p[pos + start] == p[now]:
                    pos += 1
                f.append(pos)
                now += 1
            
            return now

        start = -1
        start = get_next(start + 1, first_next)
        start = get_next(start + 1, second_next)
        start = get_next(start + 1, third_next)

        first_hit = []
        second_hit = []
        third_hit = []

        pos_first = 0
        pos_second = 0
        pos_third = 0

        for index, char in enumerate(s):
            if first_next:
                while pos_first > 0 and p[pos_first] != char:
                    pos_first = first_next[pos_first - 1]
                if p[pos_first] == char:
                    pos_first += 1
                    if pos_first == len(first_next):
                        first_hit.append(index - pos_first + 1)
                        pos_first = first_next[pos_first - 1]
            
            if second_next:
                while pos_second > 0 and p[pos_second + len(first_next) + 1] != char:
                    pos_second = second_next[pos_second - 1]
                if p[pos_second + len(first_next) + 1] == char:
                    pos_second += 1
                    if pos_second == len(second_next):
                        second_hit.append(index - pos_second + 1)
                        pos_second = second_next[pos_second - 1]
            
            if third_next:
                while pos_third > 0 and p[pos_third + len(first_next) + 1 + len(second_next) + 1] != char:
                    pos_third = third_next[pos_third - 1]
                if p[pos_third + len(first_next) + 1 + len(second_next) + 1] == char:
                    pos_third += 1
                    if pos_third == len(third_next):
                        third_hit.append(index - pos_third + 1)
                        pos_third = third_next[pos_third - 1]
        
        res = -1
        if first_next and second_next and third_next:
            first_index = 0
            second_index = 0
            third_index = 0
            while first_index < len(first_hit):
                while second_index < len(second_hit) and first_hit[first_index] + len(first_next) > second_hit[second_index]:
                    second_index += 1
                if second_index < len(second_hit):
                    while third_index < len(third_hit) and second_hit[second_index] + len(second_next) > third_hit[third_index]:
                        third_index += 1
                    
                    if third_index < len(third_hit):
                        length = third_hit[third_index] + len(third_next) - 1 - first_hit[first_index] + 1
                        if res == -1 or res > length:
                            res = length
                
                first_index += 1
        
        else:
            if first_next:
                left_part = first_hit
                left_length = len(first_next)
                if second_next:
                    right_part = second_hit
                    right_length = len(second_next)
                elif third_next:
                    right_part = third_hit
                    right_length = len(third_next)
                else:
                    right_part = None
                    right_length = 0
            
            elif second_next:
                left_part = second_hit
                left_length = len(second_next)
                if third_next:
                    right_part = third_hit
                    right_length = len(third_next)
                else:
                    right_part = None
                    right_length = 0
            
            else:
                if third_next:
                    left_part = third_hit
                    left_length = len(third_next)
                else:
                    left_part = None
                    left_length = 0
                right_part = None
                right_length = 0

            if right_part is None:
                if left_part is not None and len(left_part) == 0:
                    res = -1
                else:
                    res = left_length
            else:
                left_index = 0
                right_index = 0
                while left_index < len(left_part):
                    while right_index < len(right_part) and left_part[left_index] + left_length > right_part[right_index]:
                        right_index += 1
                
                    if right_index < len(right_part):
                        length = right_part[right_index] + right_length - 1 - left_part[left_index] + 1
                        if res == -1 or res > length:
                            res = length

                    left_index += 1
            
        return res
```
