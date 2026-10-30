_P = [False] * 2 + [True] * 99
for _i in range(2, 11):
    if _P[_i]:
        for _j in range(_i * _i, 101, _i):
            _P[_j] = False


def _ptxt(S):
    cnt = S.get('cnt')
    if cnt is None:
        return '`is_prime[c]`：==c 是质数吗==？预处理好的筛表，1 不是质数'
    items = []
    for k, c in cnt.items():
        items.append(f"`{k}` 出现 {c} 次（{'==质数==' if _P[c] else '非质数'}）")
    return '；'.join(items)


CONFIG = dict(
    num=3591, title='检查元素频次是否为质数', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='埃氏筛 + 哈希表计数',
    tags=['灵神题单·数学算法', '数学算法', '难度分 1235'],
    code='''
MX = 101
is_prime = [False] * 2 + [True] * (MX - 2)
for i in range(2, isqrt(MX) + 1):
    if is_prime[i]:
        for j in range(i * i, MX, i):
            is_prime[j] = False  # j 是质数 i 的倍数

class Solution:
    def checkPrimeFrequency(self, nums: List[int]) -> bool:
        cnt = Counter(nums)
        return any(is_prime[c] for c in cnt.values())
''',
    call='Solution().checkPrimeFrequency([5,5,5,5,6,6,6])',
    expect=True,
    views=[
        dict(type='array', var='nums', label='nums', h=170, cell=90),
        dict(type='map', var='cnt', label='cnt（元素 → 频次）', fmt=lambda k, v: f'{k}: {v}', h=170, font=34),
        dict(type='text', size=28, h=120, fn=_ptxt),
        dict(type='text', size=26, h=90, fn=lambda S: '100 以内的质数：`2 3 5 7 11 13 17 19 23 29 ...`，频次 1、4、6、8、9 都不是'),
    ],
    watch=[('MX', 'MX'), ('i', 'i', 'blue'), ('j', 'j', 'pink')],
    max_steps=60,
    captions={
        'MX = 101': '频次最大 100（`nums.length <= 100`），所以筛到 ==100==，`MX = 101`',
        'is_prime = [False]': '先假设 `2..100` 都是质数，`0` 和 `1` ==不是质数==（注意 1）',
        'for i in range': '`i` 只需枚举到 `isqrt(MX) = 10`：合数必有不超过根号的因子',
        'if is_prime[i]': lambda S, B, r: (f'`{S.i}` 是质数，把它的倍数划掉' if S.is_prime[S.i] else f'`{S.i}` 已被划掉（是合数），它的倍数早被更小的质数划过'),
        'for j in range': '倍数从 `i*i` 开始：更小的倍数已被更小的质数划掉',
        'is_prime[j] = False': '`{j}` 是质数 `{i}` 的倍数 → 合数',
        'cnt = Counter': '`cnt` 统计每个元素的出现次数：`{dict(cnt)}`',
        'return any': lambda S, B, r: '只要有一个频次是质数就返回 `True`：' + '，'.join(f'频次 {c} → {"质数" if _P[c] else "非质数"}' for c in S.cnt.values()) + f'，结果 =={r}==',
    },
    cards=dict(
        one_liner='筛出质数表，再看有没有频次落在质数上',
        complexity='时间 `O(n)`，空间 `O(n)`（不计预处理）',
        problem=['元素 `x` 的==频次==是它在数组中出现的次数',
                 '只要有任一元素的频次是质数，就返回 `true`',
                 '示例：`[1,2,3,4,5,4]` → `true`（4 出现 2 次）',
                 '本视频：`[5,5,5,5,6,6,6]` → `true`（6 出现 3 次）'],
        quote='用埃氏筛（或者欧拉筛）预处理一个布尔数组，表示哪些数是质数。……注意 1 不是质数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`nums.length <= 100`，频次不超过 100，先筛出 100 以内的质数',
              '用 `Counter` 数出每个元素的频次',
              '`any(is_prime[c] ...)` 查表，一旦找到就返回 `True`'],
        before=[dict(heading='预处理：埃氏筛', lines=['先假设 `2..100` 全是质数，`0`、`1` 标成非质数', '遇到质数 `i`，把 `i*i, i*i+i, ...` 全部划掉', '`i` 只需枚举到 `isqrt(101) = 10`', '筛完后 `is_prime[c]` 就是 O(1) 的质数查询']),
                dict(heading='为什么频次最大是 100', lines=['`nums.length <= 100`，一个元素最多出现 100 次', '所以只要筛 `[0, 100]`，`MX = 101`', '数组下标 `c` 就是频次 `c`'])],
        summary=['时间 `O(n)`，空间 `O(n)`；预处理只做一次，不计入',
                 '易错点：==1 不是质数==，频次 1 的元素不能算',
                 '数据范围很小，也可以不筛，现场逐个判断质数',
                 '同类题：204. 计数质数，3618. 根据质数下标分割数组'],
    ),
)
