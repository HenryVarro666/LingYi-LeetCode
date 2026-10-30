CONFIG = dict(
    num=1386, title='安排电影院座位', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表 + 位掩码',
    code='''
class Solution:
    def maxNumberOfFamilies(self, n: int, reservedSeats: List[List[int]]) -> int:
        seats = defaultdict(int)  # 2~9 有预定座位的行 -> 这一行具体哪些座位被预定
        for row, seat in reservedSeats:
            if 2 <= seat <= 9:
                seats[row] |= 1 << (seat - 2)  # 把二进制数的 seat-2 这一位变成 1

        # 注意：如果某一行只有 1 和 10 被预定，那么这一行不会插到哈希表中（相当于这一行是空的）
        # 示例 1 只有第 1 行和第 2 行插到哈希表中
        empty_rows = n - len(seats)
        ans = empty_rows * 2  # 一个空行可以容量 2 个四人小组
        for x in seats.values():
            # 在哈希表中的行，由于 2~9 至少一个座位被预定，所以至多容纳 1 个四人小组，ans 至多增加 1
            if x & 0b1111 == 0 or x & 0b111100 == 0 or x & 0b11110000 == 0:
                ans += 1
        return ans
''',
    call='Solution().maxNumberOfFamilies(3, [[1,2],[1,3],[1,8],[2,6],[3,1],[3,10]])',
    expect=4,
    views=[
        dict(type='array', var='reservedSeats', label='reservedSeats（[行, 座位]）', h=250, cell=150),
        dict(type='map', var='seats', fmt=lambda k, v: f'第{k}行 → {v:08b}', h=230, label='seats：行 → 掩码（低位 = 座位 2）'),
        dict(type='text', h=70, fn=lambda S: (f"`empty_rows` = {S['empty_rows']}，`ans` = =={S['ans']}==" if 'ans' in S else '')),
    ],
    watch=['row', 'seat', 'empty_rows', 'x', ('ans', 'ans', 'green')],
    captions={
        'if 2 <= seat <= 9': lambda S, B, r: (f'座位 `{S.seat}` 在 2~9 之内，要记下' if 2 <= S.seat <= 9 else f'座位 `{S.seat}` 是 1 或 10，任何四连座都用不到 → ==忽略=='),
        'seats[row] |= ': '第 `{row}` 行座位 `{seat}` 被占：把掩码第 `{seat-2}` 位置 1 → `{seats[row]:08b}`',
        'empty_rows = ': '没进哈希表的行全是空的：`{n} − {len(seats)}` = =={empty_rows}== 行',
        'ans = empty_rows': '每个空行放 2 组：`ans` = {empty_rows} × 2 = =={ans}==',
        'if x & 0b1111': lambda S, B, r: f"掩码 `{S.x:08b}`：座位 2~5 空 `{S.x & 15 == 0}`，4~7 空 `{S.x & 60 == 0}`，6~9 空 `{S.x & 240 == 0}` → " + ('至少有一块全空，能放 1 组' if (S.x & 15 == 0 or S.x & 60 == 0 or S.x & 240 == 0) else '三块都被占，这行放不了'),
        'ans += 1': '这一行至多再放 1 组：`ans` → =={ans}==',
        'return ans': '一共能安排 `{ans}` 组',
    },
    cards=dict(
        one_liner='空行放 2 组，只处理有预定的行，座位用位掩码',
        complexity='时间 `O(m)`，空间 `O(m)`（m 为预定数）',
        problem=['每排 10 座，四人小组必须坐 `2-5`、`4-7`、`6-9` 之一，且全空',
                 '给出已预定的座位，求最多能安排几组',
                 '示例：`n=3`，`[[1,2],[1,3],[1,8],[2,6],[3,1],[3,10]]` → `4`'],
        quote='如果某一行只有 1 和 10 被预定，那么这一行不会插到哈希表中（相当于这一行是空的）。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['行数可达 10^9，不能逐行扫：只把有预定的行放进哈希表',
              '一行的 2~9 号座位用二进制数表示，第 `i` 位 = 座位 `i+2`',
              '`x & 0b1111 == 0` 等三个判断分别检查三个四连座是否全空'],
        summary=['时间 `O(m)`，空间 `O(m)`',
                 '易错：只有 1、10 被占的行仍是空行，可放 2 组',
                 '有预定且 2~9 受影响的行，至多放 1 组，因为中间块与两侧块互相重叠',
                 '题解也提到可以用布尔数组代替二进制数'],
    ),
)
