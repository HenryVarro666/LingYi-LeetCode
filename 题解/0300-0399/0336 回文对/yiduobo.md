---
title: "336. 回文对"
aliases: ["yiduobo的每日leetcode 336.回文对"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/161969535"
zhihu_id: "161969535"
zhihu_title: "yiduobo的每日leetcode 336.回文对"
question_id: "336"
question: "回文对"
problem_url: "https://leetcode.cn/problems/palindrome-pairs/"
created: "2020-07-20T22:20:06+08:00"
updated: "2020-07-20T22:20:06+08:00"
upvotes: 0
comments: 0
---

# 336. 回文对

> **[yiduobo的每日leetcode 336.回文对](https://zhuanlan.zhihu.com/p/161969535) · 知乎 · 2020-07-20 · 赞同 0**
> 力扣：[336. 回文对](https://leetcode.cn/problems/palindrome-pairs/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧、

336.回文对<https://leetcode-cn.com/problems/palindrome-pairs/>

对于两个字符串s和t，不妨设s的长度大于等于t的长度，那么：

1、如果s+t能形成回文串，那么s一定是reverse(t)的前缀，且reverse(t)除去s剩下的部分是回文的形式。

2、如果t+s能形成回文串，那么reverse(s)一定是t的前缀，且t除去reverse(s)剩下的部分是回文的形式。

对于判断剩下的部分是否为回文串，可以预先对所有的字符串执行一次马拉车算法，求出以每个字符为回文中心的最长回文半径，那么之后就可以用O(1)的时间来判断剩下的部分是否为回文串了。

而对于前缀匹配的问题，自然就想到使用trie树来做。由于这里需要匹配原串的前缀以及翻转串的前缀，因此需要维护两个trie树。

到了这里，大致的算法流程就有了：

1、对于每个words中的每个字符串，使用马拉车算法算出以其中各个字符为中心的最长回文半径。这一步的总时间复杂度为O(nk)。

2、按字符串的长度从小到大遍历字符串，这里排序的复杂度为O(nlogn)：

1\) 将当前字符串按正序逐个字符在reverse trie中行走，如果当前字符命中且为某个reverse word的结束字符，那么通过步骤1中计算出的回文半径判断剩余的部分是否为回文串，如果是，说明当前字符串与命中的翻转串能形成回文对。在这个过程中同步将当前字符串加入到trie中。

2\) 将当前字符串按反序逐个字符在trie中行走，如果当前字符命中且为某个word的结束字符，那么通过步骤1中计算出的回文半径判断剩余的部分是否为回文串，如果是，说明当前字符串与命中的字符串能形成回文对。在这个过程中同步将当前的字符串加入到reverse trie中。

需要注意的是，对于空串，一般的trie树实现不会响应它，于是需要特殊判断。另外，这里由在正序遍历时就更新了trie，因此在反序遍历时注意不要在trie中匹配自身。

这一步对于每个字符串，需要正反两次遍历，于是时间复杂度也是O(nk)。

因此，最终的时间复杂度为O(nk)。

不过，可能是由于测试数据的问题，上面O(nk)算法的耗时比使用dict判断前后缀以及暴力判断剩下的部分是否为回文串还要久。

最后附上python代码，其中注释掉的部分是O(nk)的算法：

```python
import time
class Solution(object):

    def check(self, s, l, r):
        while l < r:
            if s[l] != s[r]:
                return False
            l += 1
            r -= 1
        return True

    def palindromePairs(self, words):
        """
        :type words: List[str]
        :rtype: List[List[int]]
        """

        '''
        f = []

        for index, word in enumerate(words):
            s = '!' + '#'.join(list(word)) + '@'
            f.append([0])
            mid = 0
            right = 0
            for index in range(1, len(s) - 1, 1):
                if index < right:
                    f[-1].append(min(f[-1][2 * mid - index], right - index))
                else:
                    f[-1].append(1)
                while s[index - f[-1][index]] == s[index + f[-1][index]]:
                    f[-1][index] += 1
                if right < index + f[-1][index]:
                    right = index + f[-1][index]
                    mid = index
        '''

        len_list = [[index, len(word)] for index, word in enumerate(words)]
        len_list = sorted(len_list, key=lambda d:d[1])
        res = []

        prefix_dict = {}
        suffix_dict = {}
        for pos, word_len in len_list:
            if word_len == 0:
                for index in range(len(words)):
                    if index != pos and self.check(words[index], 0, len(words[index]) - 1):
                        res.append([pos, index])
                        res.append([index, pos])

            for index in range(word_len):
                if self.check(words[pos], index + 1, word_len - 1):
                    prefix = words[pos][:index + 1]
                    if prefix in suffix_dict:
                        res.append([pos, suffix_dict[prefix]])
                if self.check(words[pos], 0, index - 1):
                    suffix = words[pos][index:][::-1]
                    if suffix in prefix_dict:
                        res.append([prefix_dict[suffix], pos])

            prefix_dict[words[pos]] = pos
            suffix_dict[words[pos][::-1]] = pos

        '''
        trie = [{}, None]
        reverse_trie = [{}, None]

        for pos, word_len in len_list:
            if word_len == 0:
                for index in range(len(words)):
                    if index != pos and f[index][len(words[index])] == len(words[index]):
                        res.append([pos, index])
                        res.append([index, pos])
                continue

            now_trie = trie
            now_reverse = reverse_trie
            check_flag = True
            for index, char in enumerate(words[pos]):
                if check_flag and char in now_reverse[0]:
                    now_reverse = now_reverse[0][char]
                    if now_reverse[1] is not None and now_trie[1] != pos:
                        check_len = word_len - index - 1
                        if check_len == 0 or f[pos][word_len * 2 - check_len] == check_len:
                            res.append([pos, now_reverse[1]])
                else:
                    check_flag = False
                
                if char not in now_trie[0]:
                    now_trie[0][char] = [{}, None]
                now_trie = now_trie[0][char]
            now_trie[1] = pos

            now_trie = trie
            now_reverse = reverse_trie
            check_flag = True
            for index in range(word_len - 1, -1, -1):
                char = words[pos][index]
                if check_flag and char in now_trie[0]:
                    now_trie = now_trie[0][char]
                    if now_trie[1] is not None and now_trie[1] != pos:
                        check_len = index
                        if check_len == 0 or f[pos][check_len] == check_len:
                            res.append([now_trie[1], pos])
                else:
                    check_flag = False
                    
                if char not in now_reverse[0]:
                    now_reverse[0][char] = [{}, None]
                now_reverse = now_reverse[0][char]
            now_reverse[1] = pos
        '''

        return res
```
