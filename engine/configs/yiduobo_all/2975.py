_st = set()


def _reset(S, B, r):
    _st.clear()
    return f'把外框 `1` 和 `{S.bound}` 也算进来并排序 → `{S.fences}`'


def _add(S, B, r):
    _st.add((S.i, S.j))
    return f'长度 `{S.fences[S.j]} − {S.fences[S.i]} = {S.fences[S.j] - S.fences[S.i]}` 加入集合 → `{sorted(S.length_set)}`'


def _forj(S, B, r):
    if (S.i, S.j) in _st or S.get('j') is None:
        return '这个起点的终点枚举完了'
    return f'`j = {S.j}`：终点 `fences[{S.j}] = {S.fences[S.j]}`（中间的栏杆都拆掉）'


CONFIG = dict(
    num=2975, title='移除栅栏得到的正方形田地的最大面积', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='枚举栏杆对 · 集合求交',
    tags=[],
    code='''
class Solution(object):
    def maximizeSquareArea(self, m, n, hFences, vFences):

        def generate(fences, bound):
            fences = [1] + sorted(fences) + [bound]
            length_set = set()
            for i in range(len(fences) - 1):
                for j in range(i + 1, len(fences)):
                    length_set.add(fences[j] - fences[i])
            return length_set

        h_set = generate(hFences, m)
        v_set = generate(vFences, n)

        res = -1
        for x in h_set:
            if x in v_set:
                res = max(res, x * x)
        
        if res > 0:
            res %= 10 ** 9 + 7
        return res
''',
    call='Solution().maximizeSquareArea(7, 6, [2,4], [3])',
    expect=25,
    views=[
        dict(type='text', size=26, fn=lambda S: (f"枚举栏杆对：`fences[{S['j']}] − fences[{S['i']}] = {S['fences'][S['j']] - S['fences'][S['i']]}`" if 'fences' in S and 'j' in S and 'i' in S and 'length_set' in S and 'h_set' not in S
                                                  else (f"当前 `x = {S['x']}`，`res = {S['res']}`" if 'x' in S and 'res' in S else '横竖分开：先收集每个方向上所有连续空白的长度'))),
        dict(type='array', var='fences', label='fences（含外框 1 和边界）', pointers={'i': 'blue', 'j': 'pink'}, cell=84, h=190),
        dict(type='set', var='length_set', label='length_set（当前方向）', fmt=lambda x: str(x), h=170),
        dict(type='set', var='h_set', label='h_set', fmt=lambda x: str(x), h=130),
        dict(type='set', var='v_set', label='v_set', fmt=lambda x: str(x), h=130),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('x', 'x', 'yellow'), ('res', 'res', 'green')],
    captions={
        'fences = [1] + sorted': _reset,
        'length_set = set()': '`length_set` 收集这个方向所有可能的空白长度',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：以 `fences[{S.i}] = {S.fences[S.i]}` 为起点' if S.get('i') != B.get('i') else '所有起点都枚举完了'),
        'for j in range': _forj,
        'length_set.add': _add,
        'return length_set': '这个方向的可用长度：==`{sorted(length_set)}`==',
        'h_set = generate': '水平方向 `h_set = {sorted(h_set)}`',
        'v_set = generate': '竖直方向 `v_set = {sorted(v_set)}`',
        'res = -1': '`res = -1`：先假设拼不出正方形',
        'for x in h_set': '`x = {x}`：水平方向有这个长度',
        'if x in v_set': lambda S, B, r: (f'`{S.x}` 在 `v_set` 中 → 两个方向都能得到，可以拼成边长 {S.x} 的正方形' if S.x in S.v_set else f'`{S.x}` 不在 `v_set` 中 → 竖直方向拼不出，跳过'),
        'res = max(res, x * x)': '`res = max({B.res}, {x}²)` = =={res}==',
        'if res > 0': lambda S, B, r: ('`res > 0`：找到了正方形，需要取模' if S.res > 0 else '`res = -1`：没有公共长度，原样返回'),
        'res %= ': '取模：`res` = =={res}==',
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='水平竖直互不影响：收集各自的空白长度，找最大公共值',
        complexity='时间 `O(h² + v²)`，空间 `O(h² + v²)`',
        problem=['空白网格上有一些横杠和竖杠，外框不能移除',
                 '移除一些杠之后，求能得到的最大正方形面积（对 `10^9+7` 取模），没有则返回 `-1`',
                 '本视频：`m=7, n=6, hFences=[2,4], vFences=[3]` → `25`'],
        quote='水平和竖直方向也是互不影响的，因此可以分别找出水平和竖直方向上所有可以得到的连续空白值，然后找出最大的在两个方向上都出现过的连续空白值即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['和 2943 题很像：单方向的空白值 = 枚举所有横杠（或竖杠）对的差',
              '注意外框 `1` 和 `m`（或 `n`）也可以当端点',
              '遍历 `h_set`，凡是也在 `v_set` 里的 `x`，用 `x*x` 更新答案'],
        summary=['时间 `O(h² + v²)`，空间 `O(h² + v²)`',
                 '外框也要加入杠的列表，否则会漏掉长边',
                 '`res` 初值 `-1`，只有 `res > 0` 才取模',
                 '原文本身已是 Python 3 可运行的写法，未做修改',
                 '对比灵神：灵神用集合交集 `h_set & v_set` 一步取最大；这里是遍历集合逐个判断'],
    ),
)
