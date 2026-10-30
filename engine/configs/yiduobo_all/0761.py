import functools


CONFIG = dict(
    num=761, title='特殊的二进制字符串', difficulty='Hard', category='字符串',
    author='yiduobo', technique='括号匹配 · 递归 + 自定义排序', tags=[],
    setup='''
def compare(self, other):
    if self + other > other + self:
        return -1
    else:
        return 1
''',
    code='''
class Solution(object):
    def makeLargestSpecial(self, S):

        return self.dfs(S)

    def dfs(self, s):
        if len(s) == 0:
            return ''
        if len(s) == 2:
            return s

        parts = []
        cnt = 0
        last_pos = 0
        for index, char in enumerate(s):
            if char == '1':
                cnt += 1
            else:
                cnt -= 1
                if cnt == 0:
                    parts.append('1' + self.dfs(s[last_pos + 1 : index]) + '0')
                    last_pos = index + 1

        return ''.join(sorted(parts, key = functools.cmp_to_key(compare)))
''',
    call='Solution().makeLargestSpecial("11011000")',
    expect='11100100',
    views=[
        dict(type='string', var='s', pointers={'last_pos': 'blue', 'index': 'pink'}, h=215, label='s（1 = 左括号，0 = 右括号）'),
        dict(type='array', var='parts', h=150, label='parts（拆出的最短合法串）'),
        dict(type='calls', h=230),
    ],
    watch=[('cnt', 'cnt', 'yellow'), ('last_pos', 'last_pos', 'blue'), ('index', 'index', 'pink'), ('parts', 'parts', 'green')],
    captions={
        'len(s) == 0': lambda S, B, r: '`s` 为空 → 返回空串（掐头去尾后可能出现）' if len(S.s) == 0 else '`s` 非空，继续',
        8: '空串，直接返回',
        4: '入口：交给 `dfs` 递归求解',
        'len(s) == 2': lambda S, B, r: ('长度为 2 必然是 `10` → 不用再优化，直接返回' if len(S.s) == 2 else '长度 > 2，需要拆分'),
        10: '`{ret}` 已经是最小的合法串，返回',
        'parts = []': '括号匹配，把 `s` 分解成多个 ==part==',
        'last_pos = 0': '`last_pos` 记录当前 part 的起点',
        'cnt = 0': '`cnt`：1 当左括号 +1，0 当右括号 −1',
        'for index, char': '看第 `{index}` 个字符 `{char}`',
        "if char == '1'": '`char = {char}`：{"左括号" if char == "1" else "右括号"}',
        'cnt += 1': '左括号，`cnt` → =={cnt}==',
        'cnt -= 1': '右括号，`cnt` → =={cnt}==',
        'if cnt == 0': lambda S, B, r: (f'`cnt = 0`：一个最短的合法串 `s[{S.last_pos}..{S.index}]` 结束了' if S.cnt == 0 else f'`cnt = {S.cnt}`，还没配平'),
        'parts.append': '这个 part 必是 `1……0`：掐头去尾递归 `s[{last_pos+1}:{index}]`，求完再拼回 1 和 0 放进 `parts`',
        'last_pos = index + 1': '下一个 part 从 `{last_pos}` 开始',
        24: '各 part 能相邻交换 = 冒泡排序，按==拼接后==字典序大的在前排好：`{ret}`',
    },
    cards=dict(
        one_liner='1 是左括号：拆成 part，各自掐头去尾递归，再按拼接字典序排',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['特殊序列：`1`、`0` 个数相等，任意前缀 `1` 不少于 `0`',
                 '每次可交换两个相邻的特殊子串，求字典序最大',
                 '示例：`11011000` → `11100100`'],
        quote='这实际上是合法的括号字符串，其中1代表左括号，而0代表右括号。',
        quote_src='—— yiduobo 题解原文',
        idea=['没有以首字母开头的更短合法子串时，必是 `11……00`：==掐头去尾==递归中间',
              '否则用括号匹配拆成多个 part，part 可相邻交换 → 冒泡排序',
              '只有 1 个 part 的情况和多个 part 写法一致，统一处理'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '先递归求每个 part 内部，再套回 1 和 0，最后才排序',
                 '原文为 Python 2 写法：`sorted(cmp=compare)` 已改为 `functools.cmp_to_key(compare)`，`compare` 放在 setup 中',
                 '同类题：合法括号串的拆分与重排'],
    ),
)
