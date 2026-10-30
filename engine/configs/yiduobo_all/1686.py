CONFIG = dict(
    num=1686, title='石子游戏 VI', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='价值 = 自己得分 + 对手损失',
    tags=['博弈论', '难度分 2001'],
    code='''
class Solution(object):
    def stoneGameVI(self, aliceValues, bobValues):

        merge_list = sorted(zip(aliceValues, bobValues), key=lambda d:(d[0] + d[1]), reverse=True)
        alice = bob = 0
        for index in range(len(merge_list)):
            if index & 1:
                bob += merge_list[index][1]
            else:
                alice += merge_list[index][0]
        
        if alice > bob:
            return 1
        elif alice == bob:
            return 0
        else:
            return -1
''',
    call='Solution().stoneGameVI([2,4,3,5], [1,6,7,1])',
    expect=1,
    views=[
        dict(type='array', var='aliceValues', label='aliceValues', h=160),
        dict(type='array', var='bobValues', label='bobValues', h=160),
        dict(type='array', var=lambda S: [f'{x}+{y}={x+y}' for x, y in S['merge_list']] if 'merge_list' in S else [],
             label='merge_list：按 a+b 从大到小（蓝 = Alice 拿，粉 = Bob 拿）', cell=150, h=200,
             pointers={'index': 'yellow'},
             color=lambda S, i, v: ('blue' if i % 2 == 0 else 'pink') if 'index' in S and i <= S['index'] else None),
        dict(type='text', fn=lambda S: f"alice = =={S['alice']}==　　bob = =={S['bob']}==" if 'alice' in S else '', size=34, h=70),
    ],
    watch=[('index', 'index', 'yellow'), ('alice', 'alice', 'blue'), ('bob', 'bob', 'pink')],
    captions={
        'merge_list = sorted': '一块石头被 Alice 拿走，除了得 a，还让 Bob 拿不到 b → 价值看 `a+b`，从大到小排：`{[x + y for x, y in merge_list]}`',
        'alice = bob': '两人得分都从 0 开始',
        'if index & 1': lambda S, B, r: (f'`index = {S.index}` 是奇数 → 轮到 ==Bob==，拿这颗石头' if S.index % 2 else f'`index = {S.index}` 是偶数 → 轮到 ==Alice==，拿这颗石头'),
        'bob +=': 'Bob 得到 `{merge_list[index][1]}` 分：`bob` → =={bob}==',
        'alice +=': 'Alice 得到 `{merge_list[index][0]}` 分：`alice` → =={alice}==',
        'if alice > bob': '比较总分：`alice = {alice}`，`bob = {bob}` → {"Alice 更高" if alice > bob else "不是 Alice 更高，继续判断"}',
        'elif alice == bob': '`alice == bob` 吗？`{alice} == {bob}` → {"平局" if alice == bob else "不相等 → Bob 赢"}',
        'return 1': 'Alice 分数更高，返回 ==1==',
        'return 0': '分数相同，平局，返回 ==0==',
        'return -1': 'Bob 分数更高，返回 ==-1==',
    },
    cards=dict(
        one_liner='拿一块石头 = 自己的收益 + 对手失去的收益',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['Alice、Bob 轮流取石子，同一颗石子两人估值不同：`aliceValues[i]`、`bobValues[i]`',
                 '双方都最优，总分高者赢：Alice 赢 `1`，Bob 赢 `-1`，平局 `0`',
                 '示例：`[2,4,3,5]`、`[1,6,7,1]` → `1`'],
        quote='每块石子的价值可以认为是自己拿了这块石子的价值，加上对手不能拿这块石子的价值，也就是说对于第i块石子，其价值就是aliceValues[i] + bobValues[i]。',
        quote_src='—— yiduobo 题解原文',
        idea=['Alice 拿走石头 i：自己 `+a[i]`，同时 Bob 失去 `b[i]` 的机会',
              'Bob 也一样，所以两人眼里这颗石头都值 ==a+b==',
              '谁都想先拿价值高的 → 按 `a+b` 降序排好，Alice、Bob 轮流从头拿'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '排序键是 `a+b`，但累加的是各自的原始分：Alice 加 `a`，Bob 加 `b`',
                 '`index & 1` 判断奇偶：偶数位 Alice，奇数位 Bob',
                 '对比灵神：灵神把它写成 A−B 的增量，只用一个 diff；这里分别累计两人得分'],
    ),
)
