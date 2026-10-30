def _txt(S):
    if 'start_pos' in S and 'l' in S and 'r' not in S:
        return f"`l` 向右扫描，凑够 K 种不同的数：当前 `l = {S['l']}`"
    if 'start_pos' not in S or 'r' not in S or 'l' not in S:
        return '先预处理 `next_pos[i]`：同一个数下一次出现的位置' if 'next_pos' in S else ''
    return f"start_pos = {S['start_pos']}：右边界可取 `l = {S['l']}` 到 `r = {S['r']}`，共 `{S['r']} − {S['l']} + 1` = =={S['r'] - S['l'] + 1}== 个子数组　累计 `res = {S.get('res', 0)}`"


CONFIG = dict(
    num=992, title='K个不同整数的子数组', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举左端点 · 维护最小/最大右边界 l、r',
    tags=['难度分 2210'],
    code='''
class Solution(object):
    def subarraysWithKDistinct(self, A, K):

        n = len(A)
        last_pos = {A[-1] : n - 1}
        next_pos = [-1] * n
        for index in range(n - 1, -1, -1):
            if A[index] in last_pos:
                next_pos[index] = last_pos[A[index]]
            last_pos[A[index]] = index
        
        start_pos = 0
        l = -1
        n = len(A)
        cnt_dict = {}
        while l + 1 < n and len(cnt_dict) < K:
            cnt_dict[A[l + 1]] = cnt_dict.get(A[l + 1], 0) + 1
            l += 1
        
        if len(cnt_dict) < K:
            return 0

        r = l
        while r + 1 < n and A[r + 1] in cnt_dict:
            cnt_dict[A[r + 1]] += 1
            r += 1
        
        res = r - l + 1

        while start_pos + 1 < n:
            if cnt_dict[A[start_pos]] > 1:
                cnt_dict[A[start_pos]] -= 1
                l = max(l, next_pos[start_pos])
            else:
                cnt_dict.pop(A[start_pos])
                l = r + 1
                if l == n:
                    break
                cnt_dict[A[l]] = cnt_dict.get(A[l], 0) + 1
                r = l
                while r + 1 < n and A[r + 1] in cnt_dict:
                    cnt_dict[A[r + 1]] += 1
                    r += 1
            
            res += r - l + 1
            start_pos += 1
        
        return res
''',
    call='Solution().subarraysWithKDistinct([1,2,1,2,3], 2)',
    expect=7,
    views=[
        dict(type='array', var='A', label='A（蓝 = start_pos，绿 = l，粉 = r；框 = start_pos 到 r）',
             pointers={'start_pos': 'blue', 'l': 'green', 'r': 'pink'}, window=('start_pos', 'r'), h=260, cell=100),
        dict(type='array', var='next_pos', label='next_pos（同值下一次出现的下标，-1 = 没有）', h=170, cell=100),
        dict(type='map', var='cnt_dict', label='cnt_dict（窗口 start_pos..r 内各数次数）', fmt=lambda k, v: f'{k}: {v}', h=140, font=32),
        dict(type='text', h=80, size=26, fn=_txt),
    ],
    watch=[('start_pos', 'start_pos', 'blue'), ('l', 'l', 'green'), ('r', 'r', 'pink'), ('res', 'res', 'orange')],
    captions={
        'last_pos = {': '`last_pos` 记录每个数最近见到的位置，从右往左扫',
        'if A[index] in last_pos': lambda S, B, r: (f'`last_pos` 初始就含最后一个数，所以 `next_pos[{S.index}]` 记成自己（以后不会用到）' if S.index == S.n - 1 else f'`A[{S.index}] = {S.A[S.index]}` 右边出现过 → 记下下一次出现的位置' if S.A[S.index] in S.last_pos
                                                   else f'`A[{S.index}] = {S.A[S.index]}` 右边没有再出现，`next_pos` 保持 -1'),
        'next_pos[index] = last_pos': '`next_pos[{index}] = {next_pos[index]}`',
        'last_pos[A[index]] = index': '更新 `last_pos[{A[index]}] = {index}`',
        'start_pos = 0': '左边界 `start_pos = 0`；`l`（最小右边界）先设为 -1，`cnt_dict` 先空着',
        'while l + 1 < n and len': lambda S, B, r: (f'`len(cnt_dict) = {len(S.cnt_dict)} < K = {S.K}`：还没凑够 K 种，`l` 继续向右' if len(S.cnt_dict) < S.K and S.l + 1 < S.n
                                                   else f'已有 `{len(S.cnt_dict)}` 种数 = K：`l = {S.l}` 就是 start_pos 能得到的最小右边界'),
        'cnt_dict[A[l + 1]] =': '把 `A[{l + 1}]` 加入 `cnt_dict` → `{cnt_dict}`',
        'l += 1': '`l` 右移到 {l}',
        'if len(cnt_dict) < K': '凑不够 `K` 种就没有合法子数组，否则继续',
        'r = l': '`r` 从 `l` 出发，找最大右边界',
        'while r + 1 < n and A[r + 1] in': lambda S, B, r: (f'`A[{S.r + 1}] = {S.A[S.r + 1]}` 已在窗口里 → 不增加种类，`r` 还能右移' if S.r + 1 < S.n and S.A[S.r + 1] in S.cnt_dict
                                                          else '`r` 后面的数是新数（或已到末尾），`r` 到头了'),
        'cnt_dict[A[r + 1]] += 1': '`A[{r + 1}]` 次数加一 → `{cnt_dict}`',
        'r += 1': '`r` 右移到 {r}',
        'res = r - l + 1': 'start_pos = 0 的合法子数组有 `r − l + 1` = =={r - l + 1}== 个，`res = {res}`',
        'while start_pos + 1 < n': lambda S, B, r: (f'`start_pos = {S.start_pos}`：还有下一个左边界，继续' if S.start_pos + 1 < S.n else '左边界走到最后，结束'),
        'if cnt_dict[A[start_pos]] > 1': lambda S, B, r: (f'`A[{S.start_pos}] = {S.A[S.start_pos]}` 在窗口里出现 {S.cnt_dict[S.A[S.start_pos]]} 次 > 1 → 去掉它后种类数不变，`r` 不动' if S.cnt_dict[S.A[S.start_pos]] > 1
                                                        else f'`A[{S.start_pos}] = {S.A[S.start_pos]}` 只出现 1 次 → 去掉它就少一种，需要重新找 `l`'),
        'cnt_dict[A[start_pos]] -= 1': '次数减一 → `{cnt_dict}`',
        'l = max(l, next_pos': '新窗口里还得有 `A[start_pos]`，它下一次出现在 `{next_pos[start_pos]}`；若比 `l` 靠后，`l` 要挪过去 → `l = {l}`',
        'cnt_dict.pop': '`A[start_pos]` 不再出现 → 从 `cnt_dict` 删除 → `{cnt_dict}`',
        'l = r + 1': '`A[r + 1]` 一定是新数，加进来才又凑够 K 种 → `l = r + 1 = {l}`',
        'if l == n': lambda S, B, r: ('`l` 越过末尾，再也凑不够 K 种，结束' if S.l == S.n else '`l` 还在数组内，继续'),
        'cnt_dict[A[l]] =': '把 `A[{l}]` 加入 → `{cnt_dict}`',
        'r = l': '`r` 重新从 `l` 开始找最大右边界',
        'res += r - l + 1': '左边界 {start_pos + 1} 的子数组数 `{r} − {l} + 1` = =={r - l + 1}==，`res` → {res}',
        'start_pos += 1': '左边界右移到 {start_pos}',
        'return res': '共 `{res}` 个恰好 K 种不同整数的子数组',
    },
    skip=['n = len(A)', 'l = -1', 'cnt_dict = {}', 'last_pos[A[index]] = index'],
    max_steps=95,
    cards=dict(
        one_liner='固定左端点，合法右端点是一段区间 [l, r]',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组 `A`，求恰好包含 `K` 个不同整数的==连续子数组==个数',
                 '示例：`A = [1,2,1,2,3], K = 2` → `7`',
                 '`[1,2] [2,1] [1,2] [2,3] [1,2,1] [2,1,2] [1,2,1,2]`'],
        quote='对于一个固定的左边界start_pos而言，我们定义最小右边界l以及最大右边界r。……那么从start_pos开始的有K个不同整数的子数组一共有r - l + 1个。',
        quote_src='—— yiduobo 题解原文',
        idea=['`l`：刚好凑够 `K` 种数的最短右端；`r`：再往右只吞已有的数能走多远',
              '左端点右移时，若 `A[start_pos]` 还有重复，`r` 不变，只需让 `l` 不小于它的下一次出现位置 `next_pos`',
              '若它是唯一的，种类掉到 `K-1`，必须把 `r+1` 这个新数拉进来：`l = r + 1`，再重新扩 `r`'],
        summary=['时间 `O(n)`：`start_pos`、`l`、`r` 都只向右走',
                 '`next_pos` 用一趟从右往左的扫描预处理，避免反复查找',
                 '易错：凑不够 `K` 种要直接返回 0；`l` 越界要 `break`',
                 '原文已是 Python 3 可运行写法，未作修改',
                 '常见替代：`atMost(K) − atMost(K−1)`，yiduobo 这里直接数区间长度'],
    ),
)
