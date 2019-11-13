# ura

 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![codecov](https://codecov.io/gh/eugenekoh/ura/branch/master/graph/badge.svg)](https://codecov.io/gh/eugenekoh/ura) [![Build Status](https://travis-ci.org/eugenekoh/ura.svg?branch=master)](https://travis-ci.org/eugenekoh/ura) [![Documentation Status](https://readthedocs.org/projects/ura-api/badge/?version=latest)](https://ura-api.readthedocs.io/en/latest/?badge=latest)

URA publishes URA related data for public use and is available for download for the creation, development and testing of innovative applications by third party. This is an unofficial python api wrapper for URA data services api. 

References: https://www.ura.gov.sg/maps/api

## Getting Started

### Prerequisites

You can register for an account [here](https://www.ura.gov.sg/maps/api/reg.html). After activation of your account, you will receive an email with an access key from which you can generate a token for access to the API. The email will also contain a user manual on URA Data Service API in PDF format.

### Installing

Install the package using pip

```bash
pip install ura
```

### Usage

Initialize client with access key. Each endpoint is represented by a function within the Client.  Please refer to [examples](https://github.com/eugenekoh/ura/tree/master/examples/endpoints_examples.ipynb) (recommended) or [documentation](https://ura-api.readthedocs.io/en/latest/source/ura.html) for information on other endpoints.

```python
URA_ACCESS_KEY = ''

client = Client(URA_ACCESS_KEY)
client.get_token()

carpark_availability = client.carpark_availability()
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
