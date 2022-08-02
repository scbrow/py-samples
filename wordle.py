with open('words.txt', 'r') as file:
    a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z = \
        ([0, 0, 0, 0, 0] for k in range(26))
    letters = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z]
    first, second, third, fourth, fifth = ([] for p in range(5))
    optimal = [first, second, third, fourth, fifth]
    line = file.readlines()[0]
    words = line[1:-1].split('\", \"')
    for word in words:
        for i in range(0, 5):
            letters[ord(word[i]) - 97][i] += 1
    for j in range(0, 26):
        print(f'{chr(j + 97)}: {letters[j]}')
        for m in range(0, 5):
            optimal[m].append(letters[j][m])
    print('')

    print(
        f'Most Common By Position: {chr(optimal[0].index(max(optimal[0])) + 97)}{chr(optimal[1].index(max(optimal[1])) + 97)}'
        f'{chr(optimal[2].index(max(optimal[2])) + 97)}{chr(optimal[3].index(max(optimal[3])) + 97)}'
        f'{chr(optimal[4].index(max(optimal[4])) + 97)}')
    totals = []
    for let in letters:
        totals.append(sum(let))
    common = ''
    for t in range(1, 26):
        common = common + (chr(totals.index(sorted(totals)[-t]) + 97)) + ','
    print(f'Most Common Letters: {common[:-1]}')
