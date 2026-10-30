_P = 'sum(freq.values()) - (_line == 13) if _line != 15 else None'


def _dim(S, i, v):
    if 'freq' not in S or S.get('_line') == 15:
        return False
    return i > sum(S['freq'].values()) - (S.get('_line') == 13)


def _txt(S):
    if 'v' not in S or S.get('_line') in (6, 15):
        return '先对 24 取模；`v = 0` 配 `0`，否则配 `24 − v`'
    v = S['v']
    if v == 0:
        return f"`{S['h']} % 24 = 0` → 要找另一个 ==0=="
    return f"`{S['h']} % 24 = {v}` → 要找 `24 − {v}` = =={24 - v}=="


CONFIG = dict(
    num=3185, title='构成整天的下标对数目 II', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='取模配对 · 哈希表计频率',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1010'],
    code='''
class Solution(object):
    def countCompleteDayPairs(self, hours):

        freq = Counter()
        res = 0
        for h in hours:
            v = h % 24
            if v == 0:
                res += freq[v]
            else:
                res += freq[24 - v]

            freq[v] += 1

        return res
''',
    call='Solution().countCompleteDayPairs([72,48,24,3,21,45])',
    expect=5,
    views=[
        dict(type='array', var='hours', label='hours（h = 当前遍历到的数）', pointers={_P: 'blue'}, pointer_labels={_P: 'h'}, h=210,
             dim=_dim),
        dict(type='map', var='freq', label='freq：已出现过的 h % 24 → 次数', fmt=lambda k, v: f'{k}: {v}', h=170, font=34),
        dict(type='text', fn=_txt, h=90, size=30),
    ],
    watch=[('h', 'h', 'blue'), ('v', 'v', 'orange'), ('res', 'res', 'green')],
    captions={
        'freq = Counter()': '`freq` 记录已经出现过的时间（取模后）的频率',
        'res = 0': '`res` 统计下标对数',
        'for h in hours': lambda S, B, r: (f'遍历到 `h = {S.h}`' if sum(S.freq.values()) < len(S.hours) else '遍历结束'),
        'v = h % 24': '和是 24 的倍数只取决于余数：`v = {h} % 24 = {v}`',
        'if v == 0': lambda S, B, r: ('`v == 0`：要和==另一个 0== 配对' if S.v == 0
                                      else f'`v = {S.v} ≠ 0`：要和 `24 − {S.v} = {24 - S.v}` 配对'),
        'res += freq[v]': '前面有 `{freq[v]}` 个 0 → `res = {res}`',
        'res += freq[24 - v]': '前面有 `{freq[24 - v]}` 个 `{24 - v}` → `res = {res}`',
        'freq[v] += 1': '无论哪种情况，都把 `freq[{v}]` 加 1 → `{freq[v]}`，再往后遍历',
        'return res': '一共 `{res}` 对',
    },
    cards=dict(
        one_liner='先对 24 取模，0 配 0，v 配 24 − v',
        complexity='时间 `O(n)`，空间 `O(24)`',
        problem=['整天 = 24 的整数倍；求 `i < j` 且 `hours[i] + hours[j]` 构成整天的对数',
                 '示例：`[72,48,24,3]` → `3`',
                 '本视频：`[72,48,24,3,21,45]` → `5`'],
        quote='对于其中的某个元素v，若v等于0，那么就需要找到另一个0与之配对，否则需要找到24 - v与之配对。',
        quote_src='—— yiduobo 题解原文（3184 & 3185 合并题解）',
        idea=['和为 24 的倍数 ⇔ ==余数之和为 0 或 24==',
              '哈希表 `freq` 记录前面每种余数出现的频率',
              '一趟遍历：先累加答案，再把 `freq[v]` 加 1'],
        summary=['时间 `O(n)`，空间 `O(24)`',
                 '`v == 0` 单独处理：配的是 0，不是 24',
                 '`Counter` 读不存在的键返回 0，且==不会插入==该键',
                 '原文代码在 Python 3 下可直接运行，未做修改'],
    ),
)
