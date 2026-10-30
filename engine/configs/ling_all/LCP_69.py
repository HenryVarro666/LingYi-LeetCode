_CODE = '''
# (字母在二进制上的起始位置, 这个字母能选择的上限, 位掩码)
RULES = {
    'e': (0, 4, 7),
    'l': (3, 3, 3),
    'o': (5, 2, 3),
    'h': (7, 1, 1),
    't': (8, 1, 1),
    'c': (9, 1, 1),
    'd': (10, 1, 1),
}
FULL = 2012  # 0b11111011100，每个字母都选到了对应的上限

# 合并两种选择字母的方案
def merge(cur: int, add: int) -> int:
    for pos, limit, m in RULES.values():
        c1 = (cur >> pos) & m
        c2 = (add >> pos) & m
        if c1 + c2 > limit:
            return -1
        cur += c2 << pos
    return cur

class Solution:
    def Leetcode(self, words: List[str]) -> int:
        # 预处理每个单词的每种选择字母的方案所消耗的代币的最小值
        costs = []
        for word in words:
            cost = {}
            def dfs(s: str, mask: int, tot: int) -> None:
                if mask not in cost or tot < cost[mask]:
                    cost[mask] = tot
                for i, c in enumerate(s):  # 枚举选择字母的位置
                    if c not in RULES:
                        continue
                    pos, limit, m = RULES[c]
                    if (mask >> pos) & m < limit:  # 可以选字母 c
                        dfs(s[:i] + s[i + 1:], mask + (1 << pos), tot + i * (len(s) - 1 - i))
            dfs(word, 0, 0)
            costs.append(cost)

        @cache
        def dfs(i: int, mask: int) -> int:
            if i == len(words):
                return 0 if mask == FULL else inf  # inf 表示不合法，没有选完要求的字母
            res = inf
            for add, tot in costs[i].items():
                if tot >= res: continue  # 剪枝
                m = merge(mask, add)
                if m >= 0:
                    res = min(res, tot + dfs(i + 1, m))
            return res
        ans = dfs(0, 0)
        return ans if ans < inf else -1
'''

_L = _CODE.split('\n')
# 预处理 dfs 内部、merge 内部的逐行细节不单独成步（只保留入口和结果）
_HIDE = {
    'if mask not in cost or tot < cost[mask]:', 'cost[mask] = tot', 'for i, c in enumerate(s):  # 枚举选择字母的位置',
    'if c not in RULES:', 'continue', 'pos, limit, m = RULES[c]', 'if (mask >> pos) & m < limit:  # 可以选字母 c',
    'dfs(s[:i] + s[i + 1:], mask + (1 << pos), tot + i * (len(s) - 1 - i))',
    'for pos, limit, m in RULES.values():', 'c1 = (cur >> pos) & m', 'c2 = (add >> pos) & m',
    'if c1 + c2 > limit:', 'cur += c2 << pos', 'cost = {}', 'def dfs(s: str, mask: int, tot: int) -> None:',
}
_SKIP = [k for k, t in enumerate(_L) if t.strip() in _HIDE and k < 41 or t.strip() in ('for pos, limit, m in RULES.values():', 'c1 = (cur >> pos) & m', 'c2 = (add >> pos) & m', 'if c1 + c2 > limit:', 'cur += c2 << pos')]
_NAMES = [('e', 0, 7), ('l', 3, 3), ('o', 5, 3), ('h', 7, 1), ('t', 8, 1), ('c', 9, 1), ('d', 10, 1)]


def _dec(mask):
    if not isinstance(mask, int) or mask < 0:
        return '—'
    parts = [f'{ch}×{mask >> pos & m}' for ch, pos, m in _NAMES if mask >> pos & m]
    return ' '.join(parts) if parts else '（空）'


def _txt(S):
    I = S['_inner']
    if 'costs' not in S:
        return '先给每个单词预处理：取出哪些字母（用二进制「分区」计数）最少花多少代币'
    if 'i' in I and 'mask' in I and 'res' in I:
        return f"`dfs({I['i']}, mask)`：前 {I['i']} 个单词已选 ==[{_dec(I['mask'])}]==，选完后续单词的最小代价"
    if 'mask' in I and 'tot' in I:
        return f"预处理中：这个单词取出 [{_dec(I['mask'])}] 最少花 ==`{I['tot']}`=="
    return f"`costs[i]`：每个单词取出各种字母组合的最小代价（已处理 {len(S['costs'])} 个）"


def _I(S):
    return S['_inner'].get('i')


def _curcost(S):
    i = S['_inner'].get('i')
    if i is not None and 'costs' in S and i < len(S['costs']) and 'res' in S['_inner']:
        return S['costs'][i]
    return S.get('cost', {})


def _cost_fmt(k, v):
    return f'取 [{_dec(k)}] → {v}'


