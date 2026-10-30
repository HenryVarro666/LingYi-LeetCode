def _good(v):
    s = str(v)
    return not (set(s) & set('347')) and bool(set(s) & set('2569'))


def _nums(S):
    return list(range(1, S['N'] + 1))


def _color(S, i, v):
    # 已经计入 res 的好数标绿：前 res 个好数
    goods = [k for k in range(1, S['N'] + 1) if _good(k)]
    return 'green' if v in goods[:S.get('res', 0)] else None


def _info(S):
    if 'x' not in S:
        return '对每个 `x` 取出各位数字：碰到 3/4/7 就淘汰，见到 2/5/6/9 就记 `flag`'
    t = S.get('tmp')
    if t is None:
        return f'`x` 还剩 `{S["x"]}`，`flag = {S["flag"]}`'
    return f'刚取出末位 `tmp = {t}`，`x` 还剩 `{S["x"]}`，`flag = {S["flag"]}`'


CONFIG = dict(
    num=788, title='旋转数字', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='暴力枚举 + 逐位判断',
    tags=['灵神题单', '数位 DP'],
    code='''
class Solution(object):
    def rotatedDigits(self, N):

        res = 0
        for x in range(1, N + 1):
            flag = False
            while x:
                tmp = x % 10
                x //= 10
                if tmp in (3, 4, 7):
                    flag = False
                    break
                if tmp in (2, 5, 6, 9):
                    flag = True
            
            if flag:
                res += 1
        
        return res
''',
    call='Solution().rotatedDigits(10)',
    expect=4,
    views=[
        dict(type='array', var=_nums, label='1 ~ N（绿 = 已计入的好数）', cell=64, h=170, index=False, color=_color),
        dict(type='text', fn=_info, size=26, h=80),
    ],
    watch=[('x', 'x', 'blue'), ('tmp', 'tmp', 'pink'), ('flag', 'flag', 'yellow'), ('res', 'res', 'green')],
    max_steps=110,
    skip=['res = 0', 6, 'while x', 'x //= 10'],
    captions={
        'for x in range': lambda S, B, r: (f'取下一个数 `x = {S.x}`，检查它的每一位' if S.x else '1 到 N 都检查完了'),
        14: '见到变化的数字：`flag = True`（先记着，后面还可能遇到 3/4/7）',
        'tmp = x % 10': '`x % 10` 取出末位 `tmp = {tmp}`，`x //= 10` 去掉末位（原文 `/`）→ `x = {x // 10}`',
        'if tmp in (3, 4, 7)': lambda S, B, r: (f'`tmp = {S.tmp}` ∈ {{3,4,7}} → ==旋转后不是数字==，这个数不可能是好数'
                                              if S.tmp in (3, 4, 7) else f'`tmp = {S.tmp}` 不是 3/4/7，没问题'),
        11: '`flag = False` 并 `break`：这个数直接淘汰',
        'if tmp in (2, 5, 6, 9)': lambda S, B, r: (f'`tmp = {S.tmp}` 旋转后==变成别的数字== → 至少有一位不同，`flag = True`'
                                                 if S.tmp in (2, 5, 6, 9) else f'`tmp = {S.tmp}`（0/1/8）旋转后不变，不影响 `flag`'),
        'if flag': lambda S, B, r: (f'`flag = True` → 全是有效数字且有变化，==是好数==' if S.flag
                                    else '`flag = False` → 要么含 3/4/7，要么旋转后不变，==不是好数=='),
        'res += 1': '好数 +1：`res = {res}`',
        'return res': '1 到 {N} 中共有 =={ret}== 个好数',
    },
    cards=dict(
        one_liner='3/4/7 一票否决，至少有一个 2/5/6/9 才行',
        complexity='时间 `O(N log N)`，空间 `O(1)`',
        problem=['数字每位旋转 180 度仍是有效数字，且和原数不同，就是好数',
                 '0/1/8 不变，2↔5，6↔9，其余无效；数 `1` 到 `N` 里有几个好数',
                 '示例：`N = 10` → `4`；演示即这个例子（2、5、6、9）'],
        quote='判断的依据是对于一个数，若其各位数字中不包含3、4、7，且至少有2、5、6、9其中一个，那么这个数字就是好数。',
        quote_src='—— yiduobo 题解',
        idea=['作者先想到：各位独立，可以从低位开始做 DP',
              '但 `N ≤ 10000`，直接 ==遍历 1 到 N== 更省事',
              '每个数拆出每位数字，用 `flag` 记录是否见过 2/5/6/9'],
        summary=['时间 `O(N log N)`：N 个数，每个拆 `log N` 位',
                 '易错：遇到 3/4/7 要 `flag = False` 再 `break`，否则前面的 `flag = True` 会残留',
                 '原文为 Python 2 写法，整数除法 `x /= 10` 已改为 `x //= 10`',
                 '数据再大就要用数位 DP（灵神题解的做法）'],
    ),
)
