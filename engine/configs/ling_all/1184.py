def _win(S):
    s, t = S.get('s'), S.get('t')
    if s is None or t is None or s > t:
        return None
    return (s, t - 1) if t > s else None


def _color(S, i, v):
    s, t = S.get('s'), S.get('t')
    if s is None or t is None or s > t:
        return None
    return 'green' if s <= i < t else 'orange'


def _text(S):
    if 'd1' not in S:
        return '环形：从 s 到 t 只有两条路，顺时针 d1，逆时针 = 总和 − d1'
    d1, tot = S['d1'], sum(S['distance'])
    return f'绿色段 `d1 = {d1}`，橙色段 `sum − d1 = {tot} − {d1} = {tot - d1}`'


CONFIG = dict(
    num=1184, title='公交站间的距离', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='切片求和 · 总和减去另一半',
    code='''
class Solution:
    def distanceBetweenBusStops(self, distance: List[int], s: int, t: int) -> int:
        if s > t:
            s, t = t, s
        d1 = sum(distance[s: t])
        return min(d1, sum(distance) - d1)
''',
    call='Solution().distanceBetweenBusStops([1,2,3,4,5,6], 5, 1)',
    expect=7,
    views=[
        dict(type='text', fn=_text, h=70, size=28),
        dict(type='array', var='distance', label='distance[i]：站 i 到站 i+1 的距离（绿 = s→t 顺时针段，橙 = 另一边）',
             cell=96, color=_color, window=('s', 't-1'), pointers={'s': 'blue', 't': 'pink'}, h=260),
    ],
    watch=[('s', 's', 'blue'), ('t', 't', 'pink'), ('d1', 'd1', 'green'), ('总和', 'sum(distance)', 'yellow')],
    captions={
        'if s > t': lambda S, B, r: (f'`s = {S.s} > t = {S.t}`：不妨设 s ≤ t，==交换==两者' if B.s > B.t
                                     else f'`s = {S.s} ≤ t = {S.t}`，不用交换'),
        's, t = t, s': '交换后 `s = {s}`，`t = {t}`：顺时针走 `s, s+1, ..., t`',
        'd1 = sum': '`d1` = `distance[{s}: {t}]` 之和 = ==顺时针距离== `{d1}`',
        'return min': '逆时针 = 总和 − d1 = `{sum(distance)} − {d1} = {sum(distance) - d1}`，取较小值 → ==`{ret}`==',
    },
    cards=dict(
        one_liner='两个方向之和等于一圈：算出一个，另一个用总和减',
        complexity='时间 `O(n)`，空间 `O(1)`（忽略切片空间）',
        problem=['环形公交线路，`distance[i]` 是站 `i` 到站 `(i+1)%n` 的距离',
                 '求 `start` 到 `destination` 的最短距离（可顺可逆）',
                 '示例：`[1,2,3,4]`，0 → 2，答案 `3`',
                 '本视频：`[1,2,3,4,5,6]`，5 → 1 → `7`'],
        quote='不妨设 s≤t（如果 s>t 则交换 s 和 t）。……d2 也等于 distance 的元素和减去 d1。二者取最小值，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先交换让 `s ≤ t`，顺时针就是 `s → t` 这一段',
              '`d1 = sum(distance[s:t])`',
              '逆时针绕过了剩下所有边，等于 `sum(distance) − d1`，取 `min`'],
        summary=['时间 `O(n)`，空间 `O(1)`（忽略切片空间）',
                 '易错：切片 `distance[s:t]` 不含 `t`，正好是 `t − s` 条边',
                 '写法二：`min(sum(distance[s:t]), sum(distance[:s]) + sum(distance[t:]))`，直接算两段',
                 '思考题：多次询问时用前缀和，每次 `O(1)`'],
    ),
)
