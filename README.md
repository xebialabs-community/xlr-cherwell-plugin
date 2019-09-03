# XL Release Cherwell Plugin v1.0.0

[![Build Status][xlr-cherwell-plugin-travis-image]][xlr-cherwell-plugin-travis-url]
[![License: MIT][xlr-cherwell-plugin-license-image]][xlr-cherwell-plugin-license-url]
![Github All Releases][xlr-cherwell-plugin-downloads-image]

![logo](images/cherwell.png)


## Preface

This document describes the functionality provided by the XL Release Cherwell plugin.
  
See the [XL Release reference manual](https://docs.xebialabs.com/xl-release) for background information on XL Release and release automation concepts.  

## Overview

## Requirements

Note:  XLR version should not be lower than lowest supported version.  See <https://support.xebialabs.com/hc/en-us/articles/115003299946-Supported-XebiaLabs-product-versions>.

## Installation

* Copy the latest JAR file from the [releases page](https://github.com/xebialabs-community/xlr-cherwell-plugin/releases) into the `XL_RELEASE_SERVER/plugins/__local__` directory.
* Restart the XL Release server.

## Features/Usage/Types/Tasks

![cherwell_tasks](images/Cherwell_Tasks.png)

### Get Team List

Get a list of team names from Cherwell

![Cherwell_GetTeams](images/Cherwell_GetTeamsTask.png)

### Create Business Object

Create a new Cherwell Business Object

![Cherwell_CreateBusinessObjects](images/Cherwell_CreateBusinessObject.png)

#### Example JSON for 'Create Business Object - Business Object Json Field'
        ```
        {
            "busObId": "${busObId}",
            "fields": [
                {
                "dirty": true,
                "displayName": "string",
                "fieldId": "93543f7fa541b6c5befc264642875724a8be1797d1",
                "html": "string",
                "name": "RequestedBy",
                "value": "${requestedByValue}"
                },
                {
                "dirty": true,
                "displayName": "string",
                "fieldId": "9407d01580d0329f81f00b42bb9d680962dad97aba",
                "html": "string",
                "name": "Title",
                "value": "${titleValue}"
                },
                {
                "dirty": true,
                "displayName": "string",
                "fieldId": "934fb3e2b82015e7ec07fa41098a9efcb20b1e49d6",
                "html": "string",
                "name": "Description",
                "value": "${descriptionValue}"
                }
            ]
        }


        ```

### Get Business Object

This task retrieves a list of Business Object fields and values.

![Cherwell_GetBusinessObject](images/Cherwell_GetBusinessObject.png)

### Update Business Object

This task updates fields in a Business Object

![Cherwell_GetBusinessObject](images/Cherwell_UpdateBusinessObject.png)

### Poll Business Object for field value change

This task polls a Business Object field and looks for an expected value change. The task can be configured with a list of possible expected values. The task will complete successfully the first time any one of the expected values is detected. The detected value will be displayed in the completed task output.

![Cherwell_GetBusinessObject](images/Cherwell_Polling.png)


## References

* [Cherwell API](https://cherwellsupport.com/WebHelp/csm/en/9.2/content/system_administration/rest_api/csm_rest_api_landing_page.html)
* [Swagger - Cherwell Rest API](https://cherwellsupport.com/CherwellAPI/Swagger/ui/index)


[xlr-cherwell-plugin-travis-image]: https://travis-ci.org/xebialabs-community/xlr-cherwell-plugin.svg?branch=master
[xlr-cherwell-plugin-travis-url]: https://travis-ci.org/xebialabs-community/xlr-cherwell-plugin
[xlr-cherwell-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xlr-cherwell-plugin-license-url]: https://opensource.org/licenses/MIT
[xlr-cherwell-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-cherwell-plugin/total.svg

