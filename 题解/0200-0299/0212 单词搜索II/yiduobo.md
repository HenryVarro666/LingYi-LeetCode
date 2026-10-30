---
title: "212. 单词搜索II"
aliases: ["yiduobo的每日leetcode 212.单词搜索II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/147665262"
zhihu_id: "147665262"
zhihu_title: "yiduobo的每日leetcode 212.单词搜索II"
question_id: "212"
question: "单词搜索II"
problem_url: "https://leetcode.cn/problems/word-search-ii/"
created: "2020-06-11T21:54:44+08:00"
updated: "2020-06-11T21:54:44+08:00"
upvotes: 0
comments: 0
---

# 212. 单词搜索II

> **[yiduobo的每日leetcode 212.单词搜索II](https://zhuanlan.zhihu.com/p/147665262) · 知乎 · 2020-06-11 · 赞同 0**
> 力扣：[212. 单词搜索II](https://leetcode.cn/problems/word-search-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

212.单词搜索II <https://leetcode-cn.com/problems/word-search-ii/>

又是一道运用到trie树的题目，同时也是79题单词搜索的升级版（传送门在这里[yiduobo：yiduobo的每日leetcode 79.单词搜索](https://zhuanlan.zhihu.com/p/133840036)）。

对于一个单词的情况，直接在board中搜索就好了，那么对于多个单词，在搜索完一个单词A后，实际上可能存在另一个单词B的前缀与A相同，那么就可以在这个基础上开展B的搜索，而不用从头开始搜索B。

于是，这里就可以使用trie树来维护所有单词的前缀，在除了基础的树结构与是否是单词结尾的标记之外，还可以额外添加一个计数器，表示从根节点到这个叶子节点形成的前缀是几个单词的公共前缀，那么在之后的搜索过程中，若当前节点的计数器大于0，说明有继续往下搜索的必要，否则就可以直接进行回溯了。

其他的细节与79题一样，通过方向数组来确定board中下一步的位置，然后通过trie树判断这一步是否合法即可。

我在这里的实现还是嵌套的dict，每个节点由子树dict、以该节点路径为前缀的单词数量计数器以及是否是某个单词结尾这三样组成。

在建树过程中，每当一个节点被走到，那么其计数器就加一，表示新来的这个单词会以这个节点的路径为前缀。

在搜索过程中，当某个节点完成某个孩子节点的搜索时，计数器需要减去搜索完该孩子节点所能匹配到的单词数目，那么计数器剩下的值就表示搜索其他孩子可能搜索到的单词数目。当计数器为0时，说明以当前节点路径为前缀的单词全都已经被找出来了，那么就没有继续往下搜索的必要了，直接回溯即可。

最后附上python代码：

```python
class Solution(object):
    def findWords(self, board, words):
        """
        :type board: List[List[str]]
        :type words: List[str]
        :rtype: List[str]
        """

        trie = [{}, len(words), False]
        for word in words:
            now = trie
            for char in word:
                if char not in now[0]:
                    now[0][char] = [{}, 1, False]
                else:
                    now[0][char][1] += 1
                now = now[0][char]
            now[2] = True

        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]

        res = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if trie[1] == 0:
                    return res
                if board[i][j] in trie[0] and trie[0][board[i][j]][1] > 0:
                    next_char = board[i][j]
                    board[i][j] = ' '
                    trie[1] -= self.dfs(board, i, j, trie[0][next_char], next_char, res, dx, dy)
                    board[i][j] = next_char
        
        return res

    def dfs(self, board, x, y, trie, now, res, dx, dy):
        cnt = 0
        if trie[2]:
            res.append(now)
            cnt = 1
            trie[2] = False

        if trie[1] > cnt:
            for index in range(4):
                next_x = x + dx[index]
                next_y = y + dy[index]
                if next_x >= 0 and next_x < len(board) and next_y >= 0 and next_y < len(board[0]):
                    next_char = board[next_x][next_y]
                    if next_char in trie[0] and trie[0][next_char][1] > 0:
                        board[next_x][next_y] = ' '
                        cnt += self.dfs(board, next_x, next_y, trie[0][next_char], now + next_char, res, dx, dy)
                        board[next_x][next_y] = next_char
            trie[1] -= cnt

        return cnt
```
