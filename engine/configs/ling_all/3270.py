CONFIG = dict(
    num=3270, title='求出数字答案', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='逐位取最小 · 到某数为 0 停止',
    code='''
class Solution:
    def generateKey(self, x: int, y: int, z: int) -> int:
        ans = 0
        pow10 = 1
        while x and y and z:
            ans += min(x % 10, y % 10, z % 10) * pow10
            x //= 10
            y //= 10
            z //= 10
            pow10 *= 10
        return ans
''',
    call='Solution().generateKey(987, 879, 798)',
    expect=777,
    views=[
        dict(type='text', h=70, fn=lambda S: (f"当前最低位：`min({S['x']%10}, {S['y']%10}, {S['z']%10})` = =={min(S['x']%10, S['y']%10, S['z']%10)}==，权重 `{S['pow10']}`" if 'pow10' in S and S['x'] and S['y'] and S['z'] else ('有一个数已经是 0，后面各位最小值都是 0' if 'pow10' in S else ''))),
        dict(type='array', var=lambda S: [S['x'], S['y'], S['z']], pointers={}, h=200, label='x, y, z（每轮整除 10）'),
        dict(type='array', var=lambda S: [S['ans'], S['pow10']], pointers={}, h=200, label='ans, pow10'),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('z', 'z', 'cyan'), ('pow10', 'pow10', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'pow10 = 1': '`pow10` 是当前数位的权重，从个位 `1` 开始',
        'while x and y and z': lambda S, B, r: (f'`x={S.x}, y={S.y}, z={S.z}` 都非 0，继续' if S.x and S.y and S.z
            else '有一个数变成 0 了：更高位的最小值一定是 0，不用再算 → 结束'),
        'ans +=': '这一位最小值 `min({B.x % 10}, {B.y % 10}, {B.z % 10})` = {min(B.x % 10, B.y % 10, B.z % 10)}，乘权重 `{B.pow10}` 加进答案：`ans` → =={ans}==',
        'x //= 10': '去掉 x 的最低位：`x` → {x}',
        'y //= 10': '去掉 y 的最低位：`y` → {y}',
        'z //= 10': '去掉 z 的最低位：`z` → {z}',
        'pow10 *= 10': '权重进一位：`pow10` → {pow10}',
        'return ans': '数字答案 `{ans}`',
    },
    cards=dict(
        one_liner='从个位开始，每一位取三数最小值，数位用 pow10 拼回去',
        complexity='时间 `O(log min(x,y,z))`，空间 `O(1)`',
        problem=['三个数按四位补前导 0，答案每一位取三数该位的最小值',
                 '返回去掉前导 0 的结果',
                 '示例：`987, 879, 798` → `777`'],
        quote='循环直到其中一个数等于 0 为止，因为后面的数位，最小值都是 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从最低位枚举：`x % 10` 取该位，`x //= 10` 丢掉该位',
              '最小值乘上 `pow10` 加入答案，不需要真的补前导 0',
              '任何一个数变成 0，更高位的最小值都是 0，直接停'],
        summary=['时间 `O(log min(x,y,z))`，空间 `O(1)`',
                 '循环条件是 `x and y and z`，不是 or：补的前导 0 会让最小值为 0',
                 '`pow10` 要与数位同步进位'],
    ),
)
