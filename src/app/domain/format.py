ROUND_ROBIN = 'roundrobin'
SINGLE_ELIMINATION = 'singleelim'
DOUBLE_ELIMINATION = 'doubleelim'
DOUBLE_ELIMINATION_TRUE = 'doubletrue'

FORMATS = {
    ROUND_ROBIN: {
        'name': 'Round Robin',
        'description': 'Each robot fights every other robot once.'
    },
    SINGLE_ELIMINATION: {
        'name': 'Single Elimination',
        'description': 'Robots are eliminated after one loss.'
    },
    DOUBLE_ELIMINATION: {
        'name': 'Double Elimination',
        'description': 'Robots are eliminated after two losses, with the exception of the final match.'
    },
    DOUBLE_ELIMINATION_TRUE: {
        'name': 'True Double Elimination',
        'description': 'Robots are eliminated after two losses. In order for the B-side finalist to win, he or she must defeat the A-side finalist twice.'
    },
}