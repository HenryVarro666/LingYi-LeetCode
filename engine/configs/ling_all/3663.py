CONFIG = dict(
    num=3663, title='出现频率最低的数字', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='Counter 计数 + 元组取最小',
    tags=[],
    code='''
class Solution:
    def getLeastFrequentDigit(self, n: int) -> int:
        # 统计每个数字的出现次数
        cnt = Counter(str(n))

        # 找出现次数最小的数字
        min_ch = min((c, ch) for ch, c in cnt.items())[1]
        return int(min_ch)
''',
    call='Solution().getLeastFrequentDigit(723344511)',
    expect=2,
    views=[
        dict(type='string', var='str(n)', label='n 的每一位', cell=84, h=150),
        dict(type='map', var='cnt', label='cnt（数位 → 出现次数）', fmt=lambda k, v: f"'{k}': {v}", h=220, font=30),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"最小的 `(次数, 数字)` = ==({S['min_ch'] and S['cnt'][S['min_ch']]}, {S['min_ch']})==" if S.get('min_ch') else '')),
    ],
    watch=['n', ('min_ch', 'min_ch', 'green')],
    captions={
        'cnt = Counter': '把 `n` 转成字符串，`Counter` 数出每个数位出现几次：`{dict(cnt)}`',
        'min_ch = min': '把每个数位变成 `(次数, 数字)` 元组再取最小：==次数小的优先，次数相同数字小的优先== → `{min_ch}`',
        'return int': '最小元组对应的数位是 `{min_ch}`，转回整数返回 {ret}',
    },
    cards=dict(
        one_liner='用 (次数, 数字) 当比较键，一个 min 搞定两条规则',
        complexity='时间 `O(log n)`，空间 `O(D)`，`D = 10`',
        problem=['给整数 `n`，找十进制表示中 ==出现次数最少== 的数字',
                 '次数相同取 ==最小== 的数字',
                 '示例：`723344511` → `2`（7、2、5 都只出现一次，取最小的 2）'],
        quote='统计每个数组的出现次数，记在一个 cnt 哈希表（或者数组）中。然后遍历 cnt，找到其中出现次数最小的数字。如果出现次数相同，取其中最小的数字。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`Counter(str(n))` 直接把数位当字符计数',
              '元组比较先比第一项：写成 `(c, ch)`，就先比次数、再比数字',
              '字符 `\'0\'~\'9\'` 的大小顺序和数字一致，所以比字符就行'],
        after=[dict(heading='写法二：数组计数', lines=['开 `cnt = [0] * 10`，下标就是数位', '`while n > 0`：`cnt[n % 10] += 1`，`n //= 10`', '遍历 `cnt`，只看 `0 < c < min_c` 的数位', '因为从小到大遍历，次数相同时先遇到的数字更小，不会被后面的换掉'])],
        summary=['时间 `O(log n)`，空间 `O(D)`',
                 '元组顺序别写反：`(ch, c)` 会变成取最小的数字',
                 '写法二：用 `cnt[10]` 数组，不断 `n % 10`、`n //= 10` 取数位，只看 `cnt > 0` 的数位',
                 '数组写法里 `0 < c < min_c` 的 `0 <` 不能漏，没出现的数位不算'],
    ),
)
