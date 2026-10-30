CONFIG = dict(
    num=989, title='数组形式的整数加法', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='翻转后模拟高精度加法',
    tags=[],
    code='''
class Solution(object):
    def addToArrayForm(self, A, K):

        l = len(A)
        A.reverse()
        A[0] += K
        now = 0
        while now + 1 < l and A[now] >= 10:
            A[now + 1] += A[now] // 10
            A[now] %= 10
            now += 1

        while A[-1] >= 10:
            A.append(A[-1] // 10)
            A[-2] %= 10
        
        A.reverse()

        return A
''',
    call='Solution().addToArrayForm([9, 9, 9], 15)',
    expect=[1, 0, 1, 4],
    views=[
        dict(type='text', fn=lambda S: ('数组 A 的低位在前（已翻转），下标 = 位权 `10^下标`' if 'l' in S else '数组形式：`[9,9,9]` 表示 999，再加 `K = 15`')),
        dict(type='array', var='A', pointers={'now': 'blue'}, h=300,
             color=lambda S, i, v: 'orange' if v >= 10 else None),
        dict(type='text', fn=lambda S: ('`A[now] = %s`，大于等于 10 就要进位' % S['A'][S['now']]) if 'now' in S and S['_line'] <= 11 and S['A'][S['now']] >= 10 else ''),
    ],
    watch=['l', ('now', 'now', 'blue'), 'K'],
    captions={
        'l = len(A)': '先记下原长度 `l = {l}`，后面的进位只在这 `l` 位内做',
        5: '翻转 `A`：低位放到下标 0，进位就是往==后==一格',
        'A[0] += K': '把 `K = {K}` 一次性加到最低位：`A[0]` = =={A[0]}==，可能超过 9',
        'now = 0': '`now` 指向当前要检查进位的位，从最低位开始',
        'while now + 1 < l': lambda S, B, r: (f'`now + 1 = {S.now + 1} < {S.l}` 且 `A[now] = {S.A[S.now]}` ' + ('≥ 10 → 要进位' if S.now + 1 < S.l and S.A[S.now] >= 10 else '→ 进位到此为止') if S.now + 1 < S.l else f'`now + 1 = {S.now + 1}` 已到最高位，不能再往后进位'),
        'A[now + 1] += A[now] // 10': '进位：高一位加 `{B.A[B.now] // 10}`，`A[{now + 1}]` = =={A[now + 1]}=='  ,
        'A[now] %= 10': '本位只留个位：`A[{now}]` = =={A[now]}==',
        'now += 1': '`now` 后移到 {now}，继续检查新的这一位',
        'while A[-1] >= 10': lambda S, B, r: (f'最高位 `A[-1] = {S.A[-1]}` ≥ 10 → 数组要变长' if S.A[-1] >= 10 else f'最高位 `A[-1] = {S.A[-1]}` < 10，不再进位'),
        'A.append': '最高位溢出：在末尾补一位 `{A[-1]}`（即原最高位的进位）',
        'A[-2] %= 10': '原最高位只留个位：`A[-2]` = =={A[-2]}==',
        17: '再翻转回高位在前',
        'return A': '结果 `{A}`，即 999 + 15 = 1014',
    },
    cards=dict(
        one_liner='先翻转，让低位在前，进位就是往后一格',
        complexity='时间 `O(n)`，空间 `O(1)`（不计结果）',
        problem=['整数 `num` 用数组 `A` 表示，高位在前；给定整数 `K`',
                 '返回 `num + K` 的数组形式',
                 '示例：`A=[9,9,9], K=15` → `[1,0,1,4]`'],
        quote='低配版本的高精度加法。为了方便起见，先将A翻转，此时较小的坐标值对应较低的位数，这样做的好处是方便最终进位。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把整个 `K` 加到最低位 `A[0]`，再从低往高扫一遍处理进位',
              '`A[now] >= 10`：高一位加 1（用 `//10`），本位对 10 取余',
              '扫到最高位还 >= 10，就在数组末尾补新的一位'],
        summary=['时间 `O(n)`；`K` 可能比 `A` 长，所以第二个循环可能补多位',
                 '易错：第一个循环要判断 `now + 1 < l`，防止越界',
                 '易错：最高位进位要 `append`，并且把旧最高位 `A[-2]` 取余',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
