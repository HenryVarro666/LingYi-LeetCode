CONFIG = dict(
    num=1566, title='重复至少 K 次且长度为 M 的模式', difficulty='Easy', category='模拟',
    author='yiduobo', technique='暴力枚举起点逐位检查',
    code='''
class Solution(object):
    def containsPattern(self, arr, m, k):

        n = len(arr)
        for index in range(n):
            if index + m * k - 1 >= n:
                return False

            flag = True
            for i in range(m):
                now = arr[index + i]
                for j in range(1, k):
                    next = arr[index + i + m * j]
                    if now != next:
                        flag = False
                        break
                
                if not flag:
                    break
            
            if flag:
                return True
''',
    call='Solution().containsPattern([1, 2, 2, 3, 2, 3, 2, 3], 2, 3)',
    expect=True,
    views=[
        dict(type='array', var='arr', label='arr（蓝 = 起点 index，黄 = 当前比较的两个位置）', cell=90, h=260,
             pointers={'index': 'blue'},
             window=('index', 'min(index + m * k - 1, n - 1)'),
             color=lambda S, i, v: ('yellow' if ('index' in S and 'i' in S and 'j' in S and i in (S['index'] + S['i'], S['index'] + S['i'] + S['m'] * S['j'])) else None)),
        dict(type='text', fn=lambda S: f"模式长 `m = {S['m']}`，重复 `k = {S['k']}` 次，需要连续 `m×k = {S['m'] * S['k']}` 个数" if 'm' in S else '', size=30, h=70),
    ],
    watch=['index', 'i', 'j', 'now', 'next', ('flag', 'flag', 'green')],
    captions={
        'n = len(arr)': '`n = {n}`，模式要连续占 `m × k = {m * k}` 个位置',
        'for index in range(n)': '枚举模式的起点 `index = {index}`（数据很小，直接暴力）',
        'if index + m * k - 1 >= n': lambda S, B, r: (f'从 `{S.index}` 开始需要到下标 `{S.index + S.m * S.k - 1}`，超出 `n = {S.n}` → 更靠后的起点也不行，返回 False' if S.index + S.m * S.k - 1 >= S.n else f'到下标 `{S.index + S.m * S.k - 1}` < `n = {S.n}`：长度够，开始检查'),
        'flag = True': '先假设从 `{index}` 开始的模式成立',
        'for i in range(m)': '逐位检查模式的第 `{i}` 个数',
        'now = arr[index + i]': '模式第 `{i}` 位是 `now = {now}`',
        'next = arr[index + i + m * j]': '第 `{j}` 次重复的同一位：`arr[{index + i + m * j}]` = `{next}`',
        'if now != next': lambda S, B, r: (f'`{S.now} != {S.next}`：这一位没有重复 → 此起点失败' if S.now != S.next else f'`{S.now} == {S.next}`：这一位重复了，看下一次重复'),
        'flag = False': '标记此起点失败，`flag` = {flag}',
        'if not flag': lambda S, B, r: ('已失败 → 跳出，换下一个起点' if not S.flag else '目前都匹配，继续检查模式的下一位'),
        'if flag': lambda S, B, r: ('`flag` 为真：每一位都重复了 `k` 次 → 找到模式' if S.flag else '`flag` 为假：这个起点不行'),
        'break': '跳出当前循环：这个起点已经不可能成立',
        'return True': '从 `{index}` 开始有长度 `{m}` 重复 `{k}` 次的模式 → 返回 True',
    },
    cards=dict(
        one_liner='数据很小，枚举起点，逐位检查是否重复 k 次',
        complexity='时间 `O(n·m·k)`，空间 `O(1)`',
        problem=['给整数数组 `arr`，判断是否存在长度为 `m`、连续重复 `k` 次或更多的模式',
                 '模式是 `arr` 中连续的一段，重复之间不重叠、不间隔',
                 '本视频：`arr = [1,2,2,3,2,3,2,3]`，`m = 2`，`k = 3` → `True`'],
        quote='感觉可能可以用字符串相关的数据结构例如后缀数组来做，不过这里n、m、k的规模都很小，因此我直接使用的暴力法，枚举模式的起始位置，然后逐位进行检测。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举起点 `index`，模式占 `[index, index + m×k)`',
              '对模式的每一位 `i`，检查 `arr[index+i+m*j]` 是否都等于 `arr[index+i]`',
              '起点太靠后放不下 `m×k` 个数就直接返回 False'],
        summary=['时间 `O(n·m·k)`，空间 `O(1)`',
                 '易错点：边界 `index + m*k - 1 >= n` 要提前返回，否则下标越界',
                 '内层 break 只跳出 j 循环，还要再判断 `flag` 跳出 i 循环',
                 '原文已是 Python 3 可运行，仅删去了类型说明文档字符串'],
    ),
)
