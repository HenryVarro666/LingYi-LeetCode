NUMS = [3, 1, 2, 5, 3, 6]
N = len(NUMS)


def IDX(S):
    """代码里没有下标：已处理个数 = 集合大小 + 已发现的重复个数"""
    if 'num_set' not in S or 'num' not in S:
        return None
    p = len(S['num_set']) + (1 if 'repeat' in S else 0)
    p -= 1 if S.get('_line') in (7, 9, 10) else 0
    return p if p < N else None


def _nums_color(S, i, v):
    k = IDX(S)
    if k is None:
        return None
    if i == k:
        return 'red' if S.get('_line') == 7 else 'blue'
    return None


def _one_to_n_color(S, i, v):
    st = S.get('num_set') or set()
    if v in st:
        return 'green'
    if S.get('_line') == 12:
        return 'red'
    return None


def _info(S):
    if 's' not in S:
        return f'`1 ~ {N}` 中：一个数重复了一次，另一个数丢失了'
    tot = N * (N + 1) // 2
    if S.get('_line') == 12:
        return f'缺失的数 = `(1+…+{N}) − s = {tot} − {S["s"]}` = =={tot - S["s"]}=='
    rep = f"，重复的数 `repeat = {S['repeat']}`" if 'repeat' in S else ''
    return f"不重复数字之和 `s = {S['s']}`{rep}"


def _if_cap(S, B, ret):
    if S.num in B.num_set:
        return f'`{S.num}` ==已经在集合里== → 它就是出现了两次的数'
    return f'`{S.num}` 第一次出现 → 放进集合，并累加到 `s`'


def _ret_cap(S, B, ret):
    tot = N * (N + 1) // 2
    return f'`1+2+…+{N} = {tot}`，减去不重复数字之和 `{S.s}` → 缺失 `{tot - S.s}`；返回 =={ret}=='


CONFIG = dict(
    num=645, title='错误的集合', difficulty='Easy', category='哈希',
    author='yiduobo', technique='哈希集合 + 求和',
    tags=['字节30天'],
    code='''
class Solution(object):
    def findErrorNums(self, nums):
        num_set = set()
        s = 0
        for num in nums:
            if num in num_set:
                repeat = num
            else:
                num_set.add(num)
                s += num

        return [repeat, len(nums) * (len(nums) + 1) // 2 - s]
''',
    call=f'Solution().findErrorNums({NUMS})',
    expect=[3, 4],
    views=[
        dict(type='text', h=60, fn=_info, size=27),
        dict(type='array', var='nums', label='nums（蓝 = 当前数，红 = 发现重复）', cell=84,
             pointers={IDX: 'blue'}, pointer_labels={IDX: 'num'}, color=_nums_color),
        dict(type='set', var='num_set', label='num_set（出现过的数字）', h=120, font=30),
        dict(type='array', var=lambda S: list(range(1, N + 1)), label=f'1 ~ {N}（绿 = 出现过；最后剩下的就是缺失的数）', cell=84,
             color=_one_to_n_color, index=False),
    ],
    watch=[('num', 'num', 'blue'), ('s', 's', 'cyan'), ('repeat', 'repeat', 'red')],
    captions={
        'num_set = set()': '哈希集合 `num_set` 记录出现过的数字',
        's = 0': '`s`：==不重复==的所有数字之和',
        'for num in nums': lambda S, B, ret: (f'下一个数 `num = {S.num}`' if IDX(S) is not None else '一趟扫描结束'),
        'if num in num_set': _if_cap,
        'repeat = num': '记下重复的数 `repeat = {repeat}`（它==不累加==到 `s`）',
        'num_set.add(num)': '`{num}` 加入集合',
        's += num': '`s += {num}` → `{s}`',
        'return': _ret_cap,
    },
    cards=dict(
        one_liner='哈希集合找出重复的数；1~n 之和减去不重复数字之和就是丢失的数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['集合 `s` 本应包含 `1 ~ n`，但某个数字被复制成了另一个数字的值',
                 '于是==一个数重复、一个数丢失==；给你出错后的 `nums`，返回 `[重复的数, 丢失的数]`',
                 '示例：`[1,2,2,4]` → `[2,3]`；`[1,1]` → `[1,2]`',
                 '本视频：`[3,1,2,5,3,6]` → `[3,4]`'],
        quote='比较基础的题目，一趟扫描，用哈希表判断哪个数字出现了两次，然后==1到n这些数字之和减去不重复的所有数字之和就是缺失的数字==。',
        quote_src='—— yiduobo 题解原文',
        idea=['扫描时用集合判重：==第二次见到==的数就是 `repeat`',
              '第一次见到的数才累加进 `s`，所以 `s` = 不重复数字之和',
              '`1 ~ n` 每个数恰好一次的和是 `n(n+1)/2`，差值就是丢失的数'],
        result='运行结束，返回 `[3, 4]`：3 出现两次，4 没出现',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，`n*(n+1)/2` 的 `/` 已改为 `//`（否则返回浮点数），并删去了 docstring',
                 '易错：`s` 只能累加==第一次出现==的数，重复的那次不能加',
                 '进阶：用 `sum(nums) − sum(set(nums))` 得重复数，或原地标记 / 异或做到 `O(1)` 空间'],
    ),
)
