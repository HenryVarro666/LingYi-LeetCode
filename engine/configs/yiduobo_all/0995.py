CONFIG = dict(
    num=995, title='K 连续位的最小翻转次数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='贪心 · 差分标记',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Solution(object):
    def minKBitFlips(self, A, K):

        n = len(A)
        end_pos = [0] * n
        reverse_cnt = 0
        res = 0
        for index, num in enumerate(A):
            if (num + reverse_cnt) % 2 == 0:
                if index >= n - K + 1:
                    return -1
                reverse_cnt += 1
                res += 1
                end_pos[index + K - 1] = 1
            
            reverse_cnt -= end_pos[index]
        
        return res
''',
    call='Solution().minKBitFlips([0,0,0,1,0,1,1,0], 3)',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"下标 `{S['index']}`：原值 `{S['num']}` + 已翻 `{S['reverse_cnt']}` 次 → 当前 ==`{(S['num'] + S['reverse_cnt']) % 2}`==" if 'index' in S and 'num' in S and 'reverse_cnt' in S else ''), size=28),
        dict(type='array', var='A', label='A（蓝 = 当前考察位）', h=190, pointers={'index': 'blue'},
             color=lambda S, i, v: 'blue' if 'index' in S and i == S['index'] else None),
        dict(type='array', var='end_pos', label='end_pos（1 = 某次翻转在此结束）', h=190,
             color=lambda S, i, v: 'orange' if v == 1 else None),
    ],
    watch=[('index', 'index', 'blue'), 'num', ('reverse_cnt', 'reverse_cnt', 'pink'), ('res', 'res', 'green'), 'K'],
    captions={
        'end_pos = [0]': '`end_pos[i] = 1` 表示有一次翻转在下标 `i` 结束，到这里要把翻转计数减一',
        'reverse_cnt = 0': '`reverse_cnt`：当前位置已经被覆盖的翻转次数（相当于差分的前缀和）',
        'for index, num': '考察 `A[{index}] = {num}`',
        'if (num + reverse_cnt) % 2 == 0': lambda S, B, r: (
            f'`({S.num} + {S.reverse_cnt}) % 2 == 0`：被翻 `{S.reverse_cnt}` 次后这一位是 ==0==，必须翻' if (S.num + S.reverse_cnt) % 2 == 0
            else f'`({S.num} + {S.reverse_cnt}) % 2 = 1`：这一位已经是 ==1==，不用翻'),
        'if index >= n - K + 1': lambda S, B, r: (f'`{S.index} >= {S.n - S.K + 1}`：后面不足 `K` 位，翻不了 → 无解' if S.index >= S.n - S.K + 1
                                                  else f'`{S.index} < {S.n - S.K + 1}`：后面还够 `K = {S.K}` 位，可以翻'),
        'reverse_cnt += 1': '翻转从这里开始，`reverse_cnt` → {reverse_cnt}（后面 `K` 位都受影响）',
        'res += 1': '这一位必须翻，没有别的选择 → 操作数 `res` = {res}',
        'end_pos[index + K - 1] = 1': '翻转覆盖 `{index}..{index + K - 1}`，在 `{index + K - 1}` 打结束标记',
        'reverse_cnt -= end_pos[index]': lambda S, B, r: (f'`end_pos[{S.index}] = 1`：有一次翻转到这里结束，`reverse_cnt` → {S.reverse_cnt}' if S.end_pos[S.index]
                                                         else f'`end_pos[{S.index}] = 0`：没有翻转结束，`reverse_cnt` 保持 {S.reverse_cnt}'),
        'return -1': '剩下的位置凑不够 `K` 位还需要翻 → 返回 `-1`',
        'return res': '扫完所有位置，最少翻转 `{res}` 次',
    },
    cards=dict(
        one_liner='从左到右遇到 0 就翻，用标记 O(1) 知道当前位被翻过几次',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`A` 是 0/1 数组，一次操作可翻转长度恰为 `K` 的连续子数组（0 变 1，1 变 0）',
                 '返回让数组全为 1 的最少翻转次数，做不到返回 `-1`',
                 '示例：`A=[0,0,0,1,0,1,1,0]`，`K=3` → `3`'],
        quote='若我们在之前的某处A[j]进行了翻转，我们就应该将cnt加上1，同时在A[j + k - 1]设置标记，当处理到A[j + k - 1]时，由A[j]带来的这次翻转就结束了。',
        quote_src='—— yiduobo 题解原文',
        idea=['最左边的 0 只能靠以它为起点的翻转变成 1 → 翻转方案是==唯一确定==的',
              '直接模拟每次翻 `K` 位是 `O(nK)`；改为维护 `reverse_cnt` 表示被翻过几次',
              '翻转起点处 `+1`，结束位置打标记、处理到那里再 `-1`，每位只需 `O(1)`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`(num + reverse_cnt) % 2 == 0` 才需要翻：翻偶数次等于没翻',
                 '`index >= n - K + 1` 时不足 `K` 位，直接返回 `-1`',
                 '先判断翻转，再 `reverse_cnt -= end_pos[index]`：结束标记在覆盖区间的最后一位之后才生效',
                 '原文已是 Python 3 可运行写法，无需修改'],
    ),
)
