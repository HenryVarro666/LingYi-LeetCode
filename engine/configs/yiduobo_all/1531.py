S0, K0 = 'aabaa', 1


def _cur(S):
    return S.get('now')


def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    now, dc = S.get('now'), S.get('del_cnt')
    if now is not None and now > 0 and dc is not None and j - dc >= 0 and (r, c) == (now - 1, j - dc) and S.get('_line') == 41:
        return 'blue'
    if j > 0 and i > 0 and (r, c) == (i - 1, j - 1) and S.get('_line') == 22:
        return 'green'
    return None


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return '`f[i][j]` = 处理 `s[0..i]`、最多删 `j` 个字符后的最短压缩长度'
    return f'正在算 `f[{i}][{j}]`：`s[0..{i}]` 里最多删 `{j}` 个字符'


CONFIG = dict(
    num=1531, title='压缩字符串 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='线性 DP · 向前合并相同字符',
    tags=[],
    code='''
class Solution(object):
    def getLengthOfOptimalCompression(self, s, k):

        n = len(s)
        prev_pos = [-1] * n
        last_pos = {}
        for index, char in enumerate(s):
            if char in last_pos:
                prev_pos[index] = last_pos[char]
            
            last_pos[char] = index
        
        f = [[n + 1] * (k + 1) for _ in range(n)]
        for i in range(n):
            for j in range(k + 1):
                if j >= i + 1:
                    f[i][j] = 0
                elif i == 0:
                    f[i][j] = 1
                else:
                    if j > 0:
                        f[i][j] = f[i - 1][j - 1]
                    
                    now = i
                    merge_cnt = 0
                    del_cnt = 0
                    while now != -1 and del_cnt <= j:
                        merge_cnt += 1
                        if merge_cnt == 1:
                            zip_len = 1
                        elif merge_cnt <= 9:
                            zip_len = 2
                        elif merge_cnt <= 99:
                            zip_len = 3
                        else:
                            zip_len = 4

                        if now == 0:
                            f[i][j] = min(f[i][j], zip_len)
                        else:
                            f[i][j] = min(f[i][j], f[now - 1][j - del_cnt] + zip_len)
                        
                        del_cnt += now - prev_pos[now] - 1
                        now = prev_pos[now]
        
        return f[-1][-1]
''',
    call=f'Solution().getLengthOfOptimalCompression({S0!r}, {K0})',
    expect=2,
    views=[
        dict(type='string', var='s', label='s（蓝 = i；粉 = 正在向前合并的同字符 now）', cell=84, h=190,
             pointers={'i': 'blue', _cur: 'pink'}, pointer_labels={_cur: 'now'},
             color=lambda S, k, v: 'blue' if k == S.get('i') else 'pink' if k == S.get('now') else None),
        dict(type='text', fn=_formula, size=26, h=60),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算，蓝 = 合并时依赖的格子）', h=330, cell=76,
             rows=lambda S: [f'{k}{c}' for k, c in enumerate(S0)], cols=lambda S: [str(j) for j in range(K0 + 1)],
             color=_cell),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'cyan'), ('now', 'now', 'pink'), ('merge_cnt', 'merge_cnt', 'yellow'),
           ('del_cnt', 'del_cnt', 'orange'), ('zip_len', 'zip_len', 'green')],
    skip=['n = len(s)', 'last_pos = {}', 'for index, char', 'if char in last_pos', 'prev_pos[index] = last_pos', 'last_pos[char] = index',
          'for j in range(k + 1)', 'now = i', 'merge_cnt = 0', 'del_cnt = 0', 'elif merge_cnt', 'else:', 'if merge_cnt == 1', 'zip_len = ', 'f[i][j] = 0', 'f[i][j] = 1', 'now = prev_pos[now]', 'if j > 0', 'if now == 0'],
    captions={
        'prev_pos = [-1] * n': '先扫一遍预处理：`prev_pos[x]` = 和 `s[x]` 相同的==上一个位置==，没有就是 -1（后面用它向前跳）',
        'f = [[n + 1]': '`f[i][j]`：`s[0..i]` 最多删 `j` 个字符的最短压缩长度；先填大数 `n+1`，表示还没算',
        'for i in range': '`i = {i}`：处理到 `s[{i}]`；`prev_pos = {prev_pos}`',
        'if j >= i + 1': lambda S, B, r: (f'`j = {S.j} >= i+1 = {S.i + 1}`：整个前缀都能删光 → `f[{S.i}][{S.j}] = 0`' if S.j >= S.i + 1
                                         else f'`j = {S.j} < i+1`：删不光，继续看'),
        'elif i == 0': lambda S, B, r: ('`i = 0`：只有 `s[0]` 一个字符，且 `j < 1` 不能删 → `f[0][0] = 1`' if S.i == 0 else f'`i = {S.i} > 0`：删 `s[i]`，或保留它并向前合并，两种取小'),
        'f[i][j] = f[i - 1][j - 1]': '==删掉 s[i]==：`f[{i}][{j}] = f[{i-1}][{j-1}] = {f[i][j]}`',
        'while now != -1': lambda S, B, r: (f'`now = {S.now}`，已删 `{S.del_cnt}` 个（上限 `{S.j}`）→ 继续向前找相同字符 `{S.s[S.i]}`' if S.now != -1 and S.del_cnt <= S.j
                                            else ('向前没有相同字符了，这个格子算完' if S.now == -1 else f'已删 `{S.del_cnt}` > 上限 `{S.j}` → ==不能再往前合并==，结束')),
        'merge_cnt += 1': '合并进一个 `{s[i]}`，共 `{merge_cnt}` 个，压成 `{s[i]}{merge_cnt if merge_cnt > 1 else ""}`，长度 ==`{1 if merge_cnt == 1 else 2 if merge_cnt <= 9 else 3 if merge_cnt <= 99 else 4}`==（1 / 2~9 / 10~99 / 100）',
        'if now == 0': lambda S, B, r: ('合并到了 `s[0]`，前面没有字符了，直接用 `zip_len`' if S.now == 0 else f'前面还有 `s[0..{S.now - 1}]`，它们要再处理：`f[{S.now - 1}][{S.j - S.del_cnt}]`'),
        'f[i][j] = min(f[i][j], zip_len)': '`f[{i}][{j}] = min(旧值, {zip_len})` = =={f[i][j]}==',
        'f[i][j] = min(f[i][j], f[now - 1]': '`min(旧值, f[{now-1}][{j-del_cnt}] + {zip_len})` = =={f[i][j]}==：前面还剩的删除额度是 `{j-del_cnt}`',
        'del_cnt += now - prev_pos[now] - 1': lambda S, B, r: (f'再往前合并 `s[{S.prev_pos[S.now]}]`：中间 `{S.now-S.prev_pos[S.now]-1}` 个不同字符必须删掉 → ==`del_cnt = {S.del_cnt}`==，`now` 跳到 `{S.prev_pos[S.now]}`' if S.prev_pos[S.now] != -1
                                                    else '前面没有相同字符了，`now = -1`，退出循环'),
        'now = prev_pos[now]': '`now` 跳到上一个相同字符的位置：`{now}`',
        'return f[-1][-1]': '答案 `f[{n-1}][{k}]` = =={ret}==',
    },
    max_steps=56,
    cards=dict(
        one_liner='f[i][j]：保留 s[i] 时，只往前合并“相同字符”，中间的全删',
        complexity='时间约 `O(n^2·k)`，空间 `O(n·k)`',
        problem=['游程编码：`"aaabcccd"` → `"a3bc3d"`（只有 1 个不加数字）',
                 '允许最多删掉 `k` 个字符，使压缩后的字符串==最短==，返回最短长度',
                 '本视频：`s = "aabaa", k = 1` → `2`（删掉 `b` 得 `"aaaa"` → `"a4"`）'],
        quote='对于与 s[i] 相同字符的选取必然是从后向前连续选取的……从 i 开始向前迭代 prev_pos。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：`s[0..i]` 最多删 `j` 个字符的最短压缩长度',
              '要么删掉 `s[i]`（`f[i-1][j-1]`），要么保留它并和前面相同的字符合并',
              '合并时沿 `prev_pos` 向前跳，中间不同的字符都要删，累计 `del_cnt`，超过 `j` 就停'],
        summary=['压缩长度：1 个→1，2~9 个→2，10~99 个→3，100 个→4',
                 '`j >= i+1` 时整个前缀可删光，长度为 0',
                 '易错：合并相同字符时必须==删光它们之间的其他字符==，所以用 `del_cnt` 累计删除额度',
                 '原文为 Python 2 风格，本题无需改动，直接照搬']
    ),
)
