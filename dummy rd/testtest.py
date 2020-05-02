def accumulate(op, init, seq):
    if not seq:
        return init
    else:
        return op(seq[0], accumulate(op, init, seq[1:]))


def accumulate_n(op, init, sequences):
    if (not sequences) or (not sequences[0]):
        return type(sequences)()
    else:
        return ([accumulate(op, init, [s[0] for s in sequences] )]
                + accumulate_n(op, init, [s[1:] for s in sequences]))


if __name__ == "__main__":
    print(accumulate_n(lambda x, y: x + y, 0, [[1, 2], [3, 4], [5, 6]]))
