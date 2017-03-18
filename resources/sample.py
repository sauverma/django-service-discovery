import os
from serv_disco.service_ops import ServiceOps
from serv_disco.service_invocation import ServiceInvoker

SELF_SERVICE_SETTINGS = {
    'host': '127.0.0.1',
    'port': 8500,
    'dc': os.getenv('DC'),
    'services': [
        {
            'name': 'sampleService',
            'service_id': 'sampleService_instance_1',
            'address': ServiceOps.get_interface_addr('eth0'), # register service to listen on eth0 interface
            'port': 9040, # service port
            'tags': ['primary'], # additional tags
            'healthcheck': 'http://%s:9040/healthcheck/' % ServiceOps.get_interface_addr(os.getenv('SERVICE_INTERFACE')), # healthcheck url
            'hcinterval': '60s',
            'hcttl': '60s'
        },
    ]
}

ServiceOps.SERVICE_SETTINGS = SELF_SERVICE_SETTINGS
ServiceOps.init()

CALLEE_SERVICE_MAPPINGS = {
    'REMOTE_SERVICE': {
        'name': 'remoteService',
        'create': '/api/v1/remoteService/resource',
        'get': '/api/v1/remoteService?id=%s'
    }
}


res = ServiceInvoker.post(CALLEE_SERVICE_MAPPINGS['REMOTE_SERVICE']['name'],
                          CALLEE_SERVICE_MAPPINGS['DSP_LIST_SERVICE']['create'],
                          data={'param1': 'pv1', 'param2': 'pv2'},
                          async=False,)