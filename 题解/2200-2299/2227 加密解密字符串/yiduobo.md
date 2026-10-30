---
title: "2227. 加密解密字符串"
aliases: ["yiduobo的每日leetcode 2227.加密解密字符串"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/brainteaser", "leetcode/hash-table", "leetcode/string", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/543265749"
zhihu_id: "543265749"
zhihu_title: "yiduobo的每日leetcode 2227.加密解密字符串"
question_id: "2227"
question: "加密解密字符串"
problem_url: "https://leetcode.cn/problems/encrypt-and-decrypt-strings/"
difficulty: "Hard"
rating: 1945
created: "2022-07-19T00:17:47+08:00"
updated: "2022-07-19T00:17:47+08:00"
upvotes: 0
comments: 0
---

# 2227. 加密解密字符串

> **[yiduobo的每日leetcode 2227.加密解密字符串](https://zhuanlan.zhihu.com/p/543265749) · 知乎 · 2022-07-19 · 赞同 0**
> 力扣：[2227. 加密解密字符串](https://leetcode.cn/problems/encrypt-and-decrypt-strings/) · Hard · 灵茶山艾府：[逆向思维（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2227.加密解密字符串

[力扣](https://leetcode.cn/problems/encrypt-and-decrypt-strings/)

加密操作是比较好做的，直接按照字符映射一个一个字符进行变换就行了。解密相对比较复杂，因为存在一个密文对应多个原文的情况，不过注意到最终询问的是解密后的结果有多少个词出现在字典当中，同时字典的规模也很小，因此不妨逆向思维，先求出字典中每个词加密后是什么样的，并使用哈希表统计这些密文可以由多少个字典中的词加密得到，然后再解密时直接对着哈希表查找就行了。

最后附上python代码：

```python
class Encrypter(object):

    def __init__(self, keys, values, dictionary):
        """
        :type keys: List[str]
        :type values: List[str]
        :type dictionary: List[str]
        """
        
        self.mapping = {}
        for index in range(len(keys)):
            self.mapping[keys[index]] = values[index]

        self.en_dict = {}
        for word in dictionary:
            en_word = self.encrypt(word)
            if en_word is not None:
                self.en_dict[en_word] = self.en_dict.get(en_word, 0) + 1

    def encrypt(self, word1):
        """
        :type word1: str
        :rtype: str
        """
        res = []
        for char in word1:
            if char not in self.mapping:
                return None
            res.append(self.mapping[char])
        
        return ''.join(res)

    def decrypt(self, word2):
        """
        :type word2: str
        :rtype: int
        """
        return self.en_dict.get(word2, 0)

# Your Encrypter object will be instantiated and called as such:
# obj = Encrypter(keys, values, dictionary)
# param_1 = obj.encrypt(word1)
# param_2 = obj.decrypt(word2)
```
