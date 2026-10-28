"""Starter tests for the weather module.

These tests deliberately cover only ordinary examples. They show how pytest works,
but they are not a sufficient test suite for the specification in SPECIFICATION.md.
"""

import pytest
from weather import (
    average_temperature,
    filter_by_temperature,
    hottest_measurement,
    parse_measurement,
    parse_time,
)

# - Der Text muss aus **zwei numerischen Bestandteilen** bestehen, getrennt durch genau
#   einen Doppelpunkt `:`.
# - Führende Nullen sind optional. Beispielsweise sind `"9:05"`, `"09:05"` und
#   `"9:5"` gültige Schreibweisen.
# - Die Stunde muss zwischen **0 und 23 einschließlich** liegen.
# - Die Minute muss zwischen **0 und 59 einschließlich** liegen.
# - Bei ungültigem Format, nicht-numerischen Bestandteilen oder ungültigen Werten wird
#   `ValueError` ausgelöst.

def test_parse_time_regular_time():
    assert parse_time("14:21") == 861

def test_parse_time_colo():
    with pytest.raises(ValueError):
        parse_time("14.21")

def test_parse_time_three_parts():
     with pytest.rasies(ValueError):
         parse_time("14:25:22")

def test_parse_time_zero():
    assert parse_time("09:05") == 545

def test_parse_time_hour_oob():
    with pytest.raises(ValueError):
        parse_time("24:22")

def test_parse_time_minute_oob():
    with pytest.raises(ValueError):
        parse_time("12:60")

def test_parse_time_invalid_time():
    with pytest.raises(ValueError):
        parse_time("144:21")

# - `line` muss ein String sein. Für einen anderen Typ wird `ValueError` ausgelöst.
# - Die Zeile muss aus **genau drei** durch `;` getrennten Feldern bestehen.
# - Führende und nachfolgende Leerzeichen der drei Felder werden entfernt.
# - Der Stadtname darf nach dem Entfernen von Leerzeichen nicht leer sein.
# - Die Uhrzeit wird nach den Regeln von `parse_time()` verarbeitet.
# - Die Temperatur wird mit `float(...)` in eine Fließkommazahl umgewandelt.
# - Kann die Temperatur nicht als `float` interpretiert werden, wird `ValueError`
#   ausgelöst.
# - Es findet keine zusätzliche meteorologische Plausibilitätsprüfung der Temperatur
#   statt.

def test_parse_measurement_regular_line():
    assert parse_measurement("Köln;14:21;21.7") == ("Köln", 861, 21.7)

def test_parse_measurement_no_string():
    with pytest.raises(ValueError):
        parse_measurement(1)

def test_parse_measurement_to_many_parts():
    with pytest.raises(ValueError):
        parse_measurement("Köln;14:21;21.7;12")

def test_parse_measurement_whitespaces():
    assert parse_measurement("  Köln; 14:21  ;21.7   ") == ("Köln", 861, 21.7)

def test_parse_measurement_missing_city():
    with pytest.raises(ValueError):
        parse_measurement(" ;14:21;21.7")

def test_parse_measurement_temp_is_float():
    assert parse_measurement("Köln;14:21;21") == ("Köln", 861, 21.0)

# - Die Grenzen sind **inklusive**: `lower <= temperature <= upper`.
# - Die Reihenfolge der Messungen bleibt erhalten.
# - Doppelte bzw. identische Messungen bleiben doppelt vorhanden.
# !!!- Die übergebene Liste wird nicht verändert.
# - Ist `lower > upper`, wird `ValueError` ausgelöst.
# !!!- Das Ergebnis ist eine neue Liste.


def test_filter_by_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Bonn", 900, 25.0),
    ]

    assert filter_by_temperature(measurements, 15.0, 20.0) == [
        ("Düsseldorf", 720, 18.5)
    ]

