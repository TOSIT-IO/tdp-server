import json

import tdp_server.main

app = tdp_server.main.create_app()

print(json.dumps(app.openapi(), indent=2))
