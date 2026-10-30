def _formula(S):
    f = S.get('freq')
    if not f:
        return '先数每个字母出现几次'
    vals = sorted(f.values(), reverse=True)
    return '前 8 名 ×1，9~16 名 ×2，17~24 名 ×3，其余 ×4'


CONFIG = dict(
    num=3016, title='输入单词需要的最少按键次数 II', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='频率降序 + 分档累加',
    tags=['灵神题单', '难度分 1534'],
    code='''
class Solution(object):
    def minimumPushes(self, word):

        freq = Counter(word)
        res = 0
        for index, f in enumerate(sorted(freq.values(), reverse=True)):
            if index < 8:
                res += f
            elif index < 16:
                res += f * 2
            elif index < 24:
                res += f * 3
            else:
                res += f * 4
        
        return res
''',
    call="Solution().minimumPushes('aabbccddeeffgghhiiiiii')",
    expect=24,
    views=[
        dict(type='map', var='freq', label='freq：字母出现次数', h=170, fmt=lambda k, v: f'{k}: {v}'),
        dict(type='array', var='sorted(freq.values(), reverse=True)', label='频率从大到小排好', h=200, cell=64,
             pointers={'index': 'blue'}),
        dict(type='text', size=32, fn=lambda S: f"当前第 `{S['index']}` 名（频率 `{S['f']}`）→ 每个字母按 =={S['index'] // 8 + 1}== 次，`res` = =={S['res']}==" if 'index' in S else '先数每个字母出现几次'),
    ],
    watch=['index', 'f', ('res', 'res', 'green')],
    captions={
        'freq = Counter': '`freq`：每个字母出现的次数 {freq}',
        'res = 0': '`res` 累计总按键次数',
        'for index, f': lambda S, B, r: (f'排名 `{S.index}`（从 0 数），出现 `{S.f}` 次' if 'f' in S and B.get('index') != S.get('index') or 'index' not in B else '遍历结束，所有字母都算过了'),
        'if index < 8': '`index = {index} < 8`？{"成立：占各键的第一个位置，按 1 次" if index < 8 else "不成立，排在 8 名之外，看下一档"}',
        'elif index < 16': '`index = {index} < 16`？{"成立：占各键的第二个位置，按 2 次" if index < 16 else "不成立，看下一档"}',
        'elif index < 24': '`index = {index} < 24`？{"成立：占各键的第三个位置，按 3 次" if index < 24 else "不成立，只剩第四个位置了"}',
        'res += f * 4': '剩下的字母放第四个位置：`{f} × 4` → `res` = =={res}==',
        'res += f * 3': '第三个位置：`{f} × 3` → `res` = =={res}==',
        'res += f * 2': '第二个位置：`{f} × 2` → `res` = =={res}==',
        8: '前 8 名：`res += f` = `{B.res} + {f}` → `res` = =={res}==',
        'return res': '最少按键次数 =={res}==',
    },
    cards=dict(
        one_liner='频率高的字符靠前：排名决定要按几次',
        complexity='时间 `O(n + |Σ| log |Σ|)`，空间 `O(|Σ|)`',
        problem=['`2`~`9` 共 8 个键，每个字母必须恰好放到一个键上，位置越靠后按得越多', '求输入 `word` 的最少按键次数', '示例：`aabbccddeeffgghhiiiiii` → `24`'],
        quote='为了使得按键次数最少，就应该让频率高的字符尽量靠前。只需统计每种字符出现的次数，然后从大到小排列，将排名在0-7的字符映射在2-9的第一个字符上，第8-15的字符映射在2-9的第二个字符上。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用 `Counter` 数每个字母的频率', '频率从大到小排，排名 0-7 按 1 次、8-15 按 2 次、16-23 按 3 次', '不需要真的映射，直接累加「频率 × 按键数」'],
        summary=['时间 `O(n + |Σ| log |Σ|)`，空间 `O(|Σ|)`', '排名从 0 开始：`index < 8` 是前 8 名', '26 个字母最多按 4 次，所以最后一档是 `f * 4`', '原文只有这一种写法，没有改动'],
    ),
)
