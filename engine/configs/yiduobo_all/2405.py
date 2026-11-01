CONFIG = dict(
    num=2405, title='子字符串的最优划分', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='贪心 + set 记录当前划分',
    tags=['贪心与思维', '划分型贪心', '难度分 1355'],
    code='''
class Solution(object):
    def partitionString(self, s):

        used = set()
        res = 0
        for char in s:
            if char in used:
                res += 1
                used = set()
            used.add(char)
        
        return res + 1
''',
    call='Solution().partitionString("abcabdd")',
    expect=3,
    views=[
        dict(type='string', var='s', label='s', h=160),
        dict(type='set', var='used', label='used：当前这一段里的字符', h=170, fmt=lambda x: str(x)),
        dict(type='text', h=70, fn=lambda S: f"已切出 ==`{S['res']}`== 段（最后一段还没计入，最终要 +1）" if 'res' in S else ''),
    ],
    watch=['char', ('res', 'res', 'green')],
    captions={
        'used = set()': lambda S, B, r: ('`used` 记录当前这一段里出现过的字符' if 'char' not in S else '清空 `used`：从当前字符开始新的一段'),
        'for char in s': '看字符 `{char}`',
        'if char in used': lambda S, B, r: (f'`{S.char}` 已在当前段里 → 这一段到此为止' if S.char in S.used else f'`{S.char}` 还没出现过 → 可以继续放进当前段'),
        'res += 1': '已完成一段：`res` → =={res}==',
        'used.add': '把 `{char}` 放进当前段：`used = {used}`',
        'return res + 1': '最后一段还没被计入，答案 = `{res} + 1` = =={ret}==',
    },
    cards=dict(
        one_liner='第一段越长越好，重复了才切',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把 `s` 划分成若干子串，每个子串内字符互不相同',
                 '求最少划分成几个子串',
                 '示例：`abacaba` → `4`；本视频：`abcabdd` → `3`'],
        quote='对于划分出去的第一个字符串而言，应该尽可能地划分得长一些，这样一来后面剩余的字符串就可能有更好的划分方案。',
        quote_src='—— yiduobo 题解原文',
        idea=['后缀的最优划分不会比原串多，所以第一段要尽量长',
              '用 `set` 记当前段的字符，遇到重复就切一刀、清空 set',
              '切出去的段数累计在 `res`，最后一段要补上 +1'],
        summary=['时间 `O(n)`，空间 `O(1)`（最多 26 个字符）',
                 '易错点：循环结束时最后一段没计入，所以 `return res + 1`',
                 '重置 `used = set()` 后别忘了仍要把当前字符加入',
                 '原文为 Python 2 风格，除 `class Solution(object)` 外无需改动，代码一字未改',
                 '对比灵神：灵神用整数位掩码当集合，yiduobo 用 set'],
    ),
)
