W0 = ['ab', 'ba', 'cc']
LET = list('abc')


def _sub(S):
    return S.get('sub')


def _letters(S):
    return LET


def _lcol(S, i, v):
    sub = S.get('sub')
    if sub is None:
        return None
    if S['_inner'].get('x') == i and 'color' in S['_inner']:
        return 'yellow'
    if S.get('mask2', 0) >> i & 1:
        return 'orange'
    if sub >> i & 1:
        return 'green'
    return 'orange' if S.get('mask1') is not None and (S['all_mask'] >> i & 1) else None


def _gtxt(S):
    if 'g' not in S:
        return '每个字符串 `xy` 是一条约束：x 必须在 y 左边 → 有向边 x → y'
    return '边（x 必须在 y 左边）：' + '，'.join(f"{LET[x]}→{LET[y]}" for x in sorted(S['g']) for y in S['g'][x]) if S['g'] else ''


def _stxt(S):
    sub = S.get('sub')
    if sub is None:
        return ''
    one = ''.join(LET[i] for i in range(3) if (S['all_mask'] >> i & 1) and (sub >> i & 1))
    two = ''.join(LET[i] for i in range(3) if (S['all_mask'] >> i & 1) and not (sub >> i & 1))
    return f"当前 `sub = {sub:03b}`：出现 ==1 次== 的字母 `{one or '无'}`；出现 ==2 次== 的字母 `{two or '无'}`（放在最左和最右）"


