def demote_headings(value, levels_to_demote):
    levels_handled = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', ]

    for index, level in reversed(list(enumerate(levels_handled))):
        try:
            value = value.replace(
                '<%s>' % level,
                '<%s>' % levels_handled[index + levels_to_demote]
            )

            value = value.replace(
                '</%s>' % level,
                '</%s>' % levels_handled[index + levels_to_demote]
            )
        except IndexError:
            continue

    return value
