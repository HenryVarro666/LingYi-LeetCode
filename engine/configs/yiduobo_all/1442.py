def _prefix(S):
    return list(accumulate(S['arr'], xor, initial=0))


def _pcolor(S, i, v):
    if 'index' not in S or S['_line'] < 9:
        return None
    if i == S['index'] + 1:
        return 'blue'
    if i in S['pos_dict'].get(S['now'], []):
        return 'green'
    return None


def _txt(S):
    if 'index' not in S:
        return '前缀异或相同的两个位置 `p` 和 `index+1`，夹住的 `arr[p..index]` 异或为 0'
    ln = S['_line']
    if ln in (8, 9):
        return f"`now` = arr[0..{S['index']}] 的异或" + (f" = ==`{S['now']}`==" if ln == 9 else '')
    if ln in (10, 11):
        return f"前缀异或值 `{S['now']}`：" + ('第一次出现，记下位置' if ln == 11 else '先看它是否出现过')
    if ln in (13, 14, 15):
        p = S['last_pos']
        k = S['index']
        base = f'`i = {p}`，`k = {k}`：`arr[{p}..{k}]` 异或为 0'
        if ln == 15:
            return base + f'，`j` 取 {p + 1}..{k}，共 =={k - p}== 种'
        return base
    if ln == 16:
        return f"`pos_dict[{S['now']}] = {S['pos_dict'][S['now']]}`"
    return ''


def _if_new(S, B, ret):
    now, d = S.now, S.pos_dict
    if now not in B.pos_dict:
        return f'`now = {now}` 之前没出现过：没有前缀能和它配成异或为 0 的区间'
    return f'`now = {now}` 出现过，位置 `{d[now]}`：每个旧位置 `p` 都能让 `arr[p..{S.index}]` 异或为 0'


CONFIG = dict(
    num=1442, title='形成两个异或相等数组的三元组数目', difficulty='Medium', category='位运算',
    author='yiduobo', technique='前缀异或 + 哈希表存位置列表',
    tags=['灵神核心路线', '灵神题单·位运算'],
    code='''
class Solution(object):
    def countTriplets(self, arr):

        pos_dict = {}
        pos_dict[0] = [0]
        now = 0
        res = 0
        for index, num in enumerate(arr):
            now ^= num
            if now not in pos_dict:
                pos_dict[now] = [index + 1]
            else:
                for last_pos in pos_dict[now]:
                    if index + 1 - last_pos >= 2:
                        res += index - last_pos
                pos_dict[now].append(index + 1)

        return res
''',
    call='Solution().countTriplets([1,1,1,1,1])',
    expect=10,
    views=[
        dict(type='array', var='arr', label='arr（框 = 当前异或为 0 的区间 arr[i..k]）', cell=84, pointers={'index': 'blue'},
             window=('last_pos if _line in (13, 14, 15) else None', 'index'), h=205),
        dict(type='array', var=_prefix, label='前缀异或 P[t]（绿 = 与 now 相同的旧位置，蓝 = 当前位置）', cell=84,
             pointers={'index + 1': 'blue', 'last_pos if _line in (13, 14, 15) else None': 'pink'},
             pointer_labels={'index + 1': 'index+1', 'last_pos if _line in (13, 14, 15) else None': 'last_pos'},
             color=_pcolor, dim=lambda S, i, v: 'index' in S and i > S['index'] + 1, h=225),
        dict(type='map', var='pos_dict', label='pos_dict：前缀异或值 → 出现过的位置', fmt=lambda k, v: f'{k}: {v}', h=115, font=28),
        dict(type='text', h=85, size=28, fn=_txt),
    ],
    watch=[('index', 'index', 'blue'), ('num', 'num'), ('now', 'now', 'cyan'), ('last_pos', 'last_pos', 'pink'), ('res', 'res', 'green')],
    captions={
        'pos_dict = {}': '`pos_dict`：前缀异或值 → 它出现过的位置列表（位置 `p` 表示 `arr[0..p-1]` 的异或）',
        'pos_dict[0] = [0]': '空前缀的异或是 0，位置记 `0`，这样 `arr[0..k]` 本身异或为 0 的情况也能数到',
        'now = 0': '`now`：当前前缀异或值',
        'res = 0': '`res`：三元组总数',
        'for index, num': lambda S, B, r: (f'处理 `arr[{S.index}] = {S.num}`' if 'index' in S and ('index' not in B or S.index != B.index)
                                           else '遍历结束'),
        'now ^= num': '`now = {B.now} ^ {num}` → =={now}==：这是 `arr[0..{index}]` 的异或',
        'if now not in pos_dict': _if_new,
        'pos_dict[now] = [index + 1]': '新的异或值，记下它的位置 `index + 1 = {index + 1}`',
        'for last_pos in': lambda S, B, r: (f'取下一个旧位置 `last_pos = {S.last_pos}` 当作 `i`' if 'last_pos' not in B or S.last_pos != B.last_pos
                                            else '这个异或值的旧位置都配过了，循环结束'),
        'if index + 1 - last_pos >= 2': lambda S, B, r: (f'区间长度 `{S.index + 1 - S.last_pos}` ≥ 2，能拆成两段' if S.index + 1 - S.last_pos >= 2
                                                         else f'区间只有 1 个数，拆不成 `i<j≤k` 两段，跳过'),
        'res += index - last_pos': '`i = {last_pos}`，`k = {index}`：`j` 可取 `{last_pos + 1}..{index}`，共 `{index} − {last_pos}` = `{index - last_pos}` 种 → `res` = =={res}==',
        'pos_dict[now].append(index + 1)': '把当前位置 `{index + 1}` 也记进列表，留给后面的下标配对',
        'return res': '一共 `{res}` 个三元组',
    },
    cards=dict(
        one_liner='区间异或为 0，就能在区间里任意切一刀得到 a = b',
        complexity='时间 `O(n^2)`（最坏），空间 `O(n)`',
        problem=['数组 `arr`，找三元组 `(i, j, k)`，满足 `i < j <= k`',
                 '`a = arr[i]^…^arr[j-1]`，`b = arr[j]^…^arr[k]`，要求 `a == b`',
                 '示例：`[1,1,1,1,1]` → `10`'],
        quote='根据异或的性质，a = b也就意味着a ^ b = 0。……这是一个区间异或的形式，更进一步的，可以转化成一个前缀异或问题',
        quote_src='—— yiduobo 题解原文',
        idea=['`a == b` ⇔ `a ^ b == 0` ⇔ 整段 `arr[i..k]` 异或为 0',
              '整段异或为 0 ⇔ 前缀异或 `P[i] == P[k+1]`，而 `j` 可以在 `i+1..k` 里随便选',
              '一趟扫描：每个 `k` 配上之前所有相同前缀异或的位置 `p`，各贡献 `k − p` 个三元组'],
        summary=['最坏 `O(n^2)`：全是相同前缀值时，每次要遍历整个位置列表',
                 '位置记成 `index + 1`（前缀长度），所以 `j` 的个数是 `index − last_pos`',
                 '`pos_dict[0] = [0]` 是空前缀，漏掉会少数 `i = 0` 的情况',
                 '代码与原文一致，Python 3 可直接运行',
                 '更快的写法：同一异或值只存「个数」和「下标和」，可做到 `O(n)`'],
    ),
)
