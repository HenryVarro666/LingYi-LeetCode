---
title: "1233. 删除子文件夹"
aliases: ["yiduobo的每日leetcode 1233.删除子文件夹"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sorting", "题单/常用数据结构", "题单/常用数据结构/六-字典树-trie"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/384234047"
zhihu_id: "384234047"
zhihu_title: "yiduobo的每日leetcode 1233.删除子文件夹"
question_id: "1233"
question: "删除子文件夹"
problem_url: "https://leetcode.cn/problems/remove-sub-folders-from-the-filesystem/"
difficulty: "Medium"
created: "2021-06-26T16:19:08+08:00"
updated: "2021-06-26T16:19:08+08:00"
upvotes: 0
comments: 0
---

# 1233. 删除子文件夹

> **[yiduobo的每日leetcode 1233.删除子文件夹](https://zhuanlan.zhihu.com/p/384234047) · 知乎 · 2021-06-26 · 赞同 0**
> 力扣：[1233. 删除子文件夹](https://leetcode.cn/problems/remove-sub-folders-from-the-filesystem/) · Medium · 灵茶山艾府：[排序（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1233.删除子文件夹

[力扣](https://leetcode-cn.com/problems/remove-sub-folders-from-the-filesystem/)

若一个文件夹a是另一个文件夹b的子文件夹，那么二者必然有相同的前缀b，因此一个自然的想法就是利用trie树来进行判断。

首先将所有文件夹通过斜杠切分，这样做的目的是方便计算当前文件夹的层级。

接下来将所有文件夹按层级从小到大进行排序，然后依次加入trie树当中进行判断即可。

最后附上python代码：

```python
class Solution(object):
    def removeSubfolders(self, folder):
        """
        :type folder: List[str]
        :rtype: List[str]
        """

        splitted_folder = [x[1:].split('/') for index, x in enumerate(folder)]

        res = []
        root = [{}, False]
        for folder_list in sorted(splitted_folder, key=lambda d:len(d)):
            now = root
            flag = True
            for folder in folder_list:
                if now[1]:
                    flag = False
                    break
                if folder not in now[0]:
                    now[0][folder] = [{}, False]
                now = now[0][folder]
            
            if flag:
                now[1] = True
                res.append('/' + '/'.join(folder_list))
        
        return res
```
