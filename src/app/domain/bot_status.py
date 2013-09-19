FORFEIT = "forfeit"
SURRENDER = "surrender"
KNOCKOUT = "ko"
TECHNICAL_KNOCKOUT = "tko"
JUDGES_DECISION = "judge"

BOT_STATUSES = {
    FORFEIT: {
        "name": "Forfeit",
        "description": "A robot forfeited the match, before the match started."
    },
    SURRENDER: {
        "name": "Surrender",
        "description": "A robot surrendered during the match."
    },
    KNOCKOUT: {
        "name": "Knockout",
        "description": "A robot was defeated by knockout."
    },
    TECHNICAL_KNOCKOUT: {
        "name": "Technical Knockout",
        "description": "A robot was defeated by technical knockout."
    },
    JUDGES_DECISION: {
        "name": "Judge's Decision",
        "description": "The match was called by a judge's decision."
    }
}