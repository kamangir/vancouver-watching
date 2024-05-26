#! /usr/bin/env bash

function vancouver_watching_action_git_before_push() {
    [[ "$(abcli_git get_branch)" == "main" ]] &&
        vancouver_watching pypi build
}
