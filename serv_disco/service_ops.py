import random
import consul
import netifaces
from .exceptions import *
import requests

class ServiceOps:

    services = dict()
    consul_client = None
    SERVICE_SETTINGS = None
    initialized = False
    
    # this structure is of below form
    #
    # {
    #   'host' : '',
    #   'port' : '',
    #   'dc' : '',
    #   'services' : [
    #       {
    #           'name' : '',
    #           'service_id' : '',
    #           'address' : '',
    #           'port' : '',
    #           'tags' : [],
    #           'healthcheck' : 'healthcheck_url',
    #           'hcinterval' : '',
    #           'hcttl: ''
    #       },
    #       {
    #           'name' : '',
    #           'service_id' : '',
    #           'address' : '',
    #           'port' : '',
    #           'tags' : [],
    #           'healthcheck' : 'healthcheck_url',
    #           'hcinterval' : '',
    #           'hcttl: ''
    #       }
    #    ]
    #  }

    @staticmethod
    def validate_config ():
        if ServiceOps.SERVICE_SETTINGS is None:
            return False

        return True

    @staticmethod
    def init ():
        # register the services in SERVICE_SETTINGS
        if ServiceOps.validate_config():
            ServiceOps.initialized = True
            ServiceOps.consul_client = ServiceOps.consul_manager.set_consul_client_props(
                                        ServiceOps.SERVICE_SETTINGS['host'],
                                        ServiceOps.SERVICE_SETTINGS['port'],
                                        ServiceOps.SERVICE_SETTINGS['dc'])

            for svc in ServiceOps.SERVICE_SETTINGS['services']:
                svc_obj = ServiceOps.service(ServiceOps.consul_client, svc['name'], svc['service_id'],
                                              svc['address'], svc['port'], svc['tags'],
                                              hc=consul.Check.http(svc['healthcheck'], svc['hcinterval'], svc['hcttl']))
                svc_obj.register()

    class consul_manager:
        consul_host = None
        consul_port = None
        consul_dc = None

        consul_client = None

        @staticmethod
        def set_consul_client_props(host, port, dc):

            if ServiceOps.consul_manager.consul_client is not None:
                raise ConsulClientError('Consul client has already been initialized, '
                                          'use consul_manager.get_consul_client')

            ServiceOps.consul_manager.consul_host = host
            ServiceOps.consul_manager.consul_port = port
            ServiceOps.consul_manager.consul_dc = dc

            return ServiceOps.consul_manager.get_consul_client()

        @staticmethod
        def get_consul_client ():
            if ServiceOps.consul_manager.consul_client is None:
                ServiceOps.consul_manager.consul_client = consul.Consul(host=ServiceOps.consul_manager.consul_host,
                                                                         port=ServiceOps.consul_manager.consul_port,
                                                                         dc = ServiceOps.consul_manager.consul_dc)

            return ServiceOps.consul_manager.consul_client

    class service:
        name = None
        service_id = None
        address = None
        port = None
        tags = None
        healthcheck = None
        consul_client = None

        def __init__(self, consul_client, name, service_id, address, port, tags, hc=None):
            self.name = name
            self.service_id = service_id
            self.address = address
            self.port = port
            self.tags = tags
            self.consul_client = consul_client
            self.healthcheck = hc

        def register (self):
            if ServiceOps.services.get(self.name + ':' + self.service_id) is not None:
                return "Service %s:%s already registered" % (self.name, self.service_id)

            reg_status = self.consul_client.\
                agent.\
                service.register(self.name, service_id = self.service_id, address = self.address, port = self.port,
                                 tags = self.tags, check=self.healthcheck)

            if reg_status is False:
                raise (ServiceRegDeregError("Service registration failed"))
            else:
                ServiceOps.services[self.name + ':' + self.service_id] = self
                return "Success registering %s:%s" % (self.name, self.service_id)

        def deregister (self):
            dereg_status = self.consul_client.agent.service.deregister(self.service_id)

            if dereg_status is False:
                raise (ServiceRegDeregError("Service deregistration failed"))
            else:
                ServiceOps.services.pop(self.name + ':' + self.service_id)
                return "Success deregistering %s:%s" % (self.name, self.service_id)

    @staticmethod
    def get_callable_endpoint (service_name):
        if not ServiceOps.initialized:
            raise ServiceDiscoError("Service ops uninitialized yet")

        ep = ServiceOps.get_service_endpoint(service_name)

        if ep is not None:
            return 'http://%s:%s' % (ep['service_address'], ep['service_port'])

        return None

    @staticmethod
    def get_service_endpoint (service_name):
        if not ServiceOps.initialized:
            raise ServiceDiscoError("Service ops uninitialized yet")

        if service_name is None or service_name is '':
            return None

        endpoints = ServiceOps.get_service_catalog().service(service_name)

        # get list of all healthy services
        healthy_services = ServiceOps.consul_manager.get_consul_client().health.state('passing')[1]
        healthy_instances = list()

        for h_service in healthy_services:
            for ep in endpoints[1]:
                if h_service['ServiceName'] == service_name and h_service['ServiceID'] == ep['ServiceID']:
                    healthy_instances.append(ep)

        if len(healthy_instances) != 0:
            endpoint = random.choice(healthy_instances)
            return {'service' : endpoint['ServiceName'], 'service_id' : endpoint['ServiceID'],
                    'service_port' : endpoint['ServicePort'], 'service_address' : endpoint['ServiceAddress']}

        return None

    @staticmethod
    def get_service_catalog ():
        if not ServiceOps.initialized:
            raise ServiceDiscoError("Service ops uninitialized yet")

        return ServiceOps.consul_client.catalog

    @staticmethod
    def get_self_services ():
        if not ServiceOps.initialized:
            raise ServiceDiscoError("Service ops uninitialized yet")

        return ServiceOps.services

    @staticmethod
    def get_interface_addr (interface_name, container_network=None):
        try:
            if container_network is 'rancher': # get ip from rancher-metadata service
                res  = requests.get('http://rancher-metadata/2015-12-19/self/container/ips/0')
                if res.status_code == 200:
                    return res.text
                raise BaseException(res.text)
        except BaseException as e:
            raise e
            
        if interface_name is None:
            raise ConsulClientError ('Invalid interface_name passed')

        # return the last available iface addr
        ip = netifaces.ifaddresses(interface_name)[2][0]['addr']
        return ip

    @staticmethod
    def deregister_self_services ():
        self_services = ServiceOps.get_self_services()
        for svc, svc_obj in list(self_services.items()): # works in python 3
            self_services[svc].deregister()
