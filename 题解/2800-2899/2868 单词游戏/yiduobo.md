---
title: "2868. 单词游戏"
aliases: ["yiduobo的每日leetcode 2868.单词游戏"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/662114478"
zhihu_id: "662114478"
zhihu_title: "yiduobo的每日leetcode 2868.单词游戏"
question_id: "2868"
question: "单词游戏"
problem_url: "https://leetcode.cn/problems/the-wording-game/"
created: "2023-10-19T02:27:33+08:00"
updated: "2023-10-19T02:27:33+08:00"
upvotes: 0
comments: 0
---

# 2868. 单词游戏

> **[yiduobo的每日leetcode 2868.单词游戏](https://zhuanlan.zhihu.com/p/662114478) · 知乎 · 2023-10-19 · 赞同 0**
> 力扣：[2868. 单词游戏](https://leetcode.cn/problems/the-wording-game/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2868.单词游戏

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/the-wording-game/description/)

贪心法的题目。首先可以明确两点：

1、若存在多个不改变首字符的可用单词，那么就应该选择其中字典序最大的那个：

不妨设当前玩家存在a和b两种不改变首字符的可用单词，且a \< b。

如果使用a，且对手接下来使用满足a \< c \< b的c，当前玩家还是可以使用b。反之如果对手使用满足a \< b \< c的c，那么接下来b无法再使用，这与直接使用b然后对手使用c也是等价的。

换言之，在这里使用a还是b并不会影响到输赢，但是使用b的好处是可以压缩整个游戏的流程，加速当前的算法。

2、若既存在不改变首字符的可用单词，也存在使用下一个后继字符作为首字符的可用单词，那么就应该选择首字符不变的这个单词

此时就有些变化了。设当前玩家有不改变首字符的可用单词a以及使用后继字符作为首字符的可用单词b，那么必然有a \< b。

如果对手手上有一个c满足a \< c \< b，或者b \< c且b与c的首字符相同，那么当前情况实际上与上面的情况1完全相同，选择a和b并不影响最终结果。但是，如果对手手上不存在这样的c，但是存在一个d满足d > b且d的首字符是b的首字符的后继，这里就不同了。很明显d是不能接在a后面的，但是可以接在b后面，那么在这里就显然应该使用a而不是b，因为使用a直接就赢了。

换言之，在这里使用a时有一种获胜情况是使用b无法达到的，但是使用b则不存在使用a到达不了的情况，因此在这里就应该选择a。

有了以上两点，就可以先分别遍历两个玩家的单词列表。由于已经有序，因此在这里就可以使用一个哈希表记录下每种字符最后一次作为首字符出现在这两个列表中的下标，其对应的必然是当前首字符中字典序最大的那个，符合上面使用的需求。

接下来从alice的词表中首个单词开始不断进行迭代，由bob先开始执行。

设上一轮玩家使用单词的首字符为pre，那么若当前玩家词表对应的哈希表中存在pre，就迭代到其对应的单词，若不存在，则检测是否存在pre的后继字符，若存在则进行迭代，否则说明当前玩家已经没有词可以用了，此时根据另一名玩家是否为alice返回true或false即可。

最后附上python代码：

```python
class Solution(object):
    def canAliceWin(self, a, b):
        """
        :type a: List[str]
        :type b: List[str]
        :rtype: bool
        """

        last = [{}, {}]

        for index in range(1, len(a)):
            last[0][a[index][0]] = index
        for index in range(len(b)):
            last[1][b[index][0]] = index

        def get(pre_player, pre_index, last):
            now_player = 1 - pre_player
            if pre_player == 0:
                pre_list = a
                now_list = b
            else:
                pre_list = b
                now_list = a
            
            pre_char = pre_list[pre_index][0]
            nxt_char = chr(ord(pre_char) + 1)
            for check_char in [pre_char, nxt_char]:
                if check_char in last[now_player] and now_list[last[now_player][check_char]] > pre_list[pre_index]:
                    return last[now_player][check_char]
            
            return -1

        pre_index = 0
        pre_player = 0
        while True:
            now_index = get(pre_player, pre_index, last)
            if now_index == -1:
                return pre_player == 0
            
            pre_index, pre_player = now_index, 1 - pre_player
            print(pre_index, pre_player)
```
