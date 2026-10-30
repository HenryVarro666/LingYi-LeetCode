---
title: "1032. 字符流"
aliases: ["yiduobo的每日leetcode 1032.字符流"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/369780943"
zhihu_id: "369780943"
zhihu_title: "yiduobo的每日leetcode 1032.字符流"
question_id: "1032"
question: "字符流"
problem_url: "https://leetcode.cn/problems/stream-of-characters/"
created: "2021-05-05T00:11:07+08:00"
updated: "2021-05-05T00:11:07+08:00"
upvotes: 0
comments: 0
---

# 1032. 字符流

> **[yiduobo的每日leetcode 1032.字符流](https://zhuanlan.zhihu.com/p/369780943) · 知乎 · 2021-05-05 · 赞同 0**
> 力扣：[1032. 字符流](https://leetcode.cn/problems/stream-of-characters/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1032.字符流

[力扣](https://leetcode-cn.com/problems/stream-of-characters/)

经典的字符串匹配问题。我们不妨先来关注简单的版本：假设words中仅有一个单词，那么这就是经典的模式匹配问题，可以使用kmp算法求解。

那么对于这里的若干个单词，如果每个都执行一次kmp算法，那么复杂度就太高了。对于多字符串相关的问题，一种常用的数据结构就是trie树，于是有一个想法：能否将trie树与kmp算法结合起来呢？答案是可以的，而且是处理这类多字符串匹配问题的一种常见做法，在字符串匹配这边一般称为trie图。实际上，kmp算法也可以认为是trie图在单个字符串形成的trie树上的特例。

接下来简单说明一下trie图。顾名思义，trie图就是将将trie树建立好之后，在trie树中添加一些边形成的图。回忆一下kmp算法中next的定义：对于当前字符串S[:p]，next[p]表示的是最靠后的位置q，其满足S[:q]是S[:p]的后缀。

对于trie树，也可以给出类似的定义：对于树中的节点p，其形成的字符就是从根节点开始向下走到节点p经过的边，不妨称为S[root -> p]。那么其next的定义就是层数最深的q，其满足S[root -> q]是S[root -> p]的后缀。

而trie图则是对于trie树中的每个节点p，都添加一条p到next[p]的边，这条边上面的值则是fa到p这条边上的值。

对于trie树中next的求解，也可以利用类似kmp算法求解next的方法，即从根节点开始逐层向下，利用当前节点父节点的next来求解当前节点的next。

设当前处理到节点p，其代表的字符为S[root -> p]。

首先判断边界情况。若此时的p为根节点，或者为第一层节点，那么其显然没有可以利用的后缀，因此有next[p] \= root。

接下来继续考虑一般情况：

设fa为p的父亲节点，那么就有

S[root -> p] \= S[root -> fa] + edge(fa, p)

其中edge(fa, p)表示从fa到p这条边上的字符，设为char。

对于fa而言，我们已经求得了next\[fa\]，那么就有S\[root -> next\[fa\]\]是S\[root -> fa\]的后缀。

若此时的next\[fa\]也存在一条边，上面的字符为char，那么S\[root -> next\[fa\]\] + char就是S\[root -> fa\] + char的后缀，换言之S\[root -> next\[fa\]\]就是S\[root -> p\]的后缀，于是此时就有next\[p\] \= next\[fa\].edge\[char\]

反过来，若此时的next\[fa\]没有char这条边，说明无法从next\[fa\]得到next\[p\]，于是需要继续向上，从next\[next\[fa\]\]开始寻找。

重复上面的过程知道找到next[p]，或者返回到了根节点。若最终停止的节点也没有char这条边，那么说明肯定停在了根节点，那么此时next[p]就是根节点，表示没有可以利用的后缀，需要从头开始匹配。

需要注意的是，对于节点p而言，若p本身不是某个单词的结尾，但是next\[p\]是某个单词的结尾，那么我们也应当将p看作是某个单词的结尾。理由也很简单，即S\[root -> next\[p\]\] 是S\[root -> p\]的后缀，那么我们如果能走到p，说明匹配上了S\[root -> p\]，那么此时其后缀S\[root -> next\[p\]\]也必然被匹配上了。

例如字符串abab和ba，设abab的第二a后面，第二个b前面的节点为p，那么next\[p\]就是ba中的a后面的节点q。当出现字符串aba时，我们匹配上了字符串S\[root -> p\]也就是aba，那么就必然有S\[root -> next\[p\]\]，也就是aba的某个后缀ba被匹配上了。

建立好trie图之后，就可以开始进行匹配了。我们设置一个指针pos在trie图中移动来匹配letter，pos的初始值为trie树的根节点。

那么对于letter：

1、若此时的pos有letter这条边，那么就将pos移动到pos.edge[letter]

2、若此时的pos没有letter这条边，那么就将pos移动到next[pos]得到pos’。若此时新的pos’依然没有letter这条边，那么就继续将pos’继续向上移动到next[pos’]，直到移动回到根节点或者此时的pos存在letter这条边。设最后停在了end_pos，若此时的end_pos有letter这条边，那么就将pos最后置为end_pos.edge[letter]，否则就将pos置为end_pos。

接下来，若此时的pos是某个单词的结尾，那么就返回true，否则返回false。

最后附上python代码：

```python
class Node(object):

    def __init__(self):
        self.char_dict = {}
        self.next = None
        self.end_flag = False

class StreamChecker(object):

    def __init__(self, words):
        """
        :type words: List[str]
        """

        self.trie = Node()
        
        for word in words:
            self.add(word)
        
        q = [[self.trie, None, None]]
        l = 0 
        r = 1
        while l < r:
            now, fa, edge = q[l]
            l += 1
            if now == self.trie or fa == self.trie:
                now.next = self.trie
            else:
                tmp = fa.next
                while tmp != self.trie and edge not in tmp.char_dict:
                    tmp = tmp.next
                if edge in tmp.char_dict:
                    now.next = tmp.char_dict[edge]
                    if now.next.end_flag:
                        now.end_flag = True
                else:
                    now.next = self.trie

            for char in now.char_dict:
                q.append([now.char_dict[char], now, char])
                r += 1
        
        self.pos = self.trie

    def add(self, word):
        now = self.trie
        for char in word:
            if char not in now.char_dict:
                now.char_dict[char] = Node()
            now = now.char_dict[char]
        now.end_flag = True

    def query(self, letter):
        """
        :type letter: str
        :rtype: bool
        """
        while self.pos != self.trie and letter not in self.pos.char_dict:
            self.pos = self.pos.next
        
        if letter in self.pos.char_dict:
            self.pos = self.pos.char_dict[letter]
        else:
            self.pos = self.trie
        
        return self.pos.end_flag
            

# Your StreamChecker object will be instantiated and called as such:
# obj = StreamChecker(words)
# param_1 = obj.query(letter)
```
