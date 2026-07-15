from importlib.metadata import version

import zamery_education_v4


def test_package_exposes_v4_identity() -> None:
    assert zamery_education_v4.__version__ == "4.0.0"
    try:
        installed = version("zamery-education-v4")
    except Exception:
        installed = zamery_education_v4.__version__
    assert installed == "4.0.0"
