def _val(S, ch):
    return S['val_dict'].get(ch, ord(ch) - 96)


def _txt(S):
    if 'ch' not in S or S.get('_line') not in (12, 13, 14, 15, 16):
        return '把字符换成价值后，就是最大子段和：和为负就清零重来'
    return f'字符 `{S["ch"]}` 价值 `{S.get("v")}`；`now = {S["now"]}`，`res = {S["res"]}`'


CONFIG = dict(
    num=2606, title='找到最大开销的子字符串', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='最大子段和（贪心清零）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1422'],
    code='''
class Solution(object):
    def maximumCostSubstring(self, s, chars, vals):

        val_dict = {}
        for ch, v in zip(chars, vals):
            val_dict[ch] = v

        res = 0
        now = 0
        for ch in s:
            v = val_dict.get(ch, ord(ch) - 96)
            now += v
            if now < 0:
                now = 0
            res = max(res, now)
        
        return res
''',
    call="Solution().maximumCostSubstring('abdaab', 'd', [-5])",
    expect=4,
    views=[
        dict(type='string', var='s', label='s（红 = 价值为负，绿 = 价值为正）', h=190, cell=90,
             color=lambda S, i, v: ('red' if _val(S, v) < 0 else 'green') if 'val_dict' in S else None),
        dict(type='map', var='val_dict', label='val_dict（chars 中字符的价值）', h=110, fmt=lambda k, v: f'{k}: {v}'),
        dict(type='text', fn=_txt, size=26, h=80),
    ],
    watch=['ch', 'v', ('now', 'now', 'blue'), ('res', 'res', 'green')],
    captions={
        'for ch, v in zip': lambda S, B, r: ('chars 里的价值都记完了' if B.get('ch') == S.ch else f'取出 `chars` 里的 `{S.ch}`，价值 `{S.v}`'),
        'val_dict[ch] = v': '`{ch}` 的价值记为 `{v}`',
        8: '`res = 0`：空串开销为 0',
        9: '`now = 0`：当前这段子串的和',
        'for ch in s': '轮到字符 `{ch}`',
        'v = val_dict.get': '不在表里的字母，价值 = `ord(ch) - 96` = 字母表位置；`{ch}` 的价值 `{v}`',
        'now += v': '`now = {B.now} + ({v}) = {now}`：把这个字符接到当前子串后面',
        14: lambda S, B, r: f'`now = {S.now}`：和为负，==前面的都丢掉==，从下一个字符重新开始',
        'res = max': '`res = max({B.res}, {now}) = {res}`',
        'return res': '最大开销 = =={ret}==',
    },
    cards=dict(
        one_liner='字符换成价值，一趟贪心求最大子段和',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['每个字母有价值：不在 `chars` 里就是字母表位置，否则取 `vals`',
                 '子串开销 = 价值之和，空串为 0，求最大开销',
                 '示例：`s="adaa", chars="d", vals=[-1000]` → `2`'],
        quote='将字符转化为其对应的价值后，问题就变成了经典的最大子段和问题。对于这个问题，只需一趟遍历，使用贪心法进行求解就行了。',
        quote_src='—— yiduobo 题解',
        idea=['先用字典存好 `chars` 对应的价值',
              '遍历时累加 `now`，一旦 `now < 0` 就清零：负的前缀只会拖后腿',
              '每步用 `now` 更新 `res`'],
        summary=['时间 `O(n)`，空间 `O(1)`（字典最多 26 项）',
                 '`res` 从 0 开始，所以全是负数时答案是 0（空串）',
                 '`ord(ch) - 96` 对应 `a=1`，不要写成 `ord(ch) - 97`',
                 '同类题：53 最大子数组和'],
    ),
)
