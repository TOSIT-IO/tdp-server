import json

import tdp_server.app

app = tdp_server.app.create_app()

print(json.dumps(app.openapi(), indent=2))
