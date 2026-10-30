def _tier(i):
    return 1 if i < 9 else 2 if i < 18 else 3


def _text(S):
    if 'index' in S and 'freq' in S:
        i, f = S['index'], S['freq']
        t = _tier(i)
        return f'第 {i + 1} 名 → 第 {t} 位，每次 `{t}` 键：`{f} × {t}` = =={f * t}==    累计 `{S["res"]}`'
    if 'cnt' in S and 'char' in S:
        return '先统计每个字符出现的次数'
    return '频次大的字符放第 1 位，其次第 2 位，最后第 3 位'


CONFIG = dict(
    num=2268, title='最少按键次数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='按频次排序 · 前 9 个按 1 次',
    tags=[],
    code='''
class Solution(object):
    def minimumKeypresses(self, s):

        cnt = {}
        for char in s:
            cnt[char] = cnt.get(char, 0) + 1
        
        res = 0
        
        for index, freq in enumerate(sorted(cnt.values(), reverse=True)):
            if index < 9:
                res += freq
            elif index < 18:
                res += freq * 2
            else:
                res += freq * 3
        
        return res
''',
    call="Solution().minimumKeypresses('aaabbccdefghijk')",
    expect=17,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='string', var='s', h=150,
             color=lambda S, i, v: 'yellow' if 'char' in S and v == S['char'] and 'freq' not in S else None),
        dict(type='map', var='cnt', fmt=lambda k, v: f'{k}: {v}', h=250),
        dict(type='array', var='sorted(cnt.values(), reverse=True)', h=190, label='按频次从大到小',
             pointers={'index': 'pink'},
             color=lambda S, i, v: ('green' if i < 9 else 'orange' if i < 18 else 'red') if 'index' in S and i <= S['index'] else None),
    ],
    watch=['char', 'index', 'freq', ('res', 'res', 'green')],
    captions={
        'cnt = {}': '`cnt` 记录每个字符出现的次数',
        'for char in s': '逐个看 `s` 里的字符：`char = {char!r}`',
        'cnt[char] =': '`cnt[{char!r}]` = =={cnt[char]}==（出现次数 +1）',
        'res = 0': '`res` 累计总按键次数',
        'for index, freq': lambda S, B, r: ('9 个键 × 3 个位置，名次都处理完了' if 'index' in B and B.get('index') == S.get('index')
                                            else f'第 {S["index"] + 1} 名：频次 `{S["freq"]}`，下标 `index = {S["index"]}`'),
        'if index < 9': lambda S, B, r: (f'`index = {S["index"]} < 9` 成立：排在前 9 名，放==第 1 位==，一次就按到' if S['index'] < 9
                                         else f'`index = {S["index"]} ≥ 9`：第 1 位 9 个键已被占满，往下判断'),
        'elif index < 18': lambda S, B, r: (f'`index = {S["index"]} < 18` 成立：放==第 2 位==，每次要按 2 下' if S['index'] < 18
                                            else f'`index = {S["index"]} ≥ 18`：前两位 18 个都占满'),
        'res += freq * 2': '第 2 位：每次 2 下，`res += {freq} × 2` → =={res}==',
        'res += freq * 3': '第 3 位：每次 3 下，`res += {freq} × 3` → =={res}==',
        12: '第 1 位：每次 1 下，`res += {freq}` → =={res}==',
        'return res': '最少按键 `{res}` 次',
    },
    cards=dict(
        one_liner='频次越高，越放在键盘靠前的位置',
        complexity='时间 `O(n + k log k)`，空间 `O(k)`（k 为不同字符数）',
        problem=['9 个按键，每键最多放 3 个小写字母，按第 `j` 位的字母要按 `j` 次',
                 '每个字母只能出现在一个位置，求输入 `s` 的最少按键次数',
                 '示例：`aaabbccdefghijk` → `17`'],
        quote='出现频率越高就越应该将其放在数字的第一位，若第一位用完了就应该放在第二位，最后才是第三位。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历统计每种字符的次数，再按次数==从大到小==排序',
              '排第 1–9 名的放第 1 位：频次 × 1；第 10–18 名放第 2 位：频次 × 2',
              '剩下的只能放第 3 位：频次 × 3，累加即答案'],
        summary=['时间 `O(n + k log k)`，`k ≤ 26`，空间 `O(k)`',
                 '先排序再按名次分档，名次判断用 `index` 的 `<9`、`<18`',
                 '易错点：第 2、3 位按键次数是频次再乘 2、3，不是只加一次',
                 '原文已是 Python 3 可运行写法，代码未改动'],
    ),
)
