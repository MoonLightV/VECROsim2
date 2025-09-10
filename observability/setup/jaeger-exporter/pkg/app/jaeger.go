package app

import (
	"encoding/json"
	"errors"
	"io/ioutil"
	"net/http"
	"net/url"
	"strconv"
)

var (
	jaegerSearchTracesEndpoint = "/api/traces"
)

// JaegerSearchTraces searches Jaeger for Traces with the given parameters
func JaegerSearchTraces(client *http.Client, host string, limit int, lookback, service, tags string) (*JaegerTracesResponse, error) {
	endpoint, err := url.Parse(host + jaegerSearchTracesEndpoint)
	if err != nil {
		return nil, err
	}

	queries := endpoint.Query()

	if limit > 0 {
		queries.Add("limit", strconv.Itoa(limit))
	}

	if len(lookback) > 0 {
		queries.Add("lookback", lookback)
	}

	if len(service) > 0 {
		queries.Add("service", service)
	}

	if len(tags) > 0 {
		queries.Add("tags", tags)
	}

	endpoint.RawQuery = queries.Encode()

	resp, err := client.Get(endpoint.String())
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode < 200 || resp.StatusCode > 299 {
		return nil, errors.New("received unexpected status code")
	}

	respData, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var jaegerResp *JaegerTracesResponse
	err = json.Unmarshal(respData, &jaegerResp)
	return jaegerResp, err
}
