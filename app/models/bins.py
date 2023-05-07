import sys


bins = {
    "annual_inc": [
        {
            "label": "(-inf, 70000)",
            "max": 70000
        },
        {
            "label": "(70000, inf)",
            "max": sys.maxsize
        },
    ],
    "int_rate": [
        {
            "label": "(-inf, 9)",
            "max": 9
        },
        {
            "label": "(9, 21)",
            "max": 21
        },
        {
            "label": "(21, inf)",
            "max": sys.maxsize
        },
    ],
    "loan_amnt": [
        {
            "label": "(-inf, 15000)",
            "max": 15000
        },
        {
            "label": "(15000, inf)",
            "max": sys.maxsize
        },
    ],
    "dti": [
        {
            "label": "(-inf, 15)",
            "max": 15
        },
        {
            "label": "(15, inf)",
            "max": sys.maxsize
        },
    ],
    "mths_since_last_delinq": [
        {
            "label": "(-inf, 12)",
            "max": 12
        },
        {
            "label": "(12, inf)",
            "max": sys.maxsize
        },
    ],
    "delinq_2yrs": [
        {
            "label": "(-inf, 10)",
            "max": 10
        },
        {
            "label": "(10, inf)",
            "max": sys.maxsize
        },
    ],
    "inq_last_6mths": [
        {
            "label": "(-inf, 15)",
            "max": 15
        },
        {
            "label": "(15, inf)",
            "max": sys.maxsize
        },
    ],
    "open_acc": [
        {
            "label": "(-inf, 30)",
            "max": 30
        },
        {
            "label": "(30, inf)",
            "max": sys.maxsize
        },
    ],
    "pub_rec": [
        {
            "label": "(-inf, 5)",
            "max": 5
        },
        {
            "label": "(5, inf)",
            "max": sys.maxsize
        },
    ],
    "acc_now_delinq": [
        {
            "label": "(-inf, 2)",
            "max": 2
        },
        {
            "label": "(2, inf)",
            "max": sys.maxsize
        },
    ],
    "revol_util": [
        {
            "label": "(-inf, 75)",
            "max": 75
        },
        {
            "label": "(75, inf)",
            "max": sys.maxsize
        },
    ]
}