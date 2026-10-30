---
title: "3999. 字符串变换后的最少分组数"
aliases: ["yiduobo的每日leetcode 3999.字符串变换后的最少分组数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/lexicographically-minimal-string-rotation", "题单/字符串", "题单/字符串/五-最小表示法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2063812954622105035"
zhihu_id: "2063812954622105035"
zhihu_title: "yiduobo的每日leetcode 3999.字符串变换后的最少分组数"
question_id: "3999"
question: "字符串变换后的最少分组数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-string-groups-through-transformations/"
difficulty: "Hard"
rating: 2162
created: "2026-07-24T02:38:26+08:00"
updated: "2026-07-24T02:38:27+08:00"
upvotes: 0
comments: 0
---

# 3999. 字符串变换后的最少分组数

> **[yiduobo的每日leetcode 3999.字符串变换后的最少分组数](https://zhuanlan.zhihu.com/p/2063812954622105035) · 知乎 · 2026-07-24 · 赞同 0**
> 力扣：[3999. 字符串变换后的最少分组数](https://leetcode.cn/problems/minimum-number-of-string-groups-through-transformations/) · Hard · 灵茶山艾府：[最小表示法 + 哈希集合去重（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3999.字符串变换后的最少分组数

<https://leetcode.cn/problems/minimum-number-of-string-groups-through-transformations/>

题目给出一个字符串数组words。

定义对字符串s的一次变换如下：

- 令E表示s中位于偶数下标处字符组成的子序列
- 令O表示s中位于奇数下标处字符组成的子序累
- 分别将E和O向右循环移动任意个位置，也可以不移动
- 将移动后的E中的字符依次放回到偶数下标，将移动后的O中的字符依次放回到奇数下标，从而重新构造字符串

若一个字符串可以通过一次变换得到另一个字符串，那么就称这两个字符串等价。

现在要求将words划分为最少数量的组，要求

- 每个字符串属于其中一个组
- 同一组内的任意两个字符串都等价

要求返回最少的分组数量。

题目要求将操作后相同的字符串都分到同一组，那么基于题目中的变换，一种可行的做法就是对于E和O，将这两个字符串都循环移动成字典序最小的那一个，然后再拼回到原串，最后通过集合记录不同原串的数量。

这样做的理由是若两个字符串可以通过循环移动变为相同，那么这两个字符串通过循环移动得到的字典序最小的字符串也必然相同。

到了这里，问题就变成了如何移动字符串使得字典序最小。对于这个问题，可以将原字符串复制一份，拼接在当前字符串后面，然后寻找起点位于原字符串中的所有后缀中最小的那一个就行了。

这个问题与之前遇到过的1163题相同，可以直接沿用之前的做法处理就行了。

[yiduobo的每日leetcode 1163.按字典序排在最后的子串](https://zhuanlan.zhihu.com/p/379043216)

最后附上python代码：

```python
class Solution(object):
    def minimumGroups(self, words):
        """
        :type words: List[str]
        :rtype: int
        """
        
        vis = set()

        def reorder(arr):
            n = len(arr)
            arr.extend(arr)

            now = 0
            p = 1
            k = 0
            while p < n:
                if arr[now + k] == arr[p + k]:
                    k += 1
                    if k == n:
                        return arr[now:]
                elif arr[now + k] < arr[p + k]:
                    p += k + 1
                    k = 0
                else:
                    if arr[now] > arr[p + k]:
                        now = p + k
                        if now >= n:
                            return arr[p:p + n]
                    else:
                        now = p

                    p = now + 1
                    k = 0
            
            return arr[now: now + n]

        for w in words:
            E = []
            O = []
            for index, c in enumerate(w):
                if index % 2 == 0:
                    E.append(c)
                else:
                    O.append(c)
                    
            vis.add(''.join(reorder(E) + reorder(O)))

        return len(vis)
```
