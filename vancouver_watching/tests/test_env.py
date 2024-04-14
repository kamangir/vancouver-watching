from abcli import env


def test_abcli_env():
    assert env.abcli_path_home
    assert env.abcli_path_git
    assert env.abcli_path_storage

    assert env.ABCLI_AWS_RDS_DB
    assert env.ABCLI_AWS_RDS_PORT
    assert env.ABCLI_AWS_RDS_USER
