def _pair_txt(S):
    if 'cnt' not in S:
        return ''
    if 'y' in S and 'x' in S and S['_line'] >= 12:
        x, y = S['x'], S['y']
        return f'枚举高度对 `({x}, {y})`：合成高度 `{x} + {y} = ==%d==`' % (x + y)
    if 'x' in S:
        return f"高度 `{S['x']}` 有 `{S['c']}` 块"
    return '`cnt`：每种高度的木板数；`cnt_pair`：合成出（含原板）该高度的木板数'


def _hl(S, i=None):
    return None


CONFIG = dict(
    num=4007, title='栅栏的最宽宽度', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表 · 枚举高度对',
    tags=[],
    code='''
class Solution:
    def maximumWidth(self, planks: list[int]) -> int:
        # 统计 planks 的元素出现次数
        cnt = Counter(planks)

        # 枚举所有高度对 (x,y)
        ans = 0
        cnt_pair = defaultdict(int)
        for x, c in cnt.items():
            cnt_pair[x] += c  # 方便最后算 max
            cnt_pair[x * 2] += c // 2  # 高为 x 的木板内部配对
            for y, c2 in cnt.items():
                if y > x:  # 避免 x+y 和 y+x 重复统计
                    cnt_pair[x + y] += min(c, c2)

        # 枚举栅栏高度
        return max(cnt_pair.values())
''',
    call='Solution().maximumWidth([1, 4, 2, 3, 3, 1])',
    expect=3,
    views=[
        dict(type='array', var='planks', label='planks（木板高度）', cell=80, h=150),
        dict(type='map', var='cnt', label='cnt：高度 → 原木板块数', fmt=lambda k, v: f'{k}: {v}块', h=150, font=30),
        dict(type='map', var='cnt_pair', label='cnt_pair：高度 → 能凑出的木板块数（含原板）', fmt=lambda k, v: f'{k}: {v}块', h=250, font=30),
        dict(type='text', size=28, h=70, fn=lambda S: (
            f"枚举高度对 `({S['x']}, {S['y']})`：合成高度 `{S['x']} + {S['y']}` = =={S['x'] + S['y']}=="
            if S['_line'] in (13, 14) and 'y' in S else
            f"当前高度 `x = {S['x']}`，有 `{S['c']}` 块" if 'x' in S and S['_line'] in (9, 10, 11) else '')),
    ],
    watch=[('x', 'x', 'blue'), ('c', 'c'), ('y', 'y', 'pink'), ('c2', 'c2')],
    skip=['ans = 0', 'cnt_pair = defaultdict'],
    max_steps=80,
    captions={
        'cnt = Counter': '`cnt` 统计每种木板高度的块数：`{dict(cnt)}`',
        'cnt_pair[x] += c': '高为 `{x}` 的木板直接可用 `{c}` 块 → `cnt_pair[{x}] = {cnt_pair[x]}`，最后只要在 `cnt_pair` 里取最大值',
        'cnt_pair[x * 2]': '高为 `{x}` 的木板内部两两合成：`{c} // 2 = {c // 2}` 块高 `{x * 2}` 的新板 → `cnt_pair[{x * 2}] = {cnt_pair[x * 2]}`',
        'for x, c in cnt.items()': lambda S, B, ret: ('高度枚举完毕，去 `cnt_pair` 里找最大值' if 'x' in B and S.x == B.x else f'枚举高度 `x = {S.x}`（`{S.c}` 块）'),
        'for y, c2 in cnt.items()': lambda S, B, ret: ('和 `x = %d` 配对的高度都枚举完了' % S.x if 'y' in B and S.y == B.y else f'再枚举另一种高度 `y = {S.y}`（`{S.c2}` 块）'),
        'if y > x': lambda S, B, ret: (f'`y = {S.y} > x = {S.x}`：这一对还没统计过 → 合成' if S.y > S.x
                                      else f'`y = {S.y} <= x = {S.x}`：跳过，避免 `x+y` 和 `y+x` 重复统计'),
        'cnt_pair[x + y]': '`{x}` 与 `{y}` 各有 `{c}`、`{c2}` 块，最多配 `min({c}, {c2}) = {min(c, c2)}` 对 → `cnt_pair[{x + y}] = {cnt_pair[x + y]}`',
        'return max': lambda S, B, ret: (f'`cnt_pair` 里最大的是高度 `{max(S.cnt_pair, key=S.cnt_pair.get)}`，'
                                         f'能凑 `{ret}` 块 → 栅栏最宽 ==`{ret}`=='),
    },
    cards=dict(
        one_liner='反过来枚举木板对，用哈希表记下每个高度能新增多少块',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['`planks[i]` 是木板高度，宽度都是 1；栅栏所有木板必须同高',
                 '可以直接用原木板，或把==两块不同木板==相加成一块；每块原木板最多用一次',
                 '示例：`[1,3,2,5,7,5,4,2,1]` → `4`（凑出四块高 5）',
                 '本视频：`[1,4,2,3,3,1]` → `3`'],
        quote='反过来，枚举所有木板对，用哈希表记录高度 h = planks[i] + planks[j] 新增了多少块木板，就可以在枚举高度 h 的时候，O(1) 知道最多有多少块木板可以组成 h。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先枚举高度 h 再数能凑几块，是 `O(n^3)`，太慢',
              '改成枚举==高度对 (x, y)==：x、y 两种板最多凑 `min(cnt[x], cnt[y])` 块高 `x+y`',
              '同一种高度内部配对：`cnt[x] // 2` 块高 `2x`；最后答案 = `cnt[h] + cnt_pair[h]` 的最大值'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`（`n` 为 `planks` 长度）',
                 '代码把 `cnt[x]` 也直接记进了 `cnt_pair[x]`，最后一次 `max` 搞定',
                 '`y > x` 避免 `x+y`、`y+x` 重复；`x` 自己配对要单独算 `c // 2`',
                 '固定高度 h 时，x 只会和 h-x 配对，所以不同高度对不会重复占用同一种木板'],
    ),
)
