class Solution:
    def vowelStrings(self, words: List[str], left: int, right: int) -> int:
        return sum(s[0] in "aeiou" and s[-1] in "aeiou" for s in words[left:right+1])
    
## Python 的切片是“左闭右开区间”
## words[a:b] 包含下标 a 不包含下标 b；也就是区间： [a, b)
## 题目要求的区间是 [left, right]，所以切片应该words[left : right + 1]