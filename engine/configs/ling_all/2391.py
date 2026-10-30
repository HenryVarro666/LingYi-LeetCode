def _i(S):
    if 'g' not in S or 't' not in S:
        return None
    G, T = S['garbage'], S['travel']
    for i in range(1, len(G)):
        if G[i] == S['g'] and T[i - 1] == S['t']:
            return i
    return None


def _txt(S):
    if 'seen' not in S:
        return '从最后一栋房子往回走：路段 `travel[i-1]` 要被 ==「i 号房及之后出现过的垃圾种类数」== 辆车走一遍'
    k = len(S['seen'])
    if 'g' in S and 't' in S and S['_line'] >= 7:
        return f"`travel` 这一段 `{S['t']}` × 种类数 `{k}` = =={S['t'] * k}==；加上本房垃圾 `{len(S['g'])}` 个"
    return f"之后出现过的垃圾种类 `seen = {sorted(S['seen'])}`，共 `{k}` 种"


CONFIG = dict(
    num=2391, title='收集垃圾的最少总时间', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='倒序一次遍历 · 贡献法',
    tags=[],
    code='''
class Solution:
    def garbageCollection(self, garbage: List[str], travel: List[int]) -> int:
        ans = len(garbage[0])
        seen = set()
        for g, t in zip(reversed(garbage), reversed(travel)):
            seen.update(g)
            ans += len(g) + t * len(seen)
        return ans
''',
    call='Solution().garbageCollection(["G", "P", "GP", "GG"], [2, 4, 3])',
    expect=21,
    views=[
        dict(type='array', var='garbage', label='garbage（每栋房子的垃圾）', cell=110, h=190,
             color=lambda S, i, v: 'blue' if i == _i(S) else None),
        dict(type='array', var='travel', label='travel（travel[i-1] = 房子 i-1 到 i 的路程）', cell=110, h=190,
             color=lambda S, i, v: 'pink' if _i(S) is not None and i == _i(S) - 1 else None),
        dict(type='set', var='seen', label='seen（从当前房子往后出现过的垃圾种类 = 需要走到这里的车数）', fmt=lambda x: str(x), h=130),
        dict(type='text', fn=_txt, size=26, h=100),
    ],
    watch=[('g', 'g', 'blue'), ('t', 't', 'pink'), ('len(seen)', 'len(seen)', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = len(garbage[0])': '房子 0 的垃圾只用收、==不用走路==：先加上 `len(garbage[0]) = {ans}`',
        'seen = set()': '`seen` 记录往后出现过的垃圾种类（最多 M、P、G 三种）',
        'for g, t in zip': lambda S, B, ret: ('倒序遍历结束' if 'g' in B and S.g == B.g and S.t == B.t
                                              else f'倒着走：房子 `{S.g!r}`，它前面的路段 `travel = {S.t}`'),
        'seen.update(g)': '把 `{g!r}` 里的种类加入 → `seen = {sorted(seen)}`',
        'ans += len(g)': '每个垃圾收 1 分钟：`+{len(g)}`；这段路 `{t}` 分钟，要走的车 = `len(seen) = {len(seen)}` 辆：`+{t * len(seen)}` → ans = =={ans}==',
        'return ans': '收集用时 + 各车行驶用时 = ==`{ans}`==',
    },
    cards=dict(
        one_liner='倒着看：每段路要走几辆车，就是后面出现过几种垃圾',
        complexity='时间 `O(n+L)`，空间 `O(1)`（哈希集合最多 3 个元素）',
        problem=['三辆车分别收 `M`、`P`、`G`，同一时刻只有一辆在工作',
                 '每收一个垃圾 1 分钟；`travel[i]` 是房子 i 到 i+1 的路程',
                 '车不必走完全程，求收完所有垃圾的最少总分钟数',
                 '示例：`["G","P","GP","GG"], [2,4,3]` → `21`'],
        quote='如果从 garbage[i] 到 garbage[n-1] 有 k 种字母，那么 travel[i-1] 对答案的贡献是 travel[i-1]·k。',
        quote_src='—— 灵茶山艾府题解（方法三：倒序一次遍历）',
        idea=['同一时刻只有一辆车在动 → ==总时间 = 收集时间 + 各车行驶时间==',
              '收集时间 = 所有字符串长度之和，行驶时间看每段路被几辆车走',
              '从后往前扫，`seen` 里有几种字母，这段路就被几辆车走'],
        result='收集 6 + 行驶 15 = 21 ✓',
        summary=['时间 `O(n+L)`，空间 `O(1)`',
                 '易错：`travel` 下标比 `garbage` 少 1；用 `zip` 倒序会自动少配最后一个，所以房子 0 要单独先加',
                 '方法一：先让每辆车跑满全程，再倒着扣掉多跑的路；方法二：正序用哈希表记每辆车最后到过的位置',
                 '三种写法都是 `O(n+L)`，贡献法最省空间'],
    ),
)