def test_filter_by_temperature_borders():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Bonn", 900, 25.0),
    ]

    assert filter_by_temperature(measurements, 10.0, 15.0) == [
        ("Köln", 600, 10.0)
    ]

def test_filter_by_temperature_double_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Bonn", 900, 25.0),
        ("Düsseldorf", 720, 18.5)
    ]

    assert filter_by_temperature(measurements, 15.0, 20.0) == [
        ("Düsseldorf", 720, 18.5),
        ("Düsseldorf", 720, 18.5)
    ]

def filter_by_temperature_upper_lower_switch():
    measurements = [
            ("Köln", 600, 10.0),
            ("Düsseldorf", 720, 18.5),
            ("Bonn", 900, 25.0),
    ]

    with pytest.raises(ValueError):
        filter_by_temperature(measurements, 20.0, 15.0)

## `average_temperature(measurements, city)`

# Berechnet die mittlere Temperatur aller Messungen einer Stadt.

# ### Vertrag

# - Es werden ausschließlich Messungen berücksichtigt, deren Stadtname exakt `city`
#   entspricht.
# - Städtenamen werden **case-sensitive** verglichen. `"Köln"` und `"köln"` sind also
#   unterschiedliche Namen.
# - Der Mittelwert wird über alle passenden Messungen gebildet.
# - Gibt es keine Messung für die angegebene Stadt, wird `ValueError` ausgelöst.
# !!!- Die Eingabedaten werden nicht verändert.

# ---

def test_average_temperature_case_sensitive():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 720, 20.0),
        ("köln", 720, 30.0),
        ("köln", 720, 20.0)
    ]

    assert average_temperature(measurements, "Köln") == 15.0

def test_average_temperature_city_exactly():
    measurements = [
        ("Köln ", 600, 10.0),
        ("Könl", 720, 20.0),
        ("Koeln", 720, 30.0),
        ("Köln", 720, 20.0)
    ]

    assert average_temperature(measurements, "Köln") == 20.0

# def test_average_temperature_empty_temp():
#     measurements = [
#         ("Köln", 600),
#         ("Köln", 720, 25.0),
#         ("Köln", 720, 30.0),
#         ("Köln", 720, 20.0)
#     ]

#     assert average_temperature(measurements, "Köln") == 25.0

def test_average_temperature_city_exactly():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 720, 20.0),
        ("Köln", 720, 30.0),
        ("Köln", 720, 20.0)
    ]

    with pytest.raises(ValueError):
        average_temperature(measurements, "Düsseldorf")

def test_average_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 720, 20.0),
    ]

    assert average_temperature(measurements, "Köln") == 15.0

# - Gibt es nur eine eindeutige höchste Temperatur, wird diese Messung zurückgegeben.
# - Haben mehrere Messungen dieselbe höchste Temperatur, wird die Messung mit der
#   **frühesten Uhrzeit** zurückgegeben.
# - Haben mehrere Messungen sowohl dieselbe höchste Temperatur als auch dieselbe
#   Uhrzeit, bleibt die zuerst vorkommende dieser Messungen maßgeblich.
# - Für eine leere Sequenz wird `ValueError` ausgelöst.
# !!!- Die Eingabedaten werden nicht verändert.

def test_hottest_measurement_with_unique_maximum():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 25.0),
        ("Bonn", 900, 20.0),
    ]

    assert hottest_measurement(measurements) == ("Düsseldorf", 720, 25.0)

def test_hottest_measurement_with_multiple_maximum_diff_time():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 920, 20.0),
        ("Bonn", 800, 20.0),
    ]

    assert hottest_measurement(measurements) == ("Bonn", 800, 20.0)

def test_hottest_measurement_with_multiple_maximum_same_time():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 800, 20.0),
        ("Bonn", 800, 20.0),
    ]

    assert hottest_measurement(measurements) == ("Düsseldorf", 800, 20.0)

def test_hottest_measurement_empty_measurements():
    measurements = []

    with pytest.raises(ValueError):
        hottest_measurement(measurements)