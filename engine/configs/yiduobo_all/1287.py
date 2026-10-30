ARR = [1, 2, 2, 6, 6, 6, 6, 7, 10]


def _k(S):
    """index in arr of the element `num` being scanned (loop is over arr[1:], no index variable)"""
    if 'num' not in S or 'now' not in S:
        return None
    arr, ln = S['arr'], S['_line']
    if ln == 15:
        return arr.index(S['num'])
    st = arr.index(S['now'])
    return st + S['cnt'] if ln in (9, 10) else st + S['cnt'] - 1


def _seg(S):
    if 'now' not in S:
        return None
    arr = S['arr']
    if S['_line'] == 15:
        k = arr.index(S['now'])
        return k, k
    st = arr.index(S['now'])
    return st, st + S['cnt'] - 1


def _color(S, i, v):
    sg = _seg(S)
    if sg is None:
        return None
    if sg[0] <= i <= sg[1]:
        return 'green' if S['_line'] == 13 else 'blue'
    return None


def _top(S):
    sg = _seg(S)
    if sg is None:
        return '有序数组：相等的元素==连续==，数一数每一段有多长'
    n = len(S['arr'])
    return f"当前段：值 `{S['now']}`，长度 `cnt = {S['cnt']}`；需要 `cnt × 4 > {n}`，即 `cnt >= {n // 4 + 1}`"


CONFIG = dict(
    num=1287, title='有序数组中出现次数超过25%的元素', difficulty='Easy', category='二分算法',
    author='yiduobo', technique='一趟扫描统计连续段长度',
    tags=['灵神核心路线', '灵神题单·二分算法'],
    code='''
class Solution(object):
    def findSpecialInteger(self, arr):

        n = len(arr)
        if n == 1:
            return arr[0]
        now = arr[0]
        cnt = 1
        for num in arr[1:]:
            if now == num:
                cnt += 1
                if cnt * 4 > n:
                    return now
            else:
                now = num
                cnt = 1
''',
    call=f'Solution().findSpecialInteger({ARR})',
    expect=6,
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='array', var='arr', label='arr（蓝 = 当前统计的连续段 now，箭头 = 正在扫描的 num）', cell=90, color=_color,
             pointers={_k: 'yellow'}, pointer_labels={_k: 'num'}, h=300),
    ],
    watch=['n', ('now', 'now', 'blue'), ('num', 'num', 'yellow'), ('cnt', 'cnt', 'green'),
           ('cnt * 4', lambda S: S['cnt'] * 4 if 'cnt' in S else None, 'pink')],
    captions={
        'n = len': '`n = {n}`',
        'if n == 1': '`n = {n}` 不是 1（只有一个数时它本身就是答案）',
        'now = arr[0]': '`now`：当前正在统计的值，从 `arr[0] = {now}` 开始',
        8: '`cnt = 1`：`now` 目前连续出现了 1 次',
        'for num in arr[1:]': lambda S, B, r: f'扫描下一个数 `num = {S.num}`（从 `arr[1]` 开始，arr[0] 已作为 now）',
        'if now == num': lambda S, B, r: (f'`num = {S.num} == now`：和前一段相同 → 段长 +1' if S.now == S.num else f'`num = {S.num} ≠ now = {S.now}`：有序数组里 `{S.now}` 这一段结束了'),
        'cnt += 1': '`cnt` → {cnt}',
        'if cnt * 4 > n': lambda S, B, r: (f'`{S.cnt} × 4 = {S.cnt * 4} > {S.n}`：出现次数超过 25%！' if S.cnt * 4 > S.n else f'`{S.cnt} × 4 = {S.cnt * 4} <= {S.n}`：还不够 25%'),
        'return now': '返回 =={ret}==',
        'now = num': '换成统计新值 `now = {now}`',
        16: '新的一段，`cnt` 重置为 1',
    },
    cards=dict(
        one_liner='有序 → 相等元素连续：一趟扫描数连续段长度',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['非递减数组 `arr` 中恰好有一个整数出现次数 ==超过 25%==，返回它',
                 '示例：`[1,2,2,6,6,6,6,7,10]` → `6`'],
        quote='注意到题目给出的数组已经排好序了，那么说明==相等的元素在数组中是连续的==……若某一时刻cnt * 4大于数组长度，说明now就是最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['`now` 记当前段的值，`cnt` 记当前段的长度',
              '`num == now` 就 `cnt += 1`；否则换新段，`cnt` 重置为 1',
              '用 `cnt * 4 > n` 判断超过 25%，避免浮点除法'],
        summary=['时间 `O(n)`，空间 `O(1)`（`arr[1:]` 切片另占 `O(n)`）',
                 '`n == 1` 要特判：循环一次都不执行，否则会没有返回值',
                 '只在 `cnt` 增加时检查：`n >= 2` 时答案至少出现 2 次，一定会走到这里',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行',
                 '对比灵神：利用有序性只检查 3 个下标 + 二分，做到 `O(log n)`'],
    ),
)
