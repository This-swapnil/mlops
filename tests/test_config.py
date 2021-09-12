import json
import logging
import os
import joblib
import pytest
from prediction_service.prediction import form_response, api_response
import prediction_service

input_data = {
    "incorrect_range": {
        "pt": 500,
        "RT": 2900,
        "Torque": 100,
        "TW": 100,
        "TWF": 5,
        "HDF": 5,
        "PWF": 5,
        "OSF": 5,
        "RNF": 5
    },
    "correct_range": {
        "pt": 306,
        "RT": 1168,
        "Torque": 3.8,
        "TW": 100,
        "TWF": 0,
        "HDF": 0,
        "PWF": 0,
        "OSF": 0,
        "RNF": 0
    },
    "incorrect_col": {
        "Process temperature [K]": 306,
        "Rotational speed [rpm]": 1168,
        "Torque [Nm]": 3.8,
        "Tool wear [min]": 100,
        "TWF": 0,
        "HDF": 0,
        "PWF": 0,
        "OSF": 0,
        "RNF": 0
    }
}

TARGET_range = {"min": 200, "max": 305}


def test_form_response_correct_range(data=input_data["correct_range"]):
    res = form_response(data)
    assert TARGET_range["min"] <= res <= TARGET_range["max"]


def test_api_response_correct_range(data=input_data["correct_range"]):
    res = api_response(data)
    assert TARGET_range["min"] <= res["response"] <= TARGET_range["max"]


def test_form_response_incorrect_range(data=input_data["incorrect_range"]):
    with pytest.raises(prediction_service.prediction.NotInRange):
        res = form_response(data)


def test_api_response_incorrect_range(data=input_data["incorrect_range"]):
    res = api_response(data)
    assert res["response"] == prediction_service.prediction.NotInRange(
    ).message


def test_api_response_incorrect_col(data=input_data["incorrect_col"]):
    res = api_response(data)
    assert res["response"] == prediction_service.prediction.NotInCols().message