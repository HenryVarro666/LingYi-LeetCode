def _draw(cv, S, B, box, T):
    """竖式加法：a、b 右对齐，黄框 = 当前这一位，carry 写在这一列上方"""
    x0, y0, x1, y1 = box
    a, b = S.get('a'), S.get('b')
    if a is None or b is None:
        return
    cv.text((x0 + 18, y0 + 4), '竖式加法（从右往左，黄框 = 正在算的这一位）', 24, T['muted'], bold=True)
    ans = S.get('ans') or []
    line = S.get('_line')
    n = max(len(a), len(b)) + 1
    cw = min(96, (x1 - x0 - 260) / n)
    right = x0 + (x1 - x0) / 2 + n * cw / 2 + 40
    ys = dict(carry=y0 + 62, a=y0 + 122, b=y0 + 212, ans=y0 + 330)

    def X(c):
        return right - (c + 1) * cw

    cur = len(ans) - 1 if line in (13, 14) else len(ans)
    if 'i' in S and 0 <= cur < n:
        cv.rect((X(cur) - 4, ys['carry'] - 8, X(cur) + cw + 4, ys['ans'] + cw * 0.9 + 8), fill=T['yellow'], alpha=28, r=12)
        cv.rect((X(cur) - 4, ys['carry'] - 8, X(cur) + cw + 4, ys['ans'] + cw * 0.9 + 8), outline=T['yellow'], width=3, r=12)
    for name, s, c0 in (('a', a, T['blue']), ('b', b, T['pink'])):
        y = ys[name]
        cv.text((X(n - 1) - 30, y + cw * 0.45), name, 30, c0, anchor='rm', bold=True)
        for k, ch in enumerate(s):
            c = len(s) - 1 - k
            done = c < len(ans) and not (line in (13, 14) and c == len(ans) - 1)
            fill = c0 if (c == cur and 'i' in S) else T['panel2']
            cv.rect((X(c) + 4, y, X(c) + cw - 4, y + cw * 0.9), fill=fill, r=8, outline=T['border'])
            cv.text((X(c) + cw / 2, y + cw * 0.45), ch, 36, T['bg'] if fill != T['panel2'] else (T['dim'] if done else T['text']),
                    anchor='mm', bold=True)
    cv.text((X(n - 1) + cw / 2, ys['b'] + cw * 0.45), '+', 40, T['muted'], anchor='mm', bold=True)
    ly = ys['b'] + cw * 0.9 + 18
    cv.line([(X(n - 1) - 10, ly), (right + 10, ly)], T['muted'], 3)
    # carry
    carry = S.get('carry')
    cc = len(ans) - 1 if line == 13 else len(ans)
    if carry and 0 <= cc < n:
        cv.d.ellipse((X(cc) + cw / 2 - 20, ys['carry'] - 2, X(cc) + cw / 2 + 20, ys['carry'] + 38), fill=T['orange'])
        cv.text((X(cc) + cw / 2, ys['carry'] + 18), carry, 26, T['bg'], anchor='mm', bold=True)
    cv.text((X(n - 1) - 30, ys['carry'] + 18), 'carry', 24, T['orange'], anchor='rm', bold=True)
    # ans (append 到末尾 = 竖式里从右往左)
    cv.text((X(n - 1) - 30, ys['ans'] + cw * 0.45), 'ans', 30, T['green'], anchor='rm', bold=True)
    for c, ch in enumerate(ans):
        just = line == 13 and c == len(ans) - 1
        cv.rect((X(c) + 4, ys['ans'], X(c) + cw - 4, ys['ans'] + cw * 0.9), fill=T['green'] if just else T['panel2'], r=8,
                outline=T['yellow'] if just else T['border'], width=3 if just else 1)
        cv.text((X(c) + cw / 2, ys['ans'] + cw * 0.45), ch, 36, T['bg'] if just else T['text'], anchor='mm', bold=True)
    if ans:
        cv.text((x0 + 22, y1 - 30), f"列表 ans = {ans}（append 在末尾，最后要反转）", 22, T['muted'], anchor='lm', mono=True)