CONFIG = dict(
    num=3435, title='最短公共超序列的字母出现频率', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='枚举子集 + 有向图判环',
    tags=['难度分 3028'],
    code='''
class Solution:
    def supersequences(self, words: List[str]) -> List[List[int]]:
        # 收集有哪些字母，同时建图
        all_mask = mask2 = 0
        g = defaultdict(list)
        for x, y in words:
            x, y = ord(x) - ord('a'), ord(y) - ord('a')
            all_mask |= 1 << x | 1 << y
            if x == y:
                mask2 |= 1 << x
            g[x].append(y)

        # 判断是否有环
        def has_cycle(sub: int) -> bool:
            color = [0] * 26

            def dfs(x: int) -> bool:
                color[x] = 1
                for y in g[x]:
                    # 只遍历在 sub 中的字母
                    if (sub >> y & 1) == 0:
                        continue
                    if color[y] == 1 or color[y] == 0 and dfs(y):
                        return True
                color[x] = 2
                return False

            for i, c in enumerate(color):
                # 只遍历在 sub 中的字母
                if c == 0 and sub >> i & 1 and dfs(i):
                    return True
            return False

        st = set()
        max_size = 0
        # 枚举 mask1 的所有子集 sub
        sub = mask1 = all_mask ^ mask2
        while True:
            size = sub.bit_count()
            # 剪枝：如果 size < max_size 就不需要判断了
            if size >= max_size and not has_cycle(sub):
                if size > max_size:
                    max_size = size
                    st.clear()
                st.add(sub)
            sub = (sub - 1) & mask1
            if sub == mask1:
                break

        return [[(all_mask >> i & 1) + ((all_mask ^ sub) >> i & 1) for i in range(26)]
                for sub in st]
''',
    call=f'Solution().supersequences({W0!r})',
    expect=[[1, 2, 2] + [0] * 23, [2, 1, 2] + [0] * 23],
    views=[
        dict(type='array', var=_letters, label='字母（橙 = 出现 2 次，绿 = 出现 1 次，黄 = DFS 正在访问）', cell=100, h=170,
             color=_lcol),
        dict(type='text', h=90, size=28, fn=_gtxt),
        dict(type='text', h=100, size=28, fn=_stxt),
        dict(type='set', var='st', label='st（目前最优的 sub，二进制位表示出现 1 次的字母）', fmt=lambda x: f'{x:03b}', h=110),
        dict(type='calls', h=150, hide=('words',)),
    ],
    watch=[('all_mask', 'all_mask', 'cyan'), ('mask2', 'mask2', 'orange'), ('sub', 'sub', 'pink'), ('max_size', 'max_size', 'green')],
    skip=['all_mask |=', 'x, y = ord', 'g[x].append', 'for x, y in words', 'size = sub.bit_count', 'color = [0] * 26', 'def dfs', 'def has_cycle',
          'for i, c in enumerate', 30, 51],
    max_steps=130,
    captions={
        'all_mask = mask2 = 0': '`all_mask` 记有哪些字母，`mask2` 记必须出现 2 次的字母（`xx` 型），`g` 是约束图',
        'if x == y': lambda S, B, r: (f'`{LET[S.x]}{LET[S.y]}`：`s[0] == s[1]` → 字母 `{LET[S.x]}` 必须出现 2 次，记入 `mask2`' if S.x == S.y else f'`{LET[S.x]}{LET[S.y]}`：x ≠ y，只建边 `{LET[S.x]} → {LET[S.y]}`'),
        'sub = mask1 = all_mask ^ mask2': '`mask1`：可以出现 1 次的字母。枚举 `mask1` 的所有子集 `sub` = 出现 1 次的字母集合，其余出现 2 次',
        'if size >= max_size': lambda S, B, r: (f'`sub = {S.sub:03b}` 有 `{S.size}` 个字母出现 1 次，`max_size = {S.max_size}`；'
                                                + ('不小于 max_size → 调用 has_cycle 判环' if S.size >= S.max_size else '比 max_size 小 → 剪枝')),
        'color[x] = 1': '外层循环对 sub 中没访问过的字母调用 `dfs({x})`（字母 `{LET[x]}`）：先标成 1 = 正在访问',
        'for y in g[x]': '看 `{LET[x]}` 的出边指向的字母 y',
        'if (sub >> y & 1) == 0': lambda S, B, r: (f'`{LET[S.y]}` 不在 sub 中（出现 2 次，放两端已满足）→ 这条约束不用管' if (S.sub >> S.y & 1) == 0
                                                   else f'`{LET[S.y]}` 在 sub 中（只出现 1 次）→ 这条约束要考虑'),
        'if color[y] == 1': lambda S, B, r: (f'`color[{LET[S.y]}] = 1`：回到了正在访问的字母 → ==有环==，`{LET[S.x]}` 与 `{LET[S.y]}` 互相要求在左边' if S.color[S.y] == 1
                                             else f'`color[{LET[S.y]}] = {S.color[S.y]}`：' + ('没访问过，递归 dfs' if S.color[S.y] == 0 else '已处理完，没有环')),
        'color[x] = 2': '`{LET[x]}` 的所有后继都访问完，没有发现环 → 标成 2',
        'return False': lambda S, B, r: ('这个字母处理完，没有环' if S['_line'] == 26 else '每个起点都查完，这个 sub 里没有环 → 字母可以各出现一次地排好'),
        'return True': '发现环 → 逐层返回 True：这个 sub 不合法（这些字母不可能各只出现 1 次）',
        'if size > max_size': lambda S, B, r: (f'`sub` 合法，且 `size = {S.size}` > `max_size = {S.max_size}` → 之前的最优作废，要清空 `st`' if S.size > S.max_size
                                               else f'`sub` 合法，`size = {S.size}` 与 `max_size = {S.max_size}` 一样大 → 不用清空，直接并列加入'),
        'st.clear()': '清空旧的最优集合',
        'st.add(sub)': '`sub = {sub:03b}` 合法 → 加入 `st`；出现 1 次的字母越多，超序列越短',
        'max_size = size': '更新 `max_size = {size}`',
        'sub = (sub - 1) & mask1': '枚举下一个子集：`(sub-1) & mask1`',
        'if sub == mask1': lambda S, B, r: ('绕回 `mask1`，所有子集枚举完 → break' if S.sub == S.mask1 else '还没枚举完，继续'),
        'return [[': '每个 `sub` 生成一行频率：出现 1 次的字母 `1`，其余 `2`，共 `{len(st)}` 个答案',
    },
    cards=dict(
        one_liner='每个字母最多出现 2 次：枚举谁只出现 1 次，无环才合法',
        complexity='时间 `O(m·2^k)`，空间 `O(2^k)`',
        problem=['`words` 里每个字符串长度为 2，求所有最短公共超序列的字母频率（互为排列的只算一个）',
                 '`["ab","ba"]` → 超序列 `aba`、`bab`',
                 f'本视频：`words = {W0}`'],
        quote='每个字母在公共超序列中的出现次数要么是 1，要么是 2。',
        quote_src='—— 灵茶山艾府题解',
        idea=['出现 2 次的字母放最左和最右，所有含它的字符串都满足',
              '只出现 1 次的字母：`xy` 变成约束“x 在 y 左边” → ==有向图不能有环==',
              '枚举哪些字母出现 1 次（子集），无环则合法；1 次越多越短'],
        summary=['时间 `O(m·2^k)`，`k ≤ 16`；空间 `O(2^k)`',
                 '`xx` 型字符串的字母必须出现 2 次，直接放进 `mask2`，不参与枚举',
                 '判环只看 `sub` 内的字母；用三色标记法（0/1/2）',
                 '`int.bit_count` 需要 Python 3.10+；原文还有“枚举出现 2 次的字母”的未优化写法，思路相同'],
    ),
)
