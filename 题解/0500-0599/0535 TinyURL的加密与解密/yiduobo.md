---
title: "535. TinyURL的加密与解密"
aliases: ["yiduobo的每日leetcode 535.TinyURL的加密与解密"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/261170252"
zhihu_id: "261170252"
zhihu_title: "yiduobo的每日leetcode 535.TinyURL的加密与解密"
question_id: "535"
question: "TinyURL的加密与解密"
problem_url: "https://leetcode.cn/problems/encode-and-decode-tinyurl/"
created: "2020-10-05T23:23:00+08:00"
updated: "2020-10-05T23:23:00+08:00"
upvotes: 0
comments: 0
---

# 535. TinyURL的加密与解密

> **[yiduobo的每日leetcode 535.TinyURL的加密与解密](https://zhuanlan.zhihu.com/p/261170252) · 知乎 · 2020-10-05 · 赞同 0**
> 力扣：[535. TinyURL的加密与解密](https://leetcode.cn/problems/encode-and-decode-tinyurl/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

535.TinyURL的加密与解密<https://leetcode-cn.com/problems/encode-and-decode-tinyurl/>

这个题目应该有各式各样的方法，我在这里选择的是对a-z、A-Z以及0-9共62个字符进行62进制的编码，那么一共有62^6种TinyURL。在加密时，随机一个数，将其按照62进制的编码方式变成TinyURL，同时使用一个dict保存这个数到原始url的映射。在解密时，则将TinyURL按62进制复原为数字，然后从dict中找到其映射即可。

其中随机的方式是采用的之前519题中的方法（传送门在这里[yiduobo：yiduobo的每日leetcode 519.随机翻转矩阵](https://zhuanlan.zhihu.com/p/260813840)），避免随机到重复的数字。

最后附上python代码：

```python
class Codec:

    def __init__(self):
        self.key_dict = {}
        self.pos_dict = {}
        self.rest_key = 62 ** 6

    def encode(self, longUrl):
        """Encodes a URL to a shortened URL.
        
        :type longUrl: str
        :rtype: str
        """
        self.rest_key -= 1
        key_num = random.randint(0, self.rest_key)
        if key_num in self.pos_dict:
            real_key_num = self.pos_dict[key_num]
        else:
            real_key_num = key_num
        
        if self.rest_key in self.pos_dict:
            self.pos_dict[key_num] = self.pos_dict[self.rest_key]
        else:
            self.pos_dict[key_num] = self.rest_key

        self.pos_dict[self.rest_key] = real_key_num
        self.key_dict[real_key_num] = longUrl

        shortUrl = ''
        for index in range(6):
            tmp = real_key_num % 62
            if tmp < 10:
                shortUrl = str(tmp) + shortUrl
            elif tmp < 36:
                shortUrl = chr(int(tmp) + 87) + shortUrl
            else:
                shortUrl = chr(int(tmp) + 29) + shortUrl

            real_key_num /= 62

        return shortUrl

    def decode(self, shortUrl):
        """Decodes a shortened URL to its original URL.
        
        :type shortUrl: str
        :rtype: str
        """

        key = 0
        for char in shortUrl:
            if char <= '9':
                tmp = int(char)
            elif char >= 'a':
                tmp = ord(char) - 87
            else:
                tmp = ord(char) - 29
            key = key * 62 + tmp
        return self.key_dict[key]

# Your Codec object will be instantiated and called as such:
# codec = Codec()
# codec.decode(codec.encode(url))
```
