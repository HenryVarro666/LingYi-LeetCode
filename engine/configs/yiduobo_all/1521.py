def _txt(S):
    if 'now' not in S or 'l' not in S:
        return ''
    n = S['now']
    return f"窗口 `[{S['l']}..{S['r']}]` 的按位与 `now` = =={'?' if n is None else n}==　`target = {S['target']}`　`res` = =={S['res']}=="


def _fcell(S, i, j, v):
    if S.get('_line') in (40, 42) and 'p' in S and (i, j) == (S['p'], S['j']):
        return 'yellow'
    if 'l' not in S and S.get('_line') == 20 and (i, j) == (S.get('i'), S.get('j')):
        return 'yellow'
    return None


CONFIG = dict(
    num=1521, title='找到最接近目标值的函数值', difficulty='Hard', category='位运算',
    author='yiduobo', technique='滑动窗口 + ST 表求区间与',
    tags=['灵神题单', '难度分 3171'],
    code='''
class Solution(object):
    def closestToTarget(self, arr, target):

        pow2 = [1]
        level = 0
        n = len(arr)
        while pow2[-1] <= n:
            pow2.append(pow2[-1] + pow2[-1])
            level += 1
        
        level -= 1
        pow2.pop()

        f = [[0] * (level + 1) for _ in range(n)]
        for j in range(level + 1):
            for i in range(n):
                if j == 0:
                    f[i][j] = arr[i]
                elif i + pow2[j] - 1 < n:
                    f[i][j] = f[i][j - 1] & f[i + pow2[j - 1]][j - 1]
        
        res = abs(arr[0] - target)
        l = r = 0
        now = arr[0]
        while r + 1 < n:
            r += 1
            now &= arr[r]
            res = min(res, abs(now - target))
            if res == 0:
                return res
            while l < r and now < target:
                l += 1
                p = l
                now = None
                j = level
                while p <= r:
                    while pow2[j] > r - p + 1:
                        j -= 1
                    if now is None:
                        now = f[p][j]
                    else:
                        now &= f[p][j]
                    
                    p += pow2[j]
                
                res = min(res, abs(now - target))
                if res == 0:
                    return res

        return res
''',
    call='Solution().closestToTarget([9,12,3,7], 5)',
    expect=2,
    views=[
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='array', var='arr', pointers={'l': 'pink', 'r': 'blue'}, window=('l', 'r'), h=220, label='arr（窗口 = l 到 r）',
             dim=lambda S, i, v: 'l' in S and not (S['l'] <= i <= S['r'])),
        dict(type='table', var='f', label='ST 表 f[i][j] = 从 i 起长 2^j 的区间按位与（j 列的长度 = 2^j）（黄 = 当前用到/正在算）', h=330, cell=80,
             rows=lambda S: [f'i={k}' for k in range(len(S['f']))], cols=lambda S: [f'j={k}' for k in range(len(S['f'][0]))],
             color=_fcell),
    ],
    watch=['l', 'r', ('now', 'now', 'cyan'), ('target', 'target', 'yellow'), ('res', 'res', 'green')],
    skip=['for i in range(n)', 'if j == 0', 'f[i][j] = arr[i]', 'elif i + pow2[j] - 1 < n', 'while r + 1 < n', 'p = l', 'j = level', 'if res == 0', 'while p <= r', 'j -= 1', 'if now is None', 'level += 1', 'level -= 1', 'now = None', 'l = r = 0'],
    captions={
        'pow2 = [1]': '`pow2` 存 `1, 2, 4, …`，用来切 2 的幂长度的区间',
        'while pow2[-1] <= n': '`pow2` 最后一个 `{pow2[-1]}` ≤ n={n} → 还要继续翻倍',
        'level += 1': '`pow2 = {pow2}`，`level = {level}`',
        'level -= 1': '最后一个 `pow2` 已超过 n，退一层：`level = {level}`',
        'pow2.pop()': '翻倍到超过 n 为止，`level` 退一层并丢掉多出的那个 → `pow2 = {pow2}`，`level = {level}`',
        'f = [[0]': '`f[i][j]`：从 i 开始长 `2^j` 的区间按位与，先全填 0',
        'for j in range(level + 1)': lambda S, B, r: (f'填第 `{S.j}` 层：长度 `{2 ** S.j}` 的区间与（`j=0` 是 arr 本身，之后由两个半长区间相与得到）' if S.get('j') != B.get('j') else 'ST 表建好了'),
        'f[i][j] = f[i][j - 1]': '`f[{i}][{j}] = f[{i}][{j-1}] & f[{i + 2**(j-1)}][{j-1}]` = `{f[i][j]}`',
        'res = abs(arr[0] - target)': '先只看第一个元素：`res = |{arr[0]} − {target}| = {res}`',
        'l = r = 0': '窗口 `[l, r]` 从下标 0 开始',
        'now = arr[0]': '`now` 是窗口内按位与，初始 `{now}`',
        'r += 1': '右端点右移：`r = {r}`，窗口变长',
        'now &= arr[r]': '右端点加入，直接与上去：`now = {now}`（与越多越小）',
        'res = min(res, abs(now - target))': lambda S, B, r: f'`|{S.now} − {S.target}| = {abs(S.now - S.target)}`，`res` = {S.res}',
        'if res == 0': lambda S, B, r: ('差为 0，不可能更小 → 提前返回' if S.res == 0 else '差不为 0，继续'),
        'return res': '返回 `res = {res}`',
        'while l < r and now < target': lambda S, B, r: (f'`now = {S.now} < target = {S.target}`：与值太小 → ==左端点右移==让它变大' if S.now < S.target and S.l < S.r
                                                       else f'`now = {S.now}` 不小于 target，或窗口只剩一个数 → 去扩右端点'),
        'l += 1': '左端点右移：`l = {l}`。去掉 `arr[l-1]` 后 AND 无法直接更新 → 用 ST 表重算 `[l, r]`',
        'now = None': '重算 `[{l}, {r}]` 的与值：每次切一块长为 2 的幂的区间',
        'while p <= r': lambda S, B, r: (f'`p = {S.p} <= r = {S.r}`：还有区间没算' if S.p <= S.r else f'`p = {S.p} > r`：整个窗口切完了'),
        'while pow2[j] > r - p + 1': lambda S, B, r: (f'`2^{S.j} = {S.pow2[S.j]}` 超过剩余长度 `{S.r - S.p + 1}` → 降一层（`j -= 1`）' if S.pow2[S.j] > S.r - S.p + 1
                                                    else f'`2^{S.j} = {S.pow2[S.j]}` ≤ 剩余长度 `{S.r - S.p + 1}`，用这一层'),
        'j -= 1': '`j` 降为 `{j}`',
        'if now is None': '第一块直接取，后面的块再 `&` 上去',
        'now = f[p][j]': '`now = f[{p}][{j}] = {now}`：从 `{p}` 起长 `{pow2[j]}` 的与值',
        'now &= f[p][j]': '再与上 `f[{p}][{j}]` → `now = {now}`',
        'p += pow2[j]': '这块用完，`p` 前进 `{pow2[j]}` → `{p}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='与越多越小：窗口双指针 + ST 表快速重算区间与',
        complexity='时间 `O(n log n)`，空间 `O(n log n)`',
        problem=['`func(arr, l, r)` 是 `arr[l..r]` 的按位与，求 `|func − target|` 的最小值',
                 '示例：`arr=[9,12,3,7], target=5` → `2`',
                 '本视频用同一个示例'],
        quote='当固定了左边界l时，若右边界r越大，那么按位与的结果就越小……很自然想到使用滑动窗口来处理这个问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['结果比 target 小 → 左端点右移让与值变大；每次移动都更新答案',
              '右端点加入可以直接 `&`；左端点离开不行 → 用 ST 表 `f[i][j]` 重算区间与',
              '区间 `[l, r]` 切成若干长为 2 的幂的块，`O(log n)` 个块相与'],
        summary=['时间 `O(n log n)`，空间 `O(n log n)`',
                 '易错：`now < target` 才缩左端点；`l < r` 保证窗口非空',
                 '易错：ST 表要先判断 `i + 2^j - 1 < n`，否则越界',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行',
                 '对比灵神：灵神用 LogTrick，只改 arr 本身，无需 ST 表（yiduobo 另提供了统计每位 1 个数的思路）'],
    ),
)
