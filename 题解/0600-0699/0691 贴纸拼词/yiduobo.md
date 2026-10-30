---
title: "691. 贴纸拼词"
aliases: ["yiduobo的每日leetcode 691.贴纸拼词"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/310393907"
zhihu_id: "310393907"
zhihu_title: "yiduobo的每日leetcode 691.贴纸拼词"
question_id: "691"
question: "贴纸拼词"
problem_url: "https://leetcode.cn/problems/stickers-to-spell-word/"
created: "2020-11-24T22:37:59+08:00"
updated: "2020-11-24T22:37:59+08:00"
upvotes: 1
comments: 0
---

# 691. 贴纸拼词

> **[yiduobo的每日leetcode 691.贴纸拼词](https://zhuanlan.zhihu.com/p/310393907) · 知乎 · 2020-11-24 · 赞同 1**
> 力扣：[691. 贴纸拼词](https://leetcode.cn/problems/stickers-to-spell-word/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

691.贴纸拼词

[力扣](https://leetcode-cn.com/problems/stickers-to-spell-word/)

题目保证target的长度不超过15，因此可以使用状态压缩动态规划来做。具体来说就是对于target中的第index个字母，将其编码为2^index，那么整个target的编码就是2^(len(target)) - 1。

我们用一个数组f来储存所有的状态，其中f[status]表示拼出状态status代表的单词，所需要的最少单词数目。注意到题目中所有单词都是由小写字母组成，因此我们可以统计出target中每个字母出现的次数，以及每个字母会在哪些单词中出现。

对于f[status]，我们从剩下需要填充的字母当中选出一个，然后枚举所有包含该字母的单词，尝试选择该单词，此时的status由于部分字母得到填充会得到新的状态tmp。递归求解tmp之后判断f[tmp] + 1与f[status]的大小来更新f[status]即可。

最后附上python代码：

```python
class Solution(object):
    def minStickers(self, stickers, target):
        """
        :type stickers: List[str]
        :type target: str
        :rtype: int
        """

        char_dict = {}
        stickers_list = []
        for index, sticker in enumerate(stickers):
            tmp = {}
            for char in sticker:
                tmp[char] = tmp.get(char, 0) + 1
            stickers_list.append(tmp.items())
            for char in tmp:
                if char not in char_dict:
                    char_dict[char] = []
                char_dict[char].append(index)

        target_dict = {}
        pos_dict = {}
        for index, char in enumerate(target):
            if char not in char_dict:
                return -1
            if char not in target_dict:
                pos_dict[char] = 0
                target_dict[char] = []
            target_dict[char].append(1 << index)

        f = [None] * (1 << len(target))
        f[0] = 0
        return self.dfs((1 << len(target)) - 1, f, pos_dict, target_dict, char_dict, stickers_list)

    def dfs(self, now, f, pos_dict, target_dict, char_dict, stickers_list):
        if f[now] is None:
            for char in pos_dict:
                if pos_dict[char] != len(target_dict[char]):
                    break

            stickers_index = char_dict[char]
            for index in stickers_index:
                tmp = now
                tmp_pos_dict = pos_dict.copy()
                for char, cnt in stickers_list[index]:
                    while char in target_dict and cnt > 0 and tmp_pos_dict[char] < len(target_dict[char]):
                        tmp -= target_dict[char][tmp_pos_dict[char]]
                        tmp_pos_dict[char] += 1
                        cnt -= 1
                f[tmp] = self.dfs(tmp, f, tmp_pos_dict, target_dict, char_dict, stickers_list)
                if f[now] is None or f[now] > f[tmp] + 1:
                    f[now] = f[tmp] + 1

        return f[now]
```
