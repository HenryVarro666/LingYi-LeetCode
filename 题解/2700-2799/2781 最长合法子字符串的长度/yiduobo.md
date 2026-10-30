---
title: "2781. 最长合法子字符串的长度"
aliases: ["yiduobo的每日leetcode 2781.最长合法子字符串的长度"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/字符串", "题单/滑动窗口与双指针/二-不定长滑动窗口", "题单/字符串/七-AC-自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/656138539"
zhihu_id: "656138539"
zhihu_title: "yiduobo的每日leetcode 2781.最长合法子字符串的长度"
question_id: "2781"
question: "最长合法子字符串的长度"
problem_url: "https://leetcode.cn/problems/length-of-the-longest-valid-substring/"
difficulty: "Hard"
rating: 2204
created: "2023-09-14T03:05:09+08:00"
updated: "2023-09-14T03:05:09+08:00"
upvotes: 0
comments: 0
---

# 2781. 最长合法子字符串的长度

> **[yiduobo的每日leetcode 2781.最长合法子字符串的长度](https://zhuanlan.zhihu.com/p/656138539) · 知乎 · 2023-09-14 · 赞同 0**
> 力扣：[2781. 最长合法子字符串的长度](https://leetcode.cn/problems/length-of-the-longest-valid-substring/) · Hard · 灵茶山艾府：[哈希表+滑动窗口（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2781.最长合法子字符串的长度

<https://leetcode.cn/problems/length-of-the-longest-valid-substring/description/>

对于这类不良单词过滤器问题，常规的做法是trie图，或者专业一点的名称叫做自动机。简单理解就是先通过不良单词形成trie树，然后使用类似kmp的做法，修改trie树其中部分节点的连接情况达到类似kmp算法的效果。trie树的实现比较复杂，对于本题还有跟简单的处理方法。

注意到题目保证了不良单词的长度不超过10，那么在这里就可以利用单调性加枚举来处理。

首先，对于某个位置right，设以right - 1为右边界的最长合法子字符串，其左边界为left，那么对于right自身，以right为右边界的最长合法子字符串的左边界left'必然大于等于left。证明也很简单，由于right - 1对应的left是最左侧的合法左边界，那么对于所有左边界在0到left - 1之间，右边界为right - 1的子字符串而言，其中都必然存在不良单词，而对于所有左边界在0到left - 1之间，右边界为right的子字符串，相当于在之前以right - 1为右边界的子字符串末尾额外加上一个字符，因此其中也必然存在不良单词，从而得到left' 必须要大于等于left。

另外，对于上一轮的子串s[left : right]而言，由于right向右移动了一位新加入了字符s[right]，因此在这里就可能带来末尾字符为s[right]的不良单词。题目保证了不良单词的长度不超过10，在这里就只需枚举所有不良单词可能的起点下标，也就是从right - 9开始枚举到right，检测区间内的单词是否为不良单词，这里可以通过trie树或者哈希表来进行检测。对于枚举到的下标index，若s[index : right + 1]是不良单词，那么就需要使用index + 1来更新合法左边界left'，反之left'保持不变。枚举完成后，就得到了right对应的左边界left'，此时使用这个子数组的长度更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def longestValidSubstring(self, word, forbidden):
        """
        :type word: str
        :type forbidden: List[str]
        :rtype: int
        """

        forbidden_set = set(forbidden)
        left = 0
        res = 0
        right = 0
        while right < len(word):
            for index in range(max(0, right - 9), right + 1):
                if word[index : right + 1] in forbidden_set:
                    left = max(left, index + 1)
            
            res = max(res, right - left + 1)
            right += 1
        
        return res
```
