CONFIG = dict(
    num=3178, title='找出 K 秒后拿着球的孩子', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='周期取模 · 分段讨论', tags=[],
    code='''
class Solution(object):
    def numberOfChild(self, n, k):

        k %= (n - 1) * 2
        if k <= n - 1:
            return k
        else:
            return (n - 1) * 2 - k
''',
    call='Solution().numberOfChild(5, 6)',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: f"一个完整往返 = `(n−1)×2` = ==`{(S['n']-1)*2}`== 秒；现在 `k = {S['k']}`", size=30),
        dict(type='array', var=lambda S: list(range(S['n'])), pointers={'k': 'blue'}, label='孩子编号（蓝 = k 对应的位置，k > n−1 时要折回）', h=260),
        dict(type='text', fn=lambda S: f"右行阶段：`k ≤ {S['n']-1}`；左行阶段：`k > {S['n']-1}`", size=28),
    ],
    watch=[('n', 'n', 'blue'), ('k', 'k', 'yellow'), ('一圈', '(n - 1) * 2', 'pink')],
    captions={
        'k %= ': '每 `(n-1)×2 = {(n-1)*2}` 秒球回到 0 号、方向也恢复 → 只看余数：`k` = =={k}==',
        'if k <=': '`k = {k}` 与 `n - 1 = {n-1}`：{"k 不超过 n-1，球还在向右传" if k <= n - 1 else "k 超过 n-1，球已到过右端，正在向左传"}',
        'return k': '向右传了 `k` 次，球就在 ==`{ret}`== 号',
        'return (n': '向左传了 `k-(n-1)` 次，位置 `(n-1)-(k-(n-1)) = (n-1)×2-k` = ==`{ret}`== 号',
    },
    cards=dict(
        one_liner='每个往返一周期：先取模，再判断是在去程还是回程',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`n` 个孩子排成一排，0 号拿球向右传，每秒一次',
                 '到 `n-1` 号后改向左传，回到 0 号再向右，如此循环',
                 '示例：`n = 5, k = 6` → `2`'],
        quote='每经过(n - 1) * 2秒都会完成一次传球的循环，因此可以先将k对(n - 1) * 2取模。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n-1` 秒到右端，再 `n-1` 秒回左端，周期是 `(n-1)×2`',
              '余数 `k ≤ n-1`：还在去程，位置就是 `k`',
              '余数 `k > n-1`：已在回程，向左传了 `k-(n-1)` 次，位置 `(n-1)×2-k`'],
        summary=['时间、空间 `O(1)`',
                 '周期是 ==(n-1)*2== 而不是 n*2，端点的孩子只停留一秒',
                 '分界处 `k == n-1` 属于去程，两个公式结果相同',
                 '原文为 Python 2 风格（`class Solution(object)`），无需改动',
                 '对比灵神：灵神用 divmod 看趟数奇偶，yiduobo 直接按周期分段'],
    ),
)
