def _gcolor(S, i, j, v):
    ln = S['_line']
    if ln >= 20 and S.get('i') is not None and S.get('j') is not None and (i, j) == (S['i'], S['j']) and 'm' in S:
        return 'yellow'
    if 'm' not in S:
        return None
    m, n = S['m'], S['n']
    h = (i * n + j) in (S.get('hit_row') or ())
    c = (j * m + i) in (S.get('hit_col') or ())
    return 'green' if h and c else 'blue' if h else 'pink' if c else None


def _sets(S):
    if 'hit_row' not in S:
        return ''
    a = sorted(S['hit_row'])
    s = f"水平命中的下标 `hit_row` = {a}"
    if 'hit_col' in S:
        s += f"　垂直 `hit_col` = {sorted(S['hit_col'])}"
    return s


CONFIG = dict(
    num=3529, title='统计水平子串和垂直子串重叠格子的数目', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='KMP 匹配 · 集合记录命中下标',
    tags=['灵神题单·常用数据结构', '灵神题单·字符串'],
    code='''
class Solution(object):
    def countCells(self, grid, pattern):

        f = [0]
        p = 0
        for index in range(1, len(pattern)):
            while p and pattern[p] != pattern[index]:
                p = f[p - 1]
            
            if pattern[p] == pattern[index]:
                p += 1
            f.append(p)
        
        m = len(grid)
        n = len(grid[0])
        
        hit_row = set()
        p = 0
        start = 0
        for i in range(m):
            for j in range(n):
                while p and pattern[p] != grid[i][j]:
                    p = f[p - 1]
                
                if pattern[p] == grid[i][j]:
                    p += 1
                    if p == len(pattern):
                        now = i * n + j
                        for index in range(max(start, now - len(pattern) + 1), now + 1):
                            hit_row.add(index)
                        start = now + 1
                        p = f[p - 1]
        
        hit_col = set()
        p = 0
        start = 0
        for j in range(n):
            for i in range(m):
                while p and pattern[p] != grid[i][j]:
                    p = f[p - 1]
                
                if pattern[p] == grid[i][j]:
                    p += 1
                    if p == len(pattern):
                        now = j * m + i
                        for index in range(max(start, now - len(pattern) + 1), now + 1):
                            hit_col.add(index)
                        start = now + 1
                        p = f[p - 1]
        
        res = 0
        for i in range(m):
            for j in range(n):
                if i * n + j in hit_row and j * m + i in hit_col:
                    res += 1
        
        return res
''',
    call='Solution().countCells([["a","b"],["a","b"]], "ab")',
    expect=2,
    skip=['f = [0]', 'p = 0', 'start = 0', 'hit_row = set()', 'hit_col = set()', 'res = 0', 'for index in range(1', 'for i in range', 'for j in range'],
    views=[
        dict(type='string', var='pattern', label='pattern（p = 已匹配长度，指向下一个要比的字符）',
             pointers={'p': 'pink', 'index if _line <= 12 else None': 'blue'},
             pointer_labels={'index if _line <= 12 else None': 'index'}, h=210, cell=76),
        dict(type='array', var='f', label='f（前缀函数，失配时 p 退回 f[p-1]）', h=130, cell=76, index=False),
        dict(type='grid', var='grid', label='grid（黄=当前格，蓝=水平命中，粉=垂直命中，绿=都命中）', color=_gcolor, h=190, cell=70),
        dict(type='text', size=26, h=90, fn=_sets),
    ],
    watch=['p', ('start', 'start', 'purple'), ('res', 'res', 'green')],
    captions={
        'while p and pattern[p] != pattern[index]': '算 `f[{index}]`：`p = {p}`，`pattern[{p}] = {pattern[p]}` 与 `pattern[{index}] = {pattern[index]}` {"不等且 p > 0 → 退回" if p and pattern[p] != pattern[index] else "不用退"}',
        'if pattern[p] == pattern[index]': '`pattern[{p}] = {pattern[p]}` {"==" if pattern[p] == pattern[index] else "!="} `pattern[{index}] = {pattern[index]}`：{"相等，p + 1" if pattern[p] == pattern[index] else "不等，p 保持"}',
        'f.append(p)': '`f[{index}] = {p}`：`f = {f}`',
        'm = len(grid)': '先在按行拉直的串上找：不真的拉直，直接按行扫格子，下标 `i * n + j`',
        'n = len(grid[0])': '`m = {m}` 行，`n = {n}` 列',
        'while p and pattern[p] != grid[i][j]': lambda S, B, r: (f'格子 `({S.i}, {S.j}) = {S.grid[S.i][S.j]}`，`p = {S.p}`：' + (f'`pattern[{S.p}] = {S.pattern[S.p]}` 不等 → 退回 `f[{S.p - 1}]`' if S.p and S.pattern[S.p] != S.grid[S.i][S.j] else '不用退')),
        'p = f[p - 1]': lambda S, B, r: (f'失配退回：`p = f[{B.p - 1}]` = =={S.p}==' if B.p != len(B.pattern) else f'整段匹配完不清零：`p = f[{B.p - 1}]` = =={S.p}==，重叠的下一段接着用'),
        'if pattern[p] == grid[i][j]': lambda S, B, r: f'`pattern[{S.p}] = {S.pattern[S.p]}` {"==" if S.pattern[S.p] == S.grid[S.i][S.j] else "!="} `{S.grid[S.i][S.j]}`' + ('，匹配' if S.pattern[S.p] == S.grid[S.i][S.j] else '，不匹配，看下一格'),
        'p += 1': '匹配一位：`p` → =={p}==',
        'if p == len(pattern)': lambda S, B, r: (f'`p = {S.p} == len(pattern)`：找到一个完整的 pattern' if S.p == len(S.pattern) else f'`p = {S.p}`，还没匹配完'),
        'now = i * n + j': '匹配在水平串的下标 `{now}` 结束，起点 `{now - len(pattern) + 1}`',
        'now = j * m + i': '匹配在垂直串的下标 `{now}` 结束，起点 `{now - len(pattern) + 1}`',
        'for index in range(max': '从 `max(start, now - len + 1) = {max(start, now - len(pattern) + 1)}` 记到 `{now}`：`start` 防止重叠的匹配重复记',
        'hit_row.add': '`hit_row` 加入下标 `{index}`',
        'hit_col.add': '`hit_col` 加入下标 `{index}`',
        'start = now + 1': '`start = {start}`：下次记录从这里开始，已记过的不再记',
        'if i * n + j in hit_row': lambda S, B, r: f'格子 `({S.i}, {S.j})`：水平下标 `{S.i * S.n + S.j}` {"在" if S.i * S.n + S.j in S.hit_row else "不在"} `hit_row`，垂直下标 `{S.j * S.m + S.i}` {"在" if S.j * S.m + S.i in S.hit_col else "不在"} `hit_col`' + (' → ==满足==' if (S.i * S.n + S.j in S.hit_row and S.j * S.m + S.i in S.hit_col) else ' → 不满足'),
        'res += 1': '计数：`res` → =={res}==',
        'return res': '共 `{res}` 个格子',
    },
    cards=dict(
        one_liner='按行、按列各做一遍 KMP，用集合记命中的下标，再逐格查两个集合',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['字符矩阵 `grid`，水平子串换行接着读，垂直子串换列接着读',
                 '统计同时属于水平匹配和垂直匹配的格子数',
                 '本视频：`[["a","b"],["a","b"]]`，`pattern="ab"` → `2`'],
        quote='可以发现，题目中的水平子串实际上就是将grid按行拉直后得到的字符串中的子串，而垂直子串则是将grid按列拉直后得到的字符串中的子串，那么在这里就可以先用kmp找出所有等于pattern的水平子串以及竖直子串。',
        quote_src='—— yiduobo 题解原文',
        idea=['不真的拉直，直接按行/按列扫格子，下标分别是 `i*n+j` 和 `j*m+i`',
              '匹配成功就把区间里的下标放进 `hit_row` / `hit_col`',
              '匹配会重叠，用 `start` 记下一次记录的起点，避免重复记',
              '最后遍历每个格子，两个下标都在集合里才算'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '`start` 保证每个下标只进一次集合；也可以直接 `add`，集合会去重，只是会多做重复工作',
                 '原文不含 Python 2 特有写法，代码未改动',
                 '对比灵神：灵神用差分数组标记区间，这里用集合 + `start`；灵神拆成 `kmp_search` 复用，这里水平垂直各写一遍'],
    ),
)
