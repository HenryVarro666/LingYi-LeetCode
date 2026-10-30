---
title: "3029. 将单词恢复初始状态所需的最短时间I & 3031. 将单词恢复初始状态所需的最短时间II"
aliases: ["yiduobo的每日leetcode 3029.将单词恢复初始状态所需的最短时间I && 3031.将单词恢复初始状态所需的最短时间II", "3029. 将单词恢复初始状态所需的最短时间I", "3031. 将单词恢复初始状态所需的最短时间II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hard", "题单/字符串", "题单/字符串/二-Z-函数-后缀的前缀"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/695360382"
zhihu_id: "695360382"
zhihu_title: "yiduobo的每日leetcode 3029.将单词恢复初始状态所需的最短时间I && 3031.将单词恢复初始状态所需的最短时间II"
question_id: ["3029", "3031"]
question: ["将单词恢复初始状态所需的最短时间 I", "将单词恢复初始状态所需的最短时间 II"]
problem_url: ["https://leetcode.cn/problems/minimum-time-to-revert-word-to-initial-state-i/", "https://leetcode.cn/problems/minimum-time-to-revert-word-to-initial-state-ii/"]
difficulty: ["Medium", "Hard"]
rating: 2278
created: "2024-04-30T03:14:38+08:00"
updated: "2024-04-30T03:14:38+08:00"
upvotes: 1
comments: 0
---

# 3029. 将单词恢复初始状态所需的最短时间I & 3031. 将单词恢复初始状态所需的最短时间II

> **[yiduobo的每日leetcode 3029.将单词恢复初始状态所需的最短时间I && 3031.将单词恢复初始状态所需的最短时间II](https://zhuanlan.zhihu.com/p/695360382) · 知乎 · 2024-04-30 · 赞同 1**
> 力扣：[3029. 将单词恢复初始状态所需的最短时间 I](https://leetcode.cn/problems/minimum-time-to-revert-word-to-initial-state-i/) · Medium · 灵茶山艾府：[O(n) 做法](灵茶山艾府.md)
> 力扣：[3031. 将单词恢复初始状态所需的最短时间 II](https://leetcode.cn/problems/minimum-time-to-revert-word-to-initial-state-ii/) · Hard · 灵茶山艾府：[【视频讲解】Z 函数（扩展 KMP）](../3031%20将单词恢复初始状态所需的最短时间%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3029.将单词恢复初始状态所需的最短时间I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-time-to-revert-word-to-initial-state-i/)

3031.将单词恢复初始状态所需的最短时间II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-time-to-revert-word-to-initial-state-ii/description/)

题目按每k个字符一组删去字符串的前缀，并在后方补充k个字符，补充的字符可以任意选择。问最少第几次操作后可以使得字符串复原。

两题的题设一样，第二题的数据规模较大，只能考虑O(n)或者O(nlogn)的算法。

首先，这里的操作次数显然有一个上下m，即字符串长度n除以k向上取整。在经过m轮操作后，整个字符串中原始的字符都将被删去，而补充进来的字符由于可以任意选择，那么直接补充原字符串对应的字符进来就行了。

接下来考虑操作次数t小于m的情况。此时删去的字符是字符串中的前t \* k个，也就是说，如果字符串中剩下的n - t \* k个字符，也就是word[t \* k : n]与字符串的前缀word[:n - t \* k]相同，那么就可以让补充进来的t \* k个字符与word的后缀相同，从而使得字符串复原。

换言之，在这里就需要能高效地判断对于每个位置index，能与字符串前缀匹配的最长长度是多少。这恰好就是扩展kmp算法中z数组的定义。

更具体的，令z\[index\]表示满足word\[index : index + z\[index\]\]与word\[:z\[index\]\]相等的最大值，即从每个位置index开始的后缀能与字符串前缀匹配的最大长度，那么对于z数组的求解：

1、首先设置z[0] \= 0，因为从下标0开始的后缀就是原字符串，如果按照定义设置为n不方便后续的计算

2、接下来对于index > 0：

先使用一组辅助变量right, left分别表示下标在0到index - 1之间的最大的index + z[index] - 1，以及其对应的index，也就是当前已知的最靠后的能与字符串前缀匹配的区间。

2-1）当index > right时：

此时无法利用之前的z数组，只能从index开始向后暴力匹配，即初始化z\[index\] \= 0，然后不断对比word\[z\[index\]\]与word\[index + z\[index\]\]，若匹配，则将z\[index\]加上1然后继续向后匹配。

2-2）当index \<\= right时：

left和right的存在本身就意味着word[: right - left + 1]这个前缀与word[left : right + 1]这个子串完全相同。

由于在这里的目的是求解从index开始的后缀与word前缀的匹配情况，那么在这里就可以先利用left和right这个区间。由于从left开始的子数组word[left : right + 1]与word[:right - left + 1]是完全相同的，那么这两个子数组都去掉前面的index - left个字符，也就是从index开始的子数组word[index : right + 1]与word[index - left : right - left + 1]也是完全相同的。换言之，在求解z[index]时就可以先借助之前z[index - left]的结果。

当z[index - left] \< right - index + 1时，也就是index - left + z[index - left] - 1并没有超出right - left时，index + z[index - left] - 1也不会超出right，且此时的index + z[index - left]就已经不匹配了，因此在这里直接就有z[index] \= z[index - left]。

反之，当z\[index - left\] >\= right - index + 1时，当前已知的信息是word\[index : right + 1\]能与前缀匹配上，但是从word\[right + 1\]开始的字符能否继续匹配，就无法再利用z\[index - left\]的结果了，因此在这里依然需要从right + 1开始向后暴力匹配，即先初始化z\[index\]为right - index + 1，然后还是对比word\[z\[index\]\]与word\[index + z\[index\]\]。

无论是哪种情况，计算得到当前的z[index]后，都需要使用index和index + z[index] - 1来更新left和right。

如果将最后这种情况与index > right的情况合并起来，得到的实现就是：

1、若index \<\= right且right - index + 1 > z[index - left]，那么就有z[index] \= z[index - left]

2、对于其他情况，先初始化z[index] \= max(0, right - index + 1)，然后从index + z[index]开始进行暴力匹配

3、使用当前的index以及z[index] + index - 1更新left和right，然后继续向后计算

得到z数组后，只需从下标k开始，以k为步长遍历下标index，若当前的index满足z[index] >\= n - index，也就说从index开始的整个后缀都能与word的前缀匹配，那么就说明找到了答案。

最后附上python代码：

```python
class Solution(object):
    def minimumTimeToInitialState(self, word, k):
        """
        :type word: str
        :type k: int
        :rtype: int
        """

        z = [0]
        left, right = 0, 0
        for index in range(1, len(word)):
            if index <= right and z[index - left] < right - index + 1:
                z.append(z[index - left])
            else:
                z.append(max(0, right - index + 1))
                while z[-1] + index < len(word) and word[z[-1] + index] == word[z[-1]]:
                    z[-1] += 1
                
            if index + z[-1] - 1 > right:
                left, right = index, index + z[-1] - 1

        for index in range(k, len(word), k):
            if z[index] >= len(word) - index:
                return index / k
        
        return (len(word) - 1) / k + 1
```
