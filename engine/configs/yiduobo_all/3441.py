S0 = 'bdacebd'


def _c_color(S, k, v):
    if isinstance(S.get('res'), str) and S.get('_line', 0) >= 66:
        return 'green' if k < len(S['res']) else None
    idx = S.get('index')
    cl = S.get('char_list')
    if idx is not None and cl and S.get('_line', 0) in (33, 35, 42, 44, 51, 53):
        return 'yellow' if idx <= k < idx + len(cl) else None
    if idx is not None and k == idx:
        return 'blue'
    return None


def _hl(S, k, v):
    idx = S.get('index')
    return 'blue' if idx is not None and k == idx and S.get('_line', 0) < 66 else None


def _better(S):
    bc, c, s, bs = S['best_cost'], S['cost'], S['s'], S['best_s']
    return bc is None or c < bc or (c == bc and s < bs)


def _cmp(S, B, ret):
    n = S.n
    seg = len(S.char_list)
    head = f"候选：首段 `{''.join(S.char_list)}` 全变成 `{S.s[0]}`，总代价 `{S.cost}`，比较串 `{S.s}`。"
    if S.best_cost is None:
        return head + '这是第一个候选 → ==采用=='
    if S.cost < S.best_cost:
        return head + f'代价 `{S.cost}` < 当前最优 `{S.best_cost}` → ==采用=='
    if S.cost == S.best_cost:
        if S.s < S.best_s:
            return head + f'代价相同，串 `{S.s}` < `{S.best_s}`，字典序更小 → ==采用=='
        return head + f'代价相同，但串 `{S.s}` ≥ `{S.best_s}` → 不换'
    return head + f'代价 `{S.cost}` > 当前最优 `{S.best_cost}` → 不换'


