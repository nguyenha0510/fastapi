ERROR_CODE = {

    # Error code test

    502: {
        'code': 502,
        'status_code': 502,
        'message': '{} - {} - {}'
    },

    # Error code 400

    400: {
        'code': 400,
        'status_code': 400,
        'message': 'Bad Request'
    },
    4000000: {
        'code': 400,
        'status_code': 4000000,
        'message': "Can't delete object in database"
    },
    4000001: {
        'code': 400,
        'status_code': 4000001,
        'message': 'User already has that pokemon'
    },
    4000002: {
        'code': 400,
        'status_code': 4000002,
        'message': 'Pokemon Not Found'
    },
    4000003: {
        'code': 400,
        'status_code': 4000003,
        'message': "You need to specify the pokemon_id in the api uri"
    },
    4000004: {
        'code': 400,
        'status_code': 4000004,
        'message': "User not found"
    },
    # Error code 401

    401: {
        'code': 401,
        'status_code': 401,
        'message': "Invalid Token"
    },
    4011000: {
        'code': 401,
        'status_code': 4011000,
        'message': "Invalid Signature"
    },
    4011001: {
        'code': 401,
        'status_code': 4011001,
        'message': "Invalid Audience"
    },
    4011002: {
        'code': 401,
        'status_code': 4011002,
        'message': "Token Expired"
    },
    4011003: {
        'code': 401,
        'status_code': 4011003,
        'message': "Decode Error"
    },
    4011004: {
        'code': 401,
        'status_code': 4011004,
        'message': "Token Not Found"
    },
    4011005: {
        'code': 401,
        'status_code': 4011005,
        'message': "User from session_token doesn't exist"
    },
    4011006: {
        'code': 401,
        'status_code': 4011006,
        'message': "You don't have the scope needed for this api"
    },
    4011007: {
        'code': 401,
        'status_code': 4011007,
        'message': "Token doesn't contains scopes"
    },
    4011008: {
        'code': 401,
        'status_code': 4011008,
        'message': "Authorization in wrong format scheme"
    },
    4011009: {
        'code': 401,
        'status_code': 4011009,
        'message': "Invalid jwt."
    },

    # Error code 500
    500: {
        'code': 500,
        'status_code': 500,
        'message': "Internal Error"
    },

    50000001: {
        'code': 500,
        'status_code': 50000001,
        'message': "{}"
    }
}
