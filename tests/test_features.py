from app.features import FEATURE_NAMES, password_features


def test_password_features_match_expected_shape():
    features = password_features("Abc123!@")

    assert len(features) == len(FEATURE_NAMES)
    assert features[0] == 8
    assert features[2] == 1
    assert features[3] == 3
    assert features[4] == 2


def test_password_features_handle_empty_password():
    features = password_features("")

    assert features[0] == 0
    assert features[-1] == 0
