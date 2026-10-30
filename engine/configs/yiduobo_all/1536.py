G = [[0, 0, 1], [1, 1, 0], [1, 0, 0]]

CONFIG = dict(
    num=1536, title='排布二进制网格的最少交换次数', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='最后一个 1 的位置 · 逐位冒泡',
    tags=['灵神题单', '难度分 1881'],
    code='''
class Solution(object):
    def minSwaps(self, grid):
        
        pos_list = []
        n = len(grid)
        for i in range(n):
            pos_list.append(0)
            for j in range(n - 1, -1, -1):
                if grid[i][j] == 1:
                    pos_list[-1] = j
                    break
        
        res = 0
        for i in range(n):
            if pos_list[i] <= i:
                continue
            
            now = pos_list[i]
            pos_list[i] = None
            for j in range(i + 1, n):
                pos_list[j], now = now, pos_list[j]
                res += 1
                if now <= i:
                    pos_list[i] = now
                    break
            
            if pos_list[i] is None:
                return -1
        
        return res
''',
    call=f'Solution().minSwaps({G})',
    expect=3,
    views=[
        dict(type='grid', var='grid', h=250,
             color=lambda S, i, j, v: 'blue' if v == 1 else None),
        dict(type='array', var='pos_list', label='pos_list（每行最后一个 1 的列号，要求 pos_list[k] <= k）', h=220,
             pointers={'i': 'blue', 'j': 'pink'},
             color=lambda S, i, v: ('green' if (v is not None and v <= i) else 'red') if 'res' in S and v is not None else None),
        dict(type='text', fn=lambda S: (f"第 `{S['i']}` 位要求值 `<= {S['i']}`，当前是 ==`{S['pos_list'][S['i']]}`==" if 'res' in S and 'i' in S and S['i'] < len(S['pos_list']) else ''), size=30),
    ],
    watch=['i', 'j', 'now', ('res', 'res', 'green')],
    captions={
        'pos_list.append(0)': '先给第 `{i}` 行占一个位置，默认最后的 1 在列 0（全 0 行也合法）',
        'pos_list[-1] = j': '第 `{i}` 行最后一个 1 在列 `{j}` → `pos_list = {pos_list}`',
        'res = 0': '`pos_list` 就绪：{pos_list}。问题变成：相邻交换，使每个 `pos_list[k] <= k`',
        'if pos_list[i] <= i': lambda S, B, r: (
            f'`pos_list[{S.i}] = {S.pos_list[S.i]} <= {S.i}` → 这一位已满足，跳过'
            if S.pos_list[S.i] <= S.i else
            f'`pos_list[{S.i}] = {S.pos_list[S.i]} > {S.i}` → ==不满足==，往后找最近的合格者'),
        'continue': '直接看下一位',
        'now = pos_list[i]': '把不合格的值 `{now}` 拎在手上，位置 `{i}` 先空出来',
        'pos_list[i] = None': '位置 `{i}` 置空，等合格者换过来',
        'for j in range(i + 1, n)': '从 `{i}` 的下一位开始逐个往后看',
        'pos_list[j], now = now, pos_list[j]': '相邻交换：手上的值落到位置 `{j}`，取起原来的 `{now}` → `{pos_list}`',
        'res += 1': '这是一次相邻交换，`res = {res}`',
        'if now <= i': lambda S, B, r: (
            f'手上的 `{S.now} <= {S.i}` → 合格，==最近的合格者找到了=='
            if S.now <= S.i else f'手上的 `{S.now} > {S.i}` → 还不合格，继续往后找'),
        'pos_list[i] = now': '把合格的值放到位置 `{i}` → `{pos_list}`',
        'if pos_list[i] is None': lambda S, B, r: (
            f'位置 `{S.i}` 仍是空 → 后面没有合格者，无解' if S.pos_list[S.i] is None
            else f'位置 `{S.i}` 已填好（`{S.pos_list[S.i]}`），处理下一位'),
        'return -1': '返回 `-1`',
        'return res': '一共交换 `{res}` 次',
    },
    cards=dict(
        one_liner='转成 a[k] <= k 的数组：往后找最近的合格者，两两交换换过来',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`n x n` 的 0/1 网格，每次可交换相邻两行',
                 '目标：主对角线以上全是 0，求最少交换次数，不行返回 `-1`',
                 '示例：`[[0,0,1],[1,1,0],[1,0,0]]` → `3`'],
        quote='第k行最后一个1出现的位置必须要在位置k之前。……以最少的次数交换数组中相邻的数字，使得数组中的每个数a[k]满足a[k] <= k。',
        quote_src='—— yiduobo 题解原文',
        idea=['先记下每行最后一个 1 的列号，第 `k` 行要求它 `<= k`',
              '位置 `i` 不满足就往后找最近的满足者，==两两交换==逐位换过来'],
        summary=['时间 `O(n^2)`：预处理和交换都是双重循环，不需要再用数据结构优化',
                 '`pos_list[i] = None` 标记「还没找到」，找不到就返回 `-1`',
                 '全 0 行的位置记为 0，必然满足',
                 '对比灵神：灵神记尾零数、要求 `>= n-1-i`；这里记最后一个 1 的位置、要求 `<= i`，本质相同'],
    ),
)
