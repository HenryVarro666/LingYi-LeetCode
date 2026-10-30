def _cmp_txt(S):
    if S.get('_line') in (19, 20, 23) and 'com_res' in S:
        r = S['reader'].arr
        a, b = sum(r[S['left']:S['p1'] + 1]), sum(r[S['p1'] + 1:S['p2'] + 1])
        return f"左份 [{S['left']}..{S['p1']}] 和 = {a}　右份 [{S['p1']+1}..{S['p2']}] 和 = {b}"
    if 'left' in S and 'right' in S:
        return f"候选区间 [{S['left']}, {S['right']}]，共 {S['right']-S['left']+1} 个数"
    return ''


CONFIG = dict(
    num=1533, title='找到最大整数的索引', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='三分查找 · 比较前两份的和',
    tags=['二分算法', '贪心与思维'],
    setup='''
class ArrayReader(object):
    # 题目给的交互 API：数组里只有一个数更大，其余都相等
    def __init__(self, arr):
        self.arr = arr

    def compareSub(self, l, r, x, y):
        a, b = sum(self.arr[l:r + 1]), sum(self.arr[x:y + 1])
        return 1 if a > b else (0 if a == b else -1)

    def length(self):
        return len(self.arr)
''',
    code='''
class Solution(object):
    def getIndex(self, reader):

        n = reader.length()

        left = 0
        right = n - 1
        while left < right:
            if left == right - 1:
                if reader.compareSub(left, left, right, right) > 0:
                    right = left
                else:
                    left = right

            else:
                part_len = (right - left + 1) // 3
                p1 = left + part_len - 1
                p2 = p1 + 1 + part_len - 1
                com_res = reader.compareSub(left, p1, p1 + 1, p2)
                if com_res == -1:
                    left = p1 + 1
                    right = p2
                elif com_res == 0:
                    left = p2 + 1
                else:
                    right = p1

        return left
''',
    call='Solution().getIndex(ArrayReader([6,6,6,6,6,6,9,6,6,6,6,6]))',
    expect=6,
    views=[
        dict(type='array', var=lambda S: S['reader'].arr if 'reader' in S else None, label='隐藏数组（只能用 compareSub 比较区间和；蓝框 = 候选区间）',
             cell=70, h=300, window=('left', 'right'),
             pointers={'left': 'blue', 'right': 'pink'},
             dim=lambda S, i, v: 'left' in S and not (S['left'] <= i <= S['right'])),
        dict(type='text', fn=_cmp_txt, size=26, h=120),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'part_len', 'p1', 'p2', 'com_res'],
    captions={
        'n = reader.length()': '`n = {n}`：只知道长度，看不到数值',
        'left = 0': '候选区间一开始是整个数组：`left = 0`',
        'right = n - 1': '`right = {right}`',
        'while left < right': lambda S, B, r: (f'区间还有 `{S.right - S.left + 1}` 个数，最大数未定 → 继续' if S.left < S.right
                                              else f'区间只剩下标 `{S.left}`，它就是最大数 → 结束'),
        'if left == right - 1': lambda S, B, r: ('只剩两个数：不能再分三份，直接比较这两个' if S.left == S.right - 1
                                                 else f'剩 `{S.right - S.left + 1}` 个数（>= 3）→ 均分三份'),
        'reader.compareSub(left, left, right, right) > 0': lambda S, B, r: (
            f'比较 `arr[{S.left}]` 和 `arr[{S.right}]`：左边更大 → 最大数是 ==left=={S.left}' if S.reader.compareSub(S.left, S.left, S.right, S.right) > 0
            else f'左边不更大 → 最大数是 ==right=={S.right}'),
        'right = left': '最大数在左边：`right = left = {right}`',
        'left = right': '最大数在右边：`left = right = {left}`',
        'part_len =': '每份 `(right - left + 1) // 3 = {part_len}` 个，前两份数量必须相同',
        'p1 =': '第一份是 `[{left}, {p1}]`',
        'p2 =': '第二份是 `[{p1 + 1}, {p2}]`，剩下的是第三份',
        'com_res = ': lambda S, B, r: ('比较前两份的和：`' + str(S.com_res) + '`，' +
                                       {-1: '右份更大 → 最大数在第二份', 0: '两份相等 → 最大数在第三份（落单部分）', 1: '左份更大 → 最大数在第一份'}[S.com_res]),
        'if com_res == -1': lambda S, B, r: ('`com_res == -1`：第二份更重 → 成立' if S.com_res == -1 else '`com_res` 不是 -1 → 看下一个分支'),
        'left = p1 + 1': '第二份更重：区间缩到第二份 `[{left}, {p2}]`',
        'right = p2': '`right = {right}`',
        'elif com_res == 0': lambda S, B, r: ('`com_res == 0`：前两份一样重 → 最大数不在其中' if S.com_res == 0 else '`com_res` 是 1 → 走 else'),
        'left = p2 + 1': '丢掉前两份：`left = p2 + 1 = {left}`，区间缩到第三份',
        'right = p1': '第一份更重：`right = p1 = {right}`',
        'return left': '区间只剩一个数，答案是下标 `{left}`',
    },
    cards=dict(
        one_liner='把区间切成三份，称前两份：轻重一比就丢掉三分之二',
        complexity='时间 `O(log3 n)` 次比较，空间 `O(1)`',
        problem=['数组里只有一个数比其他都大，其余全相等，看不到数值',
                 '只能调用 `compareSub(l, r, x, y)` 比较两段的和，返回 1 / 0 / -1',
                 '本视频：长度 12，最大数在下标 6'],
        quote='当剩余的数大于等于三个时，可以将这些数均分成三份，且必须保证前两份数的数量相同。',
        quote_src='—— yiduobo 题解原文',
        idea=['前两份一样长，比和：==更重的那份有最大数==',
              '两份相等 → 最大数在落单的第三份',
              '只剩两个数时直接比较这两个，每轮规模缩到约三分之一'],
        summary=['比较次数约 `log3 n`，比普通二分的 `log2 n` 更少',
                 '三份时前两份必须等长，才能靠相等判断第三份',
                 '剩 2 个数要单独处理，否则 `part_len = 0` 会死循环',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`；`ArrayReader` 在 `setup` 里按题目接口补全，并去掉了注释里的接口说明'],
    ),
)
