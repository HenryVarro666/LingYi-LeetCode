CONFIG = dict(
    num=299, title='猜数字游戏', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表计数 · min 减公牛',
    tags=[],
    code='''
class Solution(object):
    def getHint(self, secret, guess):

        A = B = 0

        secret_dict = {}
        guess_dict = {}
        for index in range(len(secret)):
            if secret[index] == guess[index]:
                A += 1
            secret_dict[secret[index]] = secret_dict.get(secret[index], 0) + 1
            guess_dict[guess[index]] = guess_dict.get(guess[index], 0) + 1

        for char in guess_dict:
            B += min(guess_dict[char], secret_dict.get(char, 0))
        
        B -= A

        return str(A) + 'A' + str(B) + 'B'
''',
    call='Solution().getHint("1123", "0111")',
    expect='1A1B',
    views=[
        dict(type='string', var='secret', label='secret', cell=90, h=165, pointers={'index': 'blue'}),
        dict(type='string', var='guess', label='guess', cell=90, h=165, pointers={'index': 'pink'}),
        dict(type='map', var='secret_dict', label='secret_dict（每个数字在 secret 的次数）', fmt=lambda k, v: f"'{k}': {v}", h=115, font=32),
        dict(type='map', var='guess_dict', label='guess_dict（每个数字在 guess 的次数）', fmt=lambda k, v: f"'{k}': {v}", h=115, font=32),
        dict(type='text', h=70, size=28, fn=lambda S: (f"`A = {S['A']}`，`B = {S['B']}`" if 'A' in S else '')),
    ],
    watch=[('index', 'index', 'blue'), ('char', 'char', 'pink'), ('A', 'A', 'green'), ('B', 'B', 'orange')],
    captions={
        'A = B = 0': '`A` 记公牛（位置也对），`B` 先用来累计「数字相同」的总数',
        'secret_dict = {}': '`secret_dict`：每个数字在 secret 里出现的次数',
        'guess_dict = {}': '`guess_dict`：每个数字在 guess 里出现的次数',
        'for index in range': '看第 `{index}` 位：secret `{secret[index]}`，guess `{guess[index]}`',
        'if secret[index] == guess[index]': '`{secret[index]}` 对 `{guess[index]}`：{"==位置也对，是公牛==" if secret[index] == guess[index] else "位置不同，不是公牛"}',
        'A += 1': '公牛 `A` = =={A}==',
        'secret_dict[secret[index]]': 'secret 的 `{secret[index]}` 计数 → {secret_dict[secret[index]]}（不管是否公牛都计）',
        'guess_dict[guess[index]]': 'guess 的 `{guess[index]}` 计数 → {guess_dict[guess[index]]}',
        'for char in guess_dict': '枚举 guess 里出现过的数字 `{char}`',
        'B += min': lambda S, Bf, r: f"数字 `{S.char}`：guess 有 {S.guess_dict[S.char]} 个，secret 有 {S.secret_dict.get(S.char, 0)} 个，取小 `{min(S.guess_dict[S.char], S.secret_dict.get(S.char, 0))}` → `B` = {S.B}（公牛+奶牛）",
        'B -= A': lambda S, Bf, r: f"`B` 此时包含公牛，减去公牛 `A = {S.A}` → 奶牛 `B` = =={S.B}==",
        'return': lambda S, Bf, r: f"拼成提示：`{S.A}A{S.B}B`",
    },
    cards=dict(
        one_liner='每个数字：min(两边次数) = 公牛 + 奶牛，再减掉公牛',
        complexity='时间 `O(n)`，空间 `O(1)`（只有 10 种数字）',
        problem=['secret 是秘密数字，guess 是猜测，返回提示 `xAyB`',
                 '`x`：数字和位置都对；`y`：数字对但位置不对',
                 '数字可以重复',
                 '示例：secret = `1123`，guess = `0111` → `1A1B`'],
        quote='对于secret中的每个字母，统计出其出现的次数以及其出现在guess中的次数，二者取min就是这个字母的cows + bulls。',
        quote_src='—— yiduobo 题解原文',
        idea=['一个数字在两边各出现几次，==较小值==就是能配上的个数',
              '这些配对里既有公牛也有奶牛',
              '位置正确的单独数一遍得 `A`，总配对 − `A` = 奶牛'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`B` 先累加所有配对数，最后才 `B -= A`',
                 '`secret_dict.get(char, 0)`：guess 里的数字 secret 可能没有',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码无需其他改动',
                 '对比灵神：灵神只统计错位数字，不用最后减公牛'],
    ),
)
