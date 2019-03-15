greek_lower = 'αβγδεζηθικλμνξοπρςστυφχψω'  # 945 ~ 969
greek_upper = greek_lower.upper()
greek = greek_lower + greek_upper

latin_lower = (
    'ß'  # 223 ss in German
    'àáâãäåæçèéêëìíîïðñòóôõö'  # 224 ~ 246
    'øùúûü'  # 248 ~ 252
)
latin_upper = latin_lower[1:].upper()  # ß does not have upper
latin = latin_lower + latin_upper

math = (
    '±'  # 177
    '×'  # 215
    '÷'  # 247
)
