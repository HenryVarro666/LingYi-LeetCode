CONFIG = dict(
    num=717, title='1 比特与 2 比特字符', difficulty='Easy', category='模拟',
    author='yiduobo', technique='从头扫描解码',
    tags=[],
    code='''
class Solution(object):
    def isOneBitCharacter(self, bits):

        now = 0
        while now < len(bits):
            if bits[now] == 1:
                now += 2
            else:
                now += 1
                if now == len(bits):
                    return True

        return False
''',
    call='Solution().isOneBitCharacter([1,0,1,0,0])',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: ('' if 'now' not in S else f"正在解码的位置：`now = {S['now']}`")),
        dict(type='array', var='bits', pointers={'now': 'blue'}, h=300,
             dim=lambda S, i, v: 'now' in S and i < S['now']),
    ],
    watch=[('now', 'now', 'blue')],
    captions={
        'while now < len(bits)': lambda S, B, r: (f"`now = {S.now} < {len(S.bits)}`：还有字符没解码" if S.now < len(S.bits) else f"`now = {S.now}` 走到了末尾以外 → 结束循环"),
        'if bits[now] == 1': lambda S, B, r: (f"`bits[{S.now}] = 1` → ==必须连同下一位解码成两比特字符==" if S.bits[S.now] == 1 else f"`bits[{S.now}] = 0` → ==只能解码成一比特字符=="),
        'now += 2': '两比特字符：`now` 跳过两位 → {now}',
        'now += 1': '一比特字符：`now` 前进一位 → {now}',
        'if now == len(bits)': lambda S, B, r: (f"`now = {S.now} == len(bits)`：最后一个解码出的是一比特字符" if S.now == len(S.bits) else f"`now = {S.now} != {len(S.bits)}`：后面还有字符，继续"),
        'return True': '最后一个解码的字符是一比特 → ==True==',
        'return False': '最后一个字符被两比特字符吃掉了 → ==False==',
    },
    cards=dict(
        one_liner='一比特和两比特字符起头不同，从头解码即可',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['一比特字符是 `0`，两比特字符是 `10` 或 `11`',
                 '`bits` 以 `0` 结尾，问最后一个字符是否必为一比特字符',
                 '本视频：`[1,0,1,0,0]` → `True`'],
        quote='由于1比特字符和2比特字符的起头不一样，因此我们可以从头开始往后扫描，若当前字符为0，那么必须解码成1比特字符；若当前字符为1，那么必须连同下一个字符一起解码成2比特字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['当前是 0：只能是一比特，`now += 1`',
              '当前是 1：必是两比特，`now += 2`',
              '解码完最后一个字符时，看它是不是由一比特走到末尾的'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '只有在 `bits[now] == 0` 的分支里才判断 `now == len(bits)`',
                 '`bits[now] == 1` 时 `now += 2` 可能直接越过末尾 → 循环结束返回 False',
                 '对比灵神：灵神循环到 `n-1` 为止，最后比较 `i == n-1`；这里逐个解码并在途中返回'],
    ),
)
