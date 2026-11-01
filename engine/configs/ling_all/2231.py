CONFIG = dict(
    num=2231, title='按奇偶性交换后的最大数字', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='分组排序再填回（Go 原文转写）', tags=[],
    code='''
class Solution:
    def largestInteger(self, num: int) -> int:
        s = list(str(num).encode())
        a = [[], []]
        for v in s:
            a[v & 1].append(v)  # 分组
        a[0].sort(reverse=True)
        a[1].sort(reverse=True)  # 排序

        for i, ch in enumerate(s):
            j = ch & 1
            s[i] = a[j][0]  # 填回
            a[j] = a[j][1:]
        ans = int(bytes(s).decode())
        return ans
''',
    call='Solution().largestInteger(65875)',
    expect=87655,
    views=[
        dict(type='array', var=lambda S: [chr(x) for x in S['s']], label='s（逐位数字）', pointers={'i': 'blue'}, h=130),
        dict(type='array', var=lambda S: [chr(x) for x in S['a'][0]], label='a[0]：偶数位', h=120),
        dict(type='array', var=lambda S: [chr(x) for x in S['a'][1]], label='a[1]：奇数位', h=120),
    ],
    watch=['i', ('j', 'j', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        's = list': '把 `num` 拆成一位位数字（Go 里是字节，奇偶性和数字一致）',
        'a = [[], []]': '`a[0]` 放偶数位，`a[1]` 放奇数位',
        'a[v & 1].append': '数字 `{chr(v)}` 的奇偶位 `v & 1` = {v & 1} → 放进 `a[{v & 1}]`',
        'a[0].sort': '偶数位从大到小排好：大的要放在高位',
        'a[1].sort': '奇数位从大到小排好：大的要放在高位',
        'j = ch & 1': '位置 {i} 原来是 `{chr(ch)}`，奇偶类别 `j = {j}`',
        's[i] = a[j][0]': '该位置只能放同类里==最大的==：`{chr(s[i])}`',
        'a[j] = a[j][1:]': '用掉的数去掉，下一位同类取次大',
        'ans = int': '拼回整数：`{ans}`',
        'return ans': '最大数字 `{ret}`',
    },
    cards=dict(
        one_liner='奇偶各自从大到小排，再按奇偶位置填回',
        complexity='时间 `O(n log n)`，空间 `O(n)`，`n` 为位数',
        problem=['可任意交换奇偶性相同的两位数字，求最大的结果',
                 '示例：`1234` → `3412`',
                 '本视频：`65875` → `87655`'],
        quote='a[v&1] = append(a[v&1], v) // 分组 …… s[i] = a[j][0] // 填回',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['奇数只能和奇数换，偶数只能和偶数换 → 两组互不影响',
              '每组内部从大到小排序，位置的奇偶不变，所以高位放大的',
              '遍历原数字：看当前位是奇是偶，就从对应组取队首'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '`sort.Slice` 的 `>` 比较对应 `sort(reverse=True)`；字节切片用整数列表代替',
                 '时间 `O(n log n)`，空间 `O(n)`',
                 '易错：填回时按原数字每位的奇偶选组，不是按顺序填'],
    ),
)