CONFIG = dict(
    num='LCP 69', title='Hello LeetCode!', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='状压 DP · 字母计数「分区」二进制',
    tags=['灵神题单·动态规划', '灵神题单·常用数据结构'],
    code=_CODE,
    call='Solution().Leetcode(["hold", "engineer", "cost", "level"])',
    expect=5,
    max_events=300000,
    views=[
        dict(type='text', fn=_txt, h=80),
        dict(type='array', var='words', label='words（蓝 = 第 i 个单词）', cell=150, h=300,
             pointers={_I: 'blue'}, pointer_labels={_I: 'i'}),
        dict(type='map', var=_curcost, label='当前单词：取出字母组合 → 最小代价', fmt=_cost_fmt, font=22, h=250),
        dict(type='calls', h=190),
    ],
    watch=[('i', lambda S: S['_inner'].get('i'), 'blue'),
           ('mask', lambda S: S['_inner'].get('mask'), 'purple'),
           ('tot', lambda S: S['_inner'].get('tot'), 'yellow'),
           ('res', lambda S: S['_inner'].get('res'), 'green')],
    skip=_SKIP,
    max_steps=58,
    captions={
        'costs = []': '`costs[i]` 记录第 `i` 个单词：取出每种字母组合的最小代价',
        'for word in words': lambda S, B, r: (f'预处理单词 `{S.word!r}`：单词很短（≤ 8），直接暴搜所有取字母顺序' if len(S.costs) < len(S.words)
                                              else '四个单词都预处理完了'),
        'dfs(word, 0, 0)': '暴搜 `{word!r}`：每次取一个需要的字母，代价 = 左边个数 × 右边个数，同一组合保留最小代价',
        'costs.append(cost)': '`{word!r}` 共有 `{len(cost)}` 种取法组合，最小代价存进 `costs`',
        '@cache': '预处理完毕，开始记忆化搜索：`dfs(i, mask)` 从第 `i` 个单词选，已选 `mask`',
        'return 0 if mask == FULL': lambda S, B, r: ('每个字母都选到了上限 `FULL` → 恰好凑成 `helloleetcode`，代价 0' if S.mask == FULL
                                                     else f'`mask = {S.mask}` ≠ `FULL`：字母没凑齐 → 不合法，返回 inf'),
        'if i == len(words)': lambda S, B, r: (f'`i = {S.i} == {len(S.words)}`：单词用完了' if S.i == len(S.words) else f'`i = {S.i}`：还有单词，枚举这个单词的取法'),
        'res = inf': '`res` 记录从这里开始的最小代价，初始为 inf',
        'for add, tot in costs[i].items()': lambda S, B, r: (f'枚举单词 `{S.words[S.i]!r}` 的一种取法：取出 [{_dec(S.add)}]，代价 `{S.tot}`'
                                                             if 'add' in S and S.get('_more', True) else '这个单词的取法都枚举完了'),
        'if tot >= res: continue': lambda S, B, r: (f'这种取法本身代价 `{S.tot}` ≥ 当前最优 `res` → 不可能更优，==剪枝==' if S.tot >= S.res
                                                    else f'`{S.tot} < res`：有机会更优，继续'),
        'm = merge(mask, add)': '合并已选 `mask` 与这次取法 `add`：每种字母分区相加，超过上限就返回 -1 → `m = {m}`',
        'if m >= 0': lambda S, B, r: ('合并合法（没有哪种字母超过上限）→ 进入下一个单词' if S.m >= 0 else '合并失败：某种字母选多了 → 这个取法不可用'),
        'res = min(res, tot + dfs': '`res = min(res, tot + dfs(i+1, m))` → ==`{res}`==',
        'return res': lambda S, B, r: f'`dfs({S.i}, [{_dec(S.mask)}])` = =={"inf（无解）" if S.res == inf else S.res}==',
        'return -1': '某种字母超过了上限 → 返回 -1',
        'return cur': '合并成功，返回新的 `mask`',
        'ans = dfs(0, 0)': '从第 0 个单词、什么都没选开始搜索 → `ans = {ans}`',
        'return ans if ans < inf': '`ans = {ans}`（不是 inf 就是答案）→ ==返回 {ret}==',
    },
    cards=dict(
        result='返回 `5`：只有 engineer 的最后一个 e 要付 `5×1`',
        one_liner='二进制分区计数 + 每个单词的取法打包，记忆化搜索逐个单词选',
        complexity='时间约 `O(n · 2^m · 状态数)`，空间 `O(状态数)`',
        problem=['从单词里取字母，凑出 `helloleetcode` 的 13 个字母',
                 '取一个字母的代价 = 它左边字母数 × 右边字母数',
                 '示例：`["hold","engineer","cost","level"]` → `5`'],
        quote='用位运算表示字母选择情况，由于一个字母可以选多个，因此要对二进制「分区」，每个区域表示对应字母的个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`helloleetcode` 只有 7 种字母：e×4、l×3、o×2、h/t/c/d 各 1',
              '每种字母占二进制的一段区域，区域里的数 = 已选个数，上限由 `RULES` 给出',
              '先暴搜每个单词的取法和最小代价，再 `dfs(i, mask)` 逐个单词选，`merge` 判断是否超限'],
        summary=['预处理：单词长 ≤ 8，每个单词的取法最多 `2^8` 种',
                 '`merge` 中任何一段字母数超过上限就返回 -1，表示这个组合非法',
                 '`FULL = 2012` 表示每种字母都恰好选满；没凑齐返回 inf，最后转成 -1',
                 '`if tot >= res: continue` 是剪枝：这种取法本身就不比当前最优好'],
    ),
)