def _cost(S, B, ret):
    cl = S.char_list
    k = len(cl)
    mid = cl[(k - 1) // 2]
    calc = sum(abs(ord(c) - ord(mid)) for c in cl)
    fv = S.f[S.index + k]
    return (f"`caption[{S.index}:{S.index + k}]` 排序得 `{''.join(cl)}`，中位数 `{mid}`，`calc` = {calc}，"
            f"再加 `f[{S.index + k}]` = {fv} → `cost` = =={calc + fv}==")


CONFIG = dict(
    num=3441, title='变成好标题的最少代价', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='划分型 DP · 中位数 · 倒推记录 fill / nxt',
    tags=['灵神题单·动态规划', '灵神题单·贪心与思维', '难度分 2765'],
    code='''
class Solution(object):
    def minCostGoodCaption(self, caption):
        
        if len(caption) < 3:
            return ''
        
        n = len(caption)
        f = [None] * (n + 1)
        fill = [None] * (n + 1)
        nxt = [None] * (n + 1)

        f[n] = 0
        fill[n] = '@'

        def calc(char_list):
            m = len(char_list)
            mid = (m - 1) // 2
            target = char_list[mid]
            cost = 0
            for index in range(mid):
                cost += ord(char_list[mid]) - ord(char_list[index])
            for index in range(mid + 1, m):
                cost += ord(char_list[index]) - ord(char_list[mid])
            return cost

        for index in range(n - 3, -1, -1):
            best_cost = None
            best_nxt = None
            best_s = ""

            if index + 3 <= n and f[index + 3] is not None:
                char_list = sorted(list(caption[index: index + 3]))
                cost = f[index + 3] + calc(char_list)
                s = char_list[1] * 3 + fill[index + 3] * 3
                if best_cost is None or cost < best_cost or (cost == best_cost and s < best_s):
                    best_cost = cost
                    best_nxt = index + 3
                    best_s = s
            
            if index + 4 <= n and f[index + 4] is not None:
                char_list = sorted(list(caption[index: index + 4]))
                cost = f[index + 4] + calc(char_list)
                s = char_list[1] * 4 + fill[index + 4] * 3
                if best_cost is None or cost < best_cost or (cost == best_cost and s < best_s):
                    best_cost = cost
                    best_nxt = index + 4
                    best_s = s
            
            if index + 5 <= n and f[index + 5] is not None:
                char_list = sorted(list(caption[index: index + 5]))
                cost = f[index + 5] + calc(char_list)
                s = char_list[2] * 5 + fill[index + 5] * 3
                if best_cost is None or cost < best_cost or (cost == best_cost and s < best_s):
                    best_cost = cost
                    best_nxt = index + 5
                    best_s = s
            
            if best_cost is not None:
                f[index] = best_cost
                nxt[index] = best_nxt
                fill[index] = best_s[0]
        
        res = ""
        index = 0
        while index != n:
            res += fill[index] * (nxt[index] - index)
            index = nxt[index]
        
        return res
''',
    call=f'Solution().minCostGoodCaption({S0!r})',
    expect='bbbbddd',
    skip=[4, 9, 10, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 27, 28, 29, 31, 32, 34, 36, 37, 38,
          40, 41, 43, 45, 46, 47, 49, 50, 52, 54, 55, 56, 58, 59, 60, 63, 64, 65, 67],
    max_steps=100,
    views=[
        dict(type='string', var='caption', label='caption（黄 = 当前候选的首段；绿 = 已还原的答案）', h=170, cell=80, color=_c_color),
        dict(type='array', var='f', label='f[i]：caption[i:] 变成好标题的最少操作（· = 无解）', h=150, cell=80, color=_hl),
        dict(type='array', var='fill', label='fill[i]：f[i] 最优时 caption[i] 变成的字母', h=150, cell=80, color=_hl),
        dict(type='array', var='nxt', label='nxt[i]：首段结束后，下一段从哪里开始', h=150, cell=80, color=_hl),
    ],
    watch=[('index', 'index', 'blue'), ('cost', 'cost', 'yellow'), ('best_cost', 'best_cost', 'green'), ('best_s', 'best_s', 'cyan'), ('res', 'res', 'green')],
    captions={
        'n = len(caption)': '`n = {n}`。长度 ≥ 3，一定有解（全改成同一个字母即可）',
        'f = [None]': '`f[i]`：把 `caption[i:]` 变成好标题的最少操作；`fill[i]`：此时首字符变成什么；`nxt[i]`：下一段起点。`f[n] = 0`，其余 `None` = 还没有',
        'for index in range': lambda S, B, ret: (f'`index = {S.index}`：倒着算 `caption[{S.index}:]`，枚举首段长度 3 / 4 / 5' if S.get('index') != B.get('index') or 'index' not in B else '倒推结束'),
        'cost = f[index + 3]': _cost,
        'cost = f[index + 4]': _cost,
        'cost = f[index + 5]': _cost,
        'if best_cost is None': _cmp,
        'fill[index] = best_s[0]': '记下最优：`f[{index}] = {f[index]}`，`nxt[{index}] = {nxt[index]}`（首段长 {nxt[index] - index}），`fill[{index}] = {fill[index]}`',
        'res += fill[index]': lambda S, B, ret: f'从 `index = {B.index}` 起这一段长 `{B.nxt[B.index] - B.index}`，全是 `{B.fill[B.index]}` → `res = {S.res}`；下一段从 `nxt[{B.index}]` = {B.nxt[B.index]} 开始',
        'return res': '答案 `{ret}`',
    },
    cards=dict(
        one_liner='段长只用 3/4/5，段内全变中位数；倒着推才好比字典序',
        complexity='时间 `O(n)`（排序的长度只有 3~5），空间 `O(n)`',
        problem=['每个字符都在连续出现 ≥ 3 次的组里，就是==好标题==',
                 '每次操作把一个字母改成相邻字母，求最少操作数；有多种方案取字典序最小；无解返回空串',
                 '示例：`"cdcd"` → `"cccc"`；本视频：`"bdacebd"` → `"bbbbddd"`'],
        quote='对于p的选择，index - p的大小就不应该大于等于6，因为所有长度大于等于6的组都可以至少拆分出一个长度为3的组出去……p只需考虑index - 2、index - 3、index - 4这三个位置就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想正着的划分 DP：`f[index] = min(f[p-1] + cost(p, index))`，`O(n^2)`',
              '长 ≥ 6 的组一定能拆开，所以最后一段只需看长 3/4/5；段内变成==中位数==最省',
              '要字典序最小就==倒着推==：`fill[index]` 记首字母，`nxt[index]` 记下一段，比较只看前 6 个字符'],
        result='倒推完成，沿 `nxt` 拼出 `"bbbb" + "ddd"` → `"bbbbddd"` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`f[index + k]` 是 `None`（后面凑不成段）时，这个候选直接跳过',
                 '比较串 = 首段字符重复 + 后一段首字符 ×3，只比较前 6 个字符就够了',
                 '原文本身可在 Python 3 运行，未修改（整数除法已是 `//`）'],
    ),
)
