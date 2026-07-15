from zamery_education_v4.kernel.execution.cache import calculate_cache_key


def test_machine_local_values_do_not_change_cache_key() -> None:
    context = dict(capability_id="c", capability_version="1", runtime_digest="sha256:"+"a"*64, input_hashes=("sha256:"+"b"*64,), configuration={"x":1}, protocol_version="p", policy_version="v")
    left = calculate_cache_key(**context, temp_dir="/tmp/a", hostname="one")
    right = calculate_cache_key(**context, temp_dir="/tmp/b", hostname="two")
    assert left == right
