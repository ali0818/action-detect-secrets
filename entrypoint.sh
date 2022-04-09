#!/bin/sh

cd "${GITHUB_WORKSPACE}" || exit 1

export REVIEWDOG_GITHUB_API_TOKEN="${INPUT_GITHUB_TOKEN}"

detect-secrets --version

GITHUB_BASEURL=https://api.github.com
GITHUB_API="/repos/${INPUT_REPOSITORY:-${GITHUB_REPOSITORY}}/actions/runs/${INPUT_RUN_ID:-${GITHUB_RUN_ID}}/jobs"
eval "$(curl --get -Ss -H "Authorization: token ${INPUT_GITHUB_TOKEN}" -H "Accept: application/vnd.github.v3+json" "${GITHUB_BASEURL}${GITHUB_API}?per_page=${INPUT_PER_PAGE:-30}" \
| jq -r --arg job_name "${INPUT_JOB_NAME}" '.jobs | map(select(.name == $job_name)) | .[0] | @sh "job_id=\(.id) html_url=\(.html_url)"')"
echo ::set-output name=job_id::"${job_id}"
export JOB_ID="${html_url}"

detect-secrets scan ${INPUT_DETECT_SECRETS_FLAGS} ${INPUT_WORKDIR} \
    | baseline2rdf -slack_token="${INPUT_SLACK_TOKEN}" \
    | reviewdog -f=rdjson \
        -name="${INPUT_NAME:-detect-secrets}" \
        -filter-mode="${INPUT_FILTER_MODE:-added}" \
        -reporter="${INPUT_REPORTER:-github-pr-check}" \
        -fail-on-error="${INPUT_FAIL_ON_ERROR}" \
        -level="${INPUT_LEVEL}" \
        ${INPUT_REVIEWDOG_FLAGS} \
