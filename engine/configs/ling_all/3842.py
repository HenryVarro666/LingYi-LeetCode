CONFIG = dict(
    num=3842, title='切换打开灯泡', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表 · 奇偶性',
    tags=[],
    code='''
class Solution:
    def toggleLightBulbs(self, bulbs: List[int]) -> List[int]:
        cnt = Counter(bulbs)
        return sorted(i for i, c in cnt.items() if c % 2)
''',
    call='Solution().toggleLightBulbs([3,5,3,7,5,5])',
    expect=[5, 7],
    views=[
        dict(type='array', var='bulbs', label='bulbs（每个数 = 按一次这个编号的开关）', cell=90, h=200),
        dict(type='map', var='cnt', label='cnt（编号 → 被按的次数）', fmt=lambda k, v: f"{k}: {v}  {'奇 → 亮' if v % 2 else '偶 → 灭'}", h=260, font=30),
        dict(type='text', h=90, size=30, fn=lambda S: '初始全灭：==按偶数次 = 灭，按奇数次 = 亮==' if 'cnt' not in S else '次数为奇数的编号，就是最后亮着的灯'),
    ],
    watch=[('cnt', 'dict(cnt)', 'cyan')],
    captions={
        'cnt = Counter': '统计每个编号被按了几次：`cnt = {dict(cnt)}`',
        'return sorted': lambda S, B, ret: f'只留下次数为奇数的编号（`c % 2` 为真），再升序排序 → ==亮着的灯 {ret}==',
    },
    cards=dict(
        one_liner='开关偶数次 = 灭，奇数次 = 亮：数谁出现奇数次',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['100 盏灯一开始全灭，`bulbs` 里每个数表示按一次对应编号的开关',
                 '按完后返回亮着的灯的编号，升序',
                 '示例：`[10,30,20,10]` → `[20,30]`；本视频：`[3,5,3,7,5,5]` → `[5,7]`'],
        quote='如果一个灯泡开关偶数次，那么这个灯泡最终是关闭的；如果一个灯泡开关奇数次，那么这个灯泡最终是打开的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['初始全灭，所以最后的状态只看==按了几次的奇偶性==',
              '问题变成：统计 `bulbs` 中哪些数出现了奇数次，用哈希表',
              '作者还问：如果 100 改成 10^9？哈希表照样能做，数组就不行了'],
        after=[dict(heading='为什么看奇偶', lines=['每按一次开关，状态翻转一次','翻转偶数次 = 回到原状态（灭）','翻转奇数次 = 和原状态相反（亮）','所以不用模拟，只数次数的奇偶就够了'])],
    summary=['时间 `O(n log n)`，瓶颈是最后的排序；空间 `O(n)`',
                 '易错点：按「次数奇偶」判断，不要模拟每次开关（也可以，但没有利用奇偶性）',
                 '编号范围很大时不能开数组，要用哈希表（这是原文的追问）',
                 '同类题：找出现奇数次的数（异或、哈希表）'],
    ),
)
