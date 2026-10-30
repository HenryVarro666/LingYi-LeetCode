def _txt(S):
    if 'cut_pos' not in S or 'index' not in S:
        return ''
    a, b = S['cut_pos'] - 1, S['index']
    return f'最后一段 `word1[{a}:{b}]` = `{S["word1"][a:b]}` → 目标 `{S["word2"][a:b]}`'


CONFIG = dict(
    num=3579, title='字符串转换需要的最小操作数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='划分 DP + 枚举最后一段 + 字符对配对',
    tags=['灵神题单·动态规划', '灵神题单·字符串', '难度分 2493'],
    code='''
class Solution(object):
    def minOperations(self, word1, word2):
        
        def calc(s1, s2):
            pair = {}
            cnt = 0
            for c1, c2 in zip(s1, s2):
                if c1 == c2:
                    continue
                cnt += 1
                if pair.get((c2, c1), 0) > 0:
                    pair[(c2, c1)] -= 1
                    cnt -= 1
                else:
                    pair[(c1, c2)] = pair.get((c1, c2), 0) + 1
            
            return cnt

        n = len(word1)
        f = [0]
        for index in range(1, n + 1):
            f.append(None)
            for cut_pos in range(1, index + 1):
                s1 = word1[cut_pos - 1: index]
                rev_s1 = word1[cut_pos - 1: index][::-1]
                s2 = word2[cut_pos - 1: index]
                cost = min(calc(s1, s2), calc(rev_s1, s2) + 1)
                if f[-1] is None or f[-1] > cost + f[cut_pos - 1]:
                    f[-1] = cost + f[cut_pos - 1]

        return f[-1]
''',
    call='Solution().minOperations("abc", "bad")',
    expect=2,
    max_steps=80,
    skip=['n = len(word1)', 'f.append(None)', 'rev_s1 =', 'cnt = 0', 'for c1, c2 in zip', 'return cnt', 'continue', 'cnt += 1', 'pair[(c2, c1)] -= 1', 'cnt -= 1', 'pair = {}', 'if c1 == c2', 's1 = word1', 's2 = word2', 'pair[(c1, c2)] = '],
    views=[
        dict(type='string', var='word1', label='word1', h=150, cell=60,
             pointers={'cut_pos - 1 if 0 < cut_pos <= index else None': 'blue', 'index - 1 if index else None': 'pink'},
             pointer_labels={'cut_pos - 1 if 0 < cut_pos <= index else None': '段首', 'index - 1 if index else None': '段尾'},
             window=('cut_pos - 1', 'index - 1')),
        dict(type='string', var='word2', label='word2', h=110, cell=60, index=False,
             window=('cut_pos - 1', 'index - 1')),
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='array', var='f', label='f[index] = word1 前 index 个字符的最少操作数（None = 待算）', h=130, cell=60,
             color=lambda S, k, v: 'yellow' if k == len(S['f']) - 1 and S.get('_line', 0) >= 25 else None),
        dict(type='map', var='pair', label='pair：还没配上的字符对 (c1, c2) 的个数', h=130,
             fmt=lambda k, v: f'{k[0]}→{k[1]}：{v}' if isinstance(k, tuple) else f'{k}：{v}'),
    ],
    watch=[('index', 'index', 'pink'), ('cut_pos', 'cut_pos', 'blue'), ('cnt', 'cnt', 'green'), ('cost', 'cost', 'orange')],
    captions={
        'def calc': '`calc(s1, s2)` 算把 `s1` 变成 `s2` 至少几次（只用替换+交换）',
        'f = [0]': '`f[0] = 0`：空前缀不用操作',
        'for index in range': lambda S, B, r: (f'`index = {S.index}`：算前 {S.index} 个字符，先枚举最后一段的起点 `cut_pos`' if S.index != B.get('index') else '全部前缀算完'),
        'for cut_pos in range': lambda S, B, r: (f'`cut_pos = {S.cut_pos}`：最后一段是 `word1[{S.cut_pos - 1}:{S.index}]`' if not (S.cut_pos == B.get('cut_pos') and S.cut_pos == S.index) else '`cut_pos` 枚举完毕'),
        's1 = word1': '不反转的这一段 `s1 = "{s1}"`',
        's2 = word2': '目标这一段 `s2 = "{s2}"`',
        'pair = {}': '`calc("{s1}", "{s2}")`：一趟遍历，字符对不同就先记 1 次操作，遇到反向对就换成一次交换',
        'cost = min(calc(s1, s2)': '`cost = min(calc(s1, s2), calc(反转 s1, s2) + 1)`：`s1 = "{s1}"`，`s2 = "{s2}"`，分别算不反转、反转两种',
        'if c1 == c2': lambda S, B, r: (f'`{S.c1} == {S.c2}`：已经一致，不用操作' if S.c1 == S.c2 else f'`({S.c1}, {S.c2})` 不同，这一对位置至少要 1 次操作'),
        'if pair.get': lambda S, B, r: (f'`({S.c1}, {S.c2})` 不同；`pair` 里已有 `({S.c2}, {S.c1})` 在等 → ==这两个位置交换一次即可==，一次交换抵两次替换，`cnt` 回退为 {S.cnt - 1}' if S.pair.get((S.c2, S.c1), 0) > 0
                                       else f'`({S.c1}, {S.c2})` 不同；没有反向的 `({S.c2}, {S.c1})`：先按替换算，`cnt` = {S.cnt}，并记下 `({S.c1}, {S.c2})` 等配对'),
        'pair[(c1, c2)] = ': '记下 `({c1}, {c2})`，等后面有反向对来配',
        'if f[-1] is None or': lambda S, B, r: (f'这一段 `cost = {S.cost}`；`f[{S.index}]` 还没算过 → 直接用 `{S.cost} + f[{S.cut_pos - 1}]`' if B.f[-1] is None else
                                                f'这一段 `cost = {S.cost}`：比较 `f[{S.index}] = {B.f[-1]}` 和 `cost + f[{S.cut_pos - 1}] = {S.cost + S.f[S.cut_pos - 1]}`'),
        'f[-1] = cost + f[cut_pos - 1]': '更新 `f[{index}] = {cost} + f[{cut_pos - 1}]` = =={f[-1]}==',
        'return f[-1]': '`f[{n}]` = =={ret}==',
    },
    cards=dict(
        one_liner='f[index] 枚举最后一段；每段 cost = min(不反转, 反转 + 1)',
        complexity='时间 `O(n^3)`，空间 `O(n)`',
        problem=['把 `word1` 切成若干连续子串，每段可替换、交换、反转（每个下标每种操作最多一次）',
                 '求变成 `word2` 的==最少操作数==',
                 '示例：`"abcdf" → "dacbe"` = `4`；本视频：`"abc" → "bad"` = `2`'],
        quote='本题可以视为编辑距离的变种，但是没有插入或者删除操作……可以将子串反转，然后分别计算不反转和反转时对应的cost，取二者的较小值。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[index] = min(f[cut_pos-1] + cost)`，枚举最后一段的起点',
              '`calc`：字符对 `(c1, c2)` 与之前的 `(c2, c1)` 配上 → 一次交换，否则一次替换',
              '反转的话把 `s1` 倒过来再 `calc`，结果 `+1`'],
        summary=['时间 `O(n^3)`（`n ≤ 100` 可行），空间 `O(n)`',
                 '易错：反转后要 `+1`；`cut_pos` 从 1 开始，所以切片下标要减 1',
                 '易错：配对只在字符对互为反向时成立；相同字符直接跳过',
                 '对比灵神：灵神用中心扩展预处理 `rev_op`，把复杂度降到 `O(n^2)`；这里每段现场调用 `calc`'],
    ),
)