def _cap_while(S, B, ret):
    i, j, c = B.i, B.j, B.carry
    if i >= 0 or j >= 0:
        return f'`i = {i}`，`j = {j}`：还有数位没加完 → 继续'
    if c:
        return f'`a`、`b` 都遍历完了，但==还剩进位== `carry = {c}` → 还要再算一位'
    return '`a`、`b` 都遍历完，且没有进位 → 结束'


def _cap_s(S, B, ret):
    s = S.s
    return f'计算这一位的加法：`s = {S.x} + {S.y} + {B.carry}` = =={s}==（二进制 `{bin(s)[2:]}`）'


CONFIG = dict(
    num=67, title='二进制求和', difficulty='Easy', category='数学',
    author='灵茶山艾府', technique='模拟竖式加法（维护进位）',
    tags=['字节30天', '面试经典150'],
    code='''
class Solution:
    def addBinary(self, a: str, b: str) -> str:
        ans = []
        i = len(a) - 1  # 从右往左遍历 a 和 b
        j = len(b) - 1
        carry = 0  # 保存进位

        while i >= 0 or j >= 0 or carry:
            x = int(a[i]) if i >= 0 else 0
            y = int(b[j]) if j >= 0 else 0
            s = x + y + carry  # 计算这一位的加法
            # 例如 s = 10，把 '0' 填入答案，把 carry 置为 1
            ans.append(str(s % 2))
            carry = s // 2
            i -= 1
            j -= 1

        return ''.join(reversed(ans))
''',
    call='Solution().addBinary("1011", "111")',
    expect='10010',
    skip=['i -= 1', 'j -= 1'],
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'x', 'y', ('s', 's'), ('carry', 'carry', 'orange')],
    captions={
        'ans = []': '`ans` 收集答案的每一位：==从低位到高位== append，最后再反转',
        'i = len(a) - 1': '从右往左遍历 a 和 b：`i = {i}` 指向 a 的最低位',
        'j = len(b) - 1': '`j = {j}` 指向 b 的最低位',
        'carry = 0': '`carry` 保存进位，一开始是 0',
        'while i >= 0': _cap_while,
        'x = int(a[i])': lambda S, B, r: (f'a 这一位：`a[{S.i}] = {S.x}`' if S.i >= 0 else '`i < 0`：a 已经用完 → 这一位当作 ==0=='),
        'y = int(b[j])': lambda S, B, r: (f'b 这一位：`b[{S.j}] = {S.y}`' if S.j >= 0 else '`j < 0`：b 已经用完 → 这一位当作 ==0=='),
        's = x + y + carry': _cap_s,
        'ans.append': '答案这一位填 `s % 2 = {s % 2}` → append 到 `ans` 末尾',
        'carry = s // 2': lambda S, B, r: (f'进位更新为 `s // 2 = {S.carry}`' + ('：==向高位进 1==' if S.carry else '：没有进位')),
        'return': '`ans` 是从低位到高位存的，==反转==后拼接：返回 =={ret}==',
    },
    cards=dict(
        one_liner='和十进制一样：从右往左逐位相加，维护进位 carry',
        complexity='时间 `O(max(n, m))`，空间 `O(max(n, m))`',
        problem=['给两个二进制字符串 `a` 和 `b`，以二进制字符串的形式返回它们的和',
                 '示例：`a = "11", b = "1"` → `"100"`；`"1010" + "1011"` → `"10101"`',
                 '本视频：`"1011" + "111"`（11 + 7）→ `"10010"`（18）'],
        quote='需要在计算过程中维护进位值 carry，每次计算 ==sum = a 这一位的值 + b 这一位的值 + carry==，然后答案这一位填 sum mod 2，进位更新为 floor(sum / 2)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['和十进制加法一样，==从低到高==（从右往左）计算',
              '一个串遍历完了就把它的这一位当作 `0`，循环条件里==带上 carry==',
              '写法一：结果 append 到末尾，最后反转'],
        result='`11 + 7 = 18`：返回 `"10010"`，最后一位完全来自进位',
        summary=['时间、空间都是 `O(max(n, m))`',
                 '易错：`a`、`b` 都遍历完了还要看 carry，否则 `"1" + "1"` 会得到 `"0"`',
                 '易错：append 得到的是倒序，别忘了 `reversed`',
                 '写法二：先保证 `len(a) >= len(b)`，开 `n+1` 长的数组直接从右往左填，不用反转'],
    ),
)
