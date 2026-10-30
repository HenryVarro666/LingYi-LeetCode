CONFIG = dict(
    num=1497, title='检查数组对是否可以被k整除', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='余数计数 · r 与 k−r 配对',
    tags=[],
    code='''
class Solution(object):
    def canArrange(self, arr, k):

        cnt_list = [0] * k
        for num in arr:
            cnt_list[num % k] += 1
        
        for r in range(1, (k + 1) // 2):
            if cnt_list[r] != cnt_list[k - r]:
                return False

        if k % 2 == 0 and cnt_list[k // 2] % 2 != 0:
            return False
        
        return True
''',
    call='Solution().canArrange([1,5,3,3,2,4,6,6], 6)',
    expect=True,
    views=[
        dict(type='array', var='arr', label='arr', cell=84, h=170),
        dict(type='array', var='cnt_list', label='cnt_list[r] = 余数为 r 的个数', cell=96, h=200,
             pointers={'r': 'pink'},
             ),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"配对：余数 `{S['r']}` 的有 `{S['cnt_list'][S['r']]}` 个，余数 `{S['k'] - S['r']}` 的有 `{S['cnt_list'][S['k'] - S['r']]}` 个"
                           if 'r' in S and 0 < S['r'] < S['k'] else '余数 r 的数只能配余数 k−r 的数（和为 k 的倍数）')),
    ],
    watch=[('k', 'k', 'yellow'), ('num', 'num', 'blue'), ('r', 'r', 'pink')],
    captions={
        'cnt_list = [0] * k': '余数只可能是 `0 … k-1`，准备 `{k}` 个计数器',
        'cnt_list[num % k] += 1': '`{num} % {k} = {num % k}` → 余数 `{num % k}` 的个数变成 `{cnt_list[num % k]}`',
        'for r in range': lambda S, B, rt: '`r` 的一半都查完了 → 循环结束' if 'r' in B and B['r'] == S.r else f'检查余数 `r = {S.r}` 与 `k - r = {S.k - S.r}`',
        'if cnt_list[r] != cnt_list[k - r]': lambda S, B, rt: (
            f'余数 `{S.r}` 有 {S.cnt_list[S.r]} 个，余数 `{S.k - S.r}` 有 {S.cnt_list[S.k - S.r]} 个：个数相等 → 刚好两两配完'
            if S.cnt_list[S.r] == S.cnt_list[S.k - S.r] else
            f'余数 `{S.r}` 有 {S.cnt_list[S.r]} 个，余数 `{S.k - S.r}` 有 {S.cnt_list[S.k - S.r]} 个：个数不等 → ==有人落单=='),
        'if k % 2 == 0 and': lambda S, B, rt: (
            f'`k` 是偶数，余数 `{S.k // 2}` 只能和自己配，个数 `{S.cnt_list[S.k // 2]}` 必须是偶数' if S.k % 2 == 0 else '`k` 是奇数，没有「自己配自己」的余数'),
        'return True': '所有余数都能配成对 → `True`',
    },
    cards=dict(
        one_liner='余数 r 只能配余数 k−r，个数必须一样多',
        complexity='时间 `O(n + k)`，空间 `O(k)`',
        problem=['整数数组 `arr`（长度为偶数）和整数 `k`',
                 '能否把数组分成若干对，使每对的和都能被 `k` 整除',
                 '示例：`[1,5,3,3,2,4,6,6]`，`k = 6` → `True`'],
        quote='对于一个数而言，其对k取模的余数必然是落在0到k - 1之间。不妨设其余数为r，那么就应该找一个余数为k - r的数来凑成一对。',
        quote_src='—— yiduobo 题解原文',
        idea=['先一趟扫描统计每种余数出现的次数',
              '`r` 与 `k-r` 的个数必须相等，否则必有落单的数',
              '`k` 为偶数时，余数 `k/2` 自己配自己，个数要为偶数',
              '其余情况都能配成对 → `True`'],
        summary=['时间 `O(n + k)`，空间 `O(k)`',
                 '易错：负数在 Python 里 `% k` 已经非负，C++/Java 要加 `k` 再取模',
                 '`range(1, (k + 1) // 2)` 只查 `r < k/2` 的一半，避免重复',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
