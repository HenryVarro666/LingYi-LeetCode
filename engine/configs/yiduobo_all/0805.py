CONFIG = dict(
    num=805, title='数组的均值分割', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='减去平均数 + 折半枚举子集和',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def splitArraySameAverage(self, A):

        n = len(A)
        if n == 1:
            return False
        A = [x * n for x in A]
        avg = sum(A) // n
        A = [x - avg for x in A]
        s_first = sum(A[:n//2])
        s_second = sum(A[n//2:])
        first_set = set([0])
        for now in A[:n//2]:
            for num in list(first_set):
                tmp = now + num
                if tmp == 0:
                    return True
                first_set.add(tmp)
        
        second_set = set([0])
        for now in A[n//2:]:
            for num in list(second_set):
                tmp = now + num
                if tmp == 0:
                    return True
                if -tmp in first_set and (tmp != s_second or -tmp != s_first):
                    return True
                second_set.add(tmp)
        
        return False
''',
    call='Solution().splitArraySameAverage([1,2,3,4,5,6])',
    expect=True,
    views=[
        dict(type='array', var='A', label='A（已乘 n 再减去平均数，找若干个数和为 0）', cell=100, h=170,
             pointers={'n//2': 'pink'}, index=True),
        dict(type='set', var='first_set', label='first_set（前半部分所有子集和）', h=150, font=28),
        dict(type='set', var='second_set', label='second_set（后半部分所有子集和）', h=150, font=28),
        dict(type='text', h=90, size=28, fn=lambda S: (
            f'`now = {S["now"]}`，`num = {S["num"]}`，`tmp = now + num = {S["tmp"]}`'
            if 'tmp' in S and 'num' in S and 'now' in S else '目标：找到非空、非全选的子集，使和为 ==0==')),
    ],
    watch=[('n', 'n', 'blue'), ('avg', 'avg', 'orange'), ('now', 'now', 'cyan'), ('tmp', 'tmp', 'pink'), ('s_second', 's_second', 'green')],
    captions={
        'n = len(A)': '共 `{n}` 个数',
        'if n == 1': lambda S, B, r: ('只有 1 个数，没法分成两个非空数组 → False' if S.n == 1 else f'`n = {S.n}`，不止 1 个数，继续'),
        'A = [x * n': '全部乘上 `n = {n}`：这样平均数一定是整数，结果不受影响',
        'avg = sum(A)': '平均数 `avg = sum(A) // n = {avg}`',
        'A = [x - avg': '每个数减去平均数：现在只需找一组数==和为 0==，A = `{A}`',
        's_first = ': '前半部分全选的和 `s_first = {s_first}`，后面用来排除“全选”的情况',
        's_second = ': '后半部分全选的和 `s_second = {s_second}`',
        'first_set = set': '`first_set` 记录前半部分所有可能的子集和，初始只有空集 `0`',
        'second_set = set': '`second_set` 记录后半部分所有可能的子集和，初始只有空集 `0`',
        'for now in A[:n//2]': '前半部分：取下一个数 `now`，把它并入所有已有子集和（取完就轮到后半部分）',
        'for now in A[n//2:]': '后半部分：取下一个数 `now`，同样并入已有子集和，并去 first_set 里找 `-tmp`',
        'for num in list': '遍历已有的子集和（先 `list` 拷贝一份，边遍历边加入也不会乱），每个都加上 `now`',
        'tmp = now + num': '`tmp = {now} + {num} = {tmp}`：把 `now` 加入这个子集',
        'if tmp == 0': lambda S, B, r: ('`tmp = 0`：找到和为 0 的非空子集 → True' if S.tmp == 0
                                        else f'`tmp = {S.tmp} ≠ 0`，继续'),
        'first_set.add': '`first_set` 加入 `{tmp}`',
        'second_set.add': '`second_set` 加入 `{tmp}`',
        'if -tmp in first_set': lambda S, B, r: (
            f'`-tmp = {-S.tmp}` 在 first_set 中，且不是“两半都全选”→ 两边凑出和 0 → True'
            if (-S.tmp in S.first_set and (S.tmp != S.s_second or -S.tmp != S.s_first))
            else f'`-tmp = {-S.tmp}` 不在 first_set 中（或是两半全选）→ 凑不出，继续'),
        'return True': '找到了 → 可以分成平均值相同的两部分',
        'return False': '没有找到 → False',
    },
    cards=dict(
        one_liner='B 的平均数 = A 的平均数，转成：找若干数和为 0',
        complexity='时间 `O(n·2^(n/2))`，空间 `O(2^(n/2))`',
        problem=['把数组 `A` 拆成非空的 `B`、`C`，使两者平均值相等',
                 '能拆返回 `True`，否则 `False`',
                 '本视频：`[1,2,3,4,5,6]` → `True`'],
        quote='题目可以转化成从集合A中找出若干个数，使这些数的平均数恰好等于所有数的平均数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`B` 与 `C` 均值相等，等价于 `B` 的均值等于整体均值',
              '全部乘 `n` 再减去均值，问题变成：非空且不全选的子集，和是否为 0',
              '30 个数太多，拆成前后两半各自枚举子集和，用集合做“两数之和”'],
        summary=['时间 `O(n·2^(n/2))`，比直接枚举 `2^n` 快得多',
                 '先乘 `n` 再减均值，避免小数',
                 '“全选”不合法：后半的和为 `s_second`、前半为 `s_first` 时要排除',
                 '原文为 Python 2 写法，`/` 整数除法已改为 `//`'],
    ),
)
